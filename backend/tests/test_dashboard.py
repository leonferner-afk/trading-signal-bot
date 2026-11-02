"""The status page on SYNTHETIC inputs only (no network): history bookkeeping,
the Markdown subset the report uses, escaping, and the page itself."""
from __future__ import annotations

import datetime as dt
import json

import pytest

from app.dashboard import _rotation_part, build_site, render_report, update_history

H = {"base_sek": 10000.0, "total_sek": 10150.0, "delta_sek": 150.0, "delta_pct": 1.5, "since": "2026-10-30",
     "index_pct": 75.0, "index_sek_pct": 1.0, "rocket_paper_sek": 10400.0,
     "positions": [{"symbol": "LLY", "kind": "rotation", "status": "open", "sek_return_pct": 6.0}]}


def test_rotation_part_is_the_tracker_minus_the_index_part():
    stake, value = _rotation_part(H)
    # Index part: 7 500 kr +1 % = +75 kr, so the rotation's 2 500 kr made the other +75 kr.
    assert stake == pytest.approx(2500.0) and value == pytest.approx(2575.0)


def test_history_starts_at_the_restart_and_keeps_one_point_per_day():
    hist = update_history([], H, "2026-11-03")
    assert [p["date"] for p in hist] == ["2026-10-30", "2026-11-03"]
    assert hist[0]["total_sek"] == 10000.0 and hist[1]["total_sek"] == 10150.0
    assert hist[1]["spy_sek"] == pytest.approx(10100.0) and hist[1]["rocket_sek"] == 10400.0
    again = update_history(hist, {**H, "total_sek": 10200.0}, "2026-11-03")       # re-run the same day replaces
    assert [p["total_sek"] for p in again] == [10000.0, 10200.0]
    old = [{"date": "2026-10-27", "since": "2026-10-26", "total_sek": 9000.0, "spy_sek": None, "rocket_sek": None}]
    assert [p["date"] for p in update_history(old, H, "2026-11-03")] == ["2026-10-30", "2026-11-03"]  # other restart dropped


def test_report_markdown_subset_is_rendered_and_escaped():
    md = ("# Tradingbot 2026-11-03\n**Marknaden:** SPY över\n\n> ⚠ varning\n\n## 🟢 KÖP (1)\n- **LLY** — köp <b>nu</b>\n\n"
          "| Aktie | Köpt |\n|---|---|\n| AMD | 624.9 |\n---\nslut")
    out = render_report(md)
    assert "<h2>Tradingbot 2026-11-03</h2>" in out and "<strong>Marknaden:</strong> SPY över" in out
    assert "<blockquote>⚠ varning</blockquote>" in out and "<li><strong>LLY</strong> — köp &lt;b&gt;nu&lt;/b&gt;</li>" in out
    assert "<th>Aktie</th>" in out and "<td>624.9</td>" in out and "<hr>" in out and "---" not in out


def test_build_site_writes_the_page_and_history(tmp_path):
    (tmp_path / "reports").mkdir()
    (tmp_path / "hypothetical.json").write_text(json.dumps(H), encoding="utf-8")
    (tmp_path / "reports" / "latest.md").write_text("# Rapport\n<script>alert(1)</script>", encoding="utf-8")
    page = build_site(tmp_path, tmp_path / "site", now=dt.datetime(2026, 11, 3, 6, 30, tzinfo=dt.timezone.utc))
    text = page.read_text(encoding="utf-8")
    assert "10 150 kr" in text and "+1,5 %" in text and "S&amp;P 500-fonden" in text and "10 400 kr" in text
    assert "<script>" not in text and "&lt;script&gt;" in text                    # report content is escaped
    assert "<svg" in text and "LLY" in text and "2026-11-03 06:30 UTC" in text
    assert len(json.loads((tmp_path / "history.json").read_text(encoding="utf-8"))) == 2
    assert build_site(tmp_path / "missing", tmp_path / "x") is None
