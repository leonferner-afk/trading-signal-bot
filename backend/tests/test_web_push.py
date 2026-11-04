import base64
import json

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from app.notify import web_push
from app.notify.web_push import b64u, encrypt, parse_code, unb64u, vapid_authorization


def _raw(pub):
    return pub.public_bytes(serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint)


def _decrypt(body: bytes, ua_key, auth: bytes) -> bytes:
    """The browser's side of RFC 8291, written independently of the sender."""
    salt, rs, idlen = body[:16], int.from_bytes(body[16:20], "big"), body[20]
    as_pub = body[21:21 + idlen]
    ciphertext = body[21 + idlen:]
    assert rs == 4096
    shared = ua_key.exchange(ec.ECDH(), ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), as_pub))
    kdf = lambda s, info, n, ikm: HKDF(algorithm=hashes.SHA256(), length=n, salt=s, info=info).derive(ikm)
    ikm = kdf(auth, b"WebPush: info\x00" + _raw(ua_key.public_key()) + as_pub, 32, shared)
    cek = kdf(salt, b"Content-Encoding: aes128gcm\x00", 16, ikm)
    nonce = kdf(salt, b"Content-Encoding: nonce\x00", 12, ikm)
    plain = AESGCM(cek).decrypt(nonce, ciphertext, None)
    assert plain.endswith(b"\x02")
    return plain[:-1]


def test_payload_decrypts_with_the_subscription_keys():
    ua = ec.generate_private_key(ec.SECP256R1())
    auth = b"0123456789abcdef"
    msg = json.dumps({"title": "Min depå", "body": "🟢 KÖP AMGN · 1 308 kr"}, ensure_ascii=False).encode()
    body = encrypt(msg, b64u(_raw(ua.public_key())), b64u(auth))
    assert _decrypt(body, ua, auth) == msg


def test_vapid_jwt_is_signed_for_the_push_origin():
    key = ec.generate_private_key(ec.SECP256R1())
    d = b64u(key.private_numbers().private_value.to_bytes(32, "big"))
    pub = b64u(_raw(key.public_key()))
    header = vapid_authorization("https://web.push.apple.com/abc123", d, pub, now=1_000_000)
    jwt = header.split("t=")[1].split(",")[0]
    h, c, sig = jwt.split(".")
    claims = json.loads(unb64u(c))
    assert claims["aud"] == "https://web.push.apple.com" and claims["exp"] == 1_000_000 + 43200
    assert claims["sub"].startswith("https://") and header.endswith(f"k={pub}")
    raw = unb64u(sig)
    der = encode_dss_signature(int.from_bytes(raw[:32], "big"), int.from_bytes(raw[32:], "big"))
    key.public_key().verify(der, f"{h}.{c}".encode(), ec.ECDSA(hashes.SHA256()))    # raises if wrong


def test_notis_kod_round_trip_and_missing_secret(monkeypatch):
    code = base64.b64encode(json.dumps({"sub": {"endpoint": "https://web.push.apple.com/x",
                                                "keys": {"p256dh": "a", "auth": "b"}},
                                        "d": "c", "pub": "e"}).encode()).decode()
    assert parse_code(code)["sub"]["endpoint"].endswith("/x")
    monkeypatch.delenv("WEB_PUSH", raising=False)
    assert web_push.is_configured() is False and web_push.send("t", "b") is False
    monkeypatch.setenv("WEB_PUSH", "not-a-code")
    assert web_push.send("t", "b") is False
