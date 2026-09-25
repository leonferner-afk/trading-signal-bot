"""Zero-setup notification channel when running on GitHub Actions: opens an
issue in the bot's own repository, assigned to the repository owner, so
GitHub itself delivers it (email, and push if the GitHub app is
installed). Needs nothing beyond the workflow's built-in GITHUB_TOKEN.

Outside GitHub Actions (no GITHUB_TOKEN / GITHUB_REPOSITORY) every call is
a silent no-op returning None.
"""
from __future__ import annotations

import logging
import os

import httpx

logger = logging.getLogger("tradingbot.github_issue")

API = "https://api.github.com"
LABEL = "tradingbot"


def _context() -> tuple[str, str, str] | None:
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPOSITORY")
    owner = os.getenv("GITHUB_REPOSITORY_OWNER") or (repo.split("/")[0] if repo else None)
    if not (token and repo and owner):
        return None
    return token, repo, owner


def _headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}


def publish(title: str, body: str) -> str | None:
    """Creates the issue (assigned to the owner) and closes the bot's older
    open issues so only the latest summary stays open. Returns its URL."""
    ctx = _context()
    if ctx is None:
        return None
    token, repo, owner = ctx
    payload = {"title": title, "body": f"@{owner}\n\n{body}"[:65000], "assignees": [owner], "labels": [LABEL]}
    try:
        with httpx.Client(timeout=20.0, headers=_headers(token)) as http:
            resp = http.post(f"{API}/repos/{repo}/issues", json=payload)
            if resp.status_code == 422:  # e.g. label/assignee not allowed — retry bare
                resp = http.post(f"{API}/repos/{repo}/issues", json={"title": title, "body": payload["body"]})
            resp.raise_for_status()
            issue = resp.json()
            _close_older(http, repo, issue["number"])
            return issue.get("html_url")
    except httpx.HTTPError as exc:
        logger.warning("GitHub issue notification failed: %s", exc)
        return None


def _close_older(http: httpx.Client, repo: str, keep_number: int) -> None:
    try:
        resp = http.get(f"{API}/repos/{repo}/issues", params={"labels": LABEL, "state": "open", "per_page": 50})
        resp.raise_for_status()
        for issue in resp.json():
            if issue["number"] != keep_number and "pull_request" not in issue:
                http.patch(f"{API}/repos/{repo}/issues/{issue['number']}", json={"state": "closed", "state_reason": "completed"})
    except httpx.HTTPError as exc:
        logger.info("Could not close older bot issues: %s", exc)
