"""Web push to the owner's home-screen app (RFC 8030 delivery, RFC 8291
payload encryption, RFC 8292 VAPID), with only the `cryptography` package.

The app creates everything on the phone: a VAPID key pair and a push
subscription. It shows them as one "notis-kod" that the owner pastes as the
Actions secret WEB_PUSH — so no key lives in the public repo or the chat.
The code is base64 of JSON: {"sub": {"endpoint", "keys": {"p256dh", "auth"}},
"d": <VAPID private key, base64url>, "pub": <VAPID public key, base64url>}.
"""
from __future__ import annotations

import base64
import json
import logging
import os
import struct
import time
from urllib.parse import urlsplit

import httpx
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

logger = logging.getLogger("tradingbot.webpush")

SUBJECT = "https://github.com/leonferner-afk/trading-signal-bot"
RECORD_SIZE = 4096


def b64u(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def unb64u(text: str) -> bytes:
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def _hkdf(salt: bytes, info: bytes, length: int, ikm: bytes) -> bytes:
    return HKDF(algorithm=hashes.SHA256(), length=length, salt=salt, info=info).derive(ikm)


def encrypt(payload: bytes, p256dh: str, auth: str, *, salt: bytes | None = None,
            server_key: ec.EllipticCurvePrivateKey | None = None) -> bytes:
    """RFC 8291 'aes128gcm' body for one subscription (single record)."""
    ua_pub = unb64u(p256dh)
    server_key = server_key or ec.generate_private_key(ec.SECP256R1())
    as_pub = server_key.public_key().public_bytes(serialization.Encoding.X962,
                                                  serialization.PublicFormat.UncompressedPoint)
    shared = server_key.exchange(ec.ECDH(), ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), ua_pub))
    ikm = _hkdf(unb64u(auth), b"WebPush: info\x00" + ua_pub + as_pub, 32, shared)
    salt = salt or os.urandom(16)
    cek = _hkdf(salt, b"Content-Encoding: aes128gcm\x00", 16, ikm)
    nonce = _hkdf(salt, b"Content-Encoding: nonce\x00", 12, ikm)
    record = AESGCM(cek).encrypt(nonce, payload + b"\x02", None)      # 0x02 = last (and only) record
    return salt + struct.pack(">I", RECORD_SIZE) + bytes([len(as_pub)]) + as_pub + record


def vapid_authorization(endpoint: str, private_d: str, public_key: str, now: float | None = None) -> str:
    """RFC 8292 header value: an ES256 JWT for the push service's origin."""
    parts = urlsplit(endpoint)
    claims = {"aud": f"{parts.scheme}://{parts.netloc}", "exp": int((now or time.time()) + 12 * 3600), "sub": SUBJECT}
    signing_input = (b64u(json.dumps({"typ": "JWT", "alg": "ES256"}, separators=(",", ":")).encode()) + "."
                     + b64u(json.dumps(claims, separators=(",", ":")).encode()))
    key = ec.derive_private_key(int.from_bytes(unb64u(private_d), "big"), ec.SECP256R1())
    r, s = decode_dss_signature(key.sign(signing_input.encode(), ec.ECDSA(hashes.SHA256())))
    jwt = signing_input + "." + b64u(r.to_bytes(32, "big") + s.to_bytes(32, "big"))
    return f"vapid t={jwt}, k={public_key}"


def parse_code(code: str) -> dict:
    data = json.loads(base64.b64decode(code.strip()))
    sub = data["sub"]
    if not (sub.get("endpoint", "").startswith("https://") and sub["keys"]["p256dh"] and sub["keys"]["auth"]
            and data["d"] and data["pub"]):
        raise ValueError("incomplete notis-kod")
    return data


def is_configured() -> bool:
    return bool(os.environ.get("WEB_PUSH", "").strip())


def send(title: str, body: str, url: str = "./", timeout: float = 15.0) -> bool:
    """Pushes one notification to the app. False (and a log line) on any problem."""
    code = os.environ.get("WEB_PUSH", "").strip()
    if not code:
        logger.warning("Web push not configured (WEB_PUSH missing) — skipping.")
        return False
    try:
        cfg = parse_code(code)
    except Exception as exc:  # malformed secret
        logger.error("WEB_PUSH is not a valid notis-kod: %s", exc)
        return False
    sub = cfg["sub"]
    payload = json.dumps({"title": title, "body": body, "url": url}, ensure_ascii=False).encode()
    try:
        res = httpx.post(sub["endpoint"], timeout=timeout,
                         content=encrypt(payload, sub["keys"]["p256dh"], sub["keys"]["auth"]),
                         headers={"Authorization": vapid_authorization(sub["endpoint"], cfg["d"], cfg["pub"]),
                                  "Content-Encoding": "aes128gcm", "Content-Type": "application/octet-stream",
                                  "TTL": "86400", "Urgency": "normal"})
    except httpx.HTTPError as exc:
        logger.error("Web push failed: %s", exc)
        return False
    if res.status_code in (404, 410):
        logger.error("Web push: the app's subscription has expired — turn notifications on again in the app "
                     "and paste the new notis-kod as WEB_PUSH.")
        return False
    if res.status_code >= 300:
        logger.error("Web push rejected: HTTP %s %s", res.status_code, res.text[:300])
        return False
    return True
