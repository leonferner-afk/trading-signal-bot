"""A small public status page (GitHub Pages), rebuilt after every daily run
from the files the run already writes to the bot-state branch:
hypothetical.json (the kronor tracker), reports/latest.md (the day's
report) and history.json (one point per run, kept here so the page can
draw how the stake developed over time).

Everything shown is paper/hypothetical — the page says so, and never shows
anything the run itself didn't compute.
"""
from __future__ import annotations

import datetime as dt
import html
import json
from pathlib import Path


def _rotation_part(h: dict) -> tuple[float, float]:
    """(rotation stake, its value now) — the rest of the tracker after the index part."""
    base = h["base_sek"]
    index_pct = h.get("index_pct") or 0.0
    index_stake = base * index_pct / 100
    index_delta = index_stake * (h.get("index_sek_pct") or 0.0) / 100
    stake = base - index_stake
    return stake, stake + h["delta_sek"] - index_delta


def update_history(history: list[dict], h: dict, today: str) -> list[dict]:
    """One point per run date (a re-run the same day replaces it). The first
    point is the restart itself, at par, so the curve starts at the stake."""
    out = [p for p in history if p.get("since") == h["since"] and p["date"] != today]
    if not out:
        out.append({"date": h["since"], "since": h["since"], "total_sek": h["base_sek"], "spy_sek": h["base_sek"],
                    "rocket_sek": None})
    spy = h["base_sek"] * (1 + h["index_sek_pct"] / 100) if h.get("index_sek_pct") is not None else None
    if today != h["since"]:
        out.append({"date": today, "since": h["since"], "total_sek": h["total_sek"], "spy_sek": spy,
                    "rocket_sek": h.get("rocket_paper_sek")})
    return sorted(out, key=lambda p: p["date"])


def _kr(value: float) -> str:
    return f"{value:,.0f}".replace(",", " ") + " kr"


def _pct(value: float | None) -> str:
    return "—" if value is None else f"{value:+.1f} %".replace(".", ",")


def _tone(value: float | None) -> str:
    return "" if value is None or abs(value) < 1e-9 else ("up" if value > 0 else "down")


def _inline(text: str) -> str:
    """Escaped text with the bot's only inline markup: **bold**."""
    parts = html.escape(text).split("**")
    return "".join(f"<strong>{p}</strong>" if i % 2 else p for i, p in enumerate(parts))


def render_report(md: str) -> str:
    """The small Markdown subset the bot's daily report uses (headings,
    tables, bullet lists, quotes, rules, bold, paragraphs) — rendered here
    so the page needs no external scripts. Everything is escaped."""
    out: list[str] = []
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            i += 1
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(set(c) <= set("-: ") for c in cells):
                    rows.append(cells)
                i += 1
            if rows:
                head = "".join(f"<th>{_inline(c)}</th>" for c in rows[0])
                body = "".join("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in r) + "</tr>" for r in rows[1:])
                out.append(f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>")
        elif line.startswith("#"):
            level = min(len(line) - len(line.lstrip("#")) + 1, 4)
            out.append(f"<h{level}>{_inline(line.lstrip('#').strip())}</h{level}>")
            i += 1
        elif line.strip() == "---":
            out.append("<hr>")
            i += 1
        elif line.lstrip().startswith("- "):
            items = []
            while i < len(lines) and lines[i].lstrip().startswith("- "):
                items.append(f"<li>{_inline(lines[i].lstrip()[2:])}</li>")
                i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
        elif line.startswith(">"):
            quote = []
            while i < len(lines) and lines[i].startswith(">"):
                quote.append(lines[i].lstrip(">").strip())
                i += 1
            out.append(f"<blockquote>{_inline(' '.join(quote))}</blockquote>")
        else:
            para = []
            while i < len(lines) and lines[i].strip() and not lines[i].lstrip().startswith(("|", "#", "- ", ">")) \
                    and lines[i].strip() != "---":
                para.append(lines[i].strip())
                i += 1
            out.append(f"<p>{'<br>'.join(_inline(p) for p in para)}</p>")
    return "\n".join(out)


def render_chart(history: list[dict]) -> str:
    """Inline SVG: the stake's value per run, next to 'all in the S&P 500'."""
    series = [("total_sek", "Din fördelning", "var(--accent)"), ("spy_sek", "Allt i S&P 500", "var(--muted)"),
              ("rocket_sek", "Raketportfölj (papper)", "var(--up)")]
    values = [p[k] for p in history for k, _, _ in series if p.get(k) is not None]
    if len(history) < 2 or not values:
        return '<p class="muted">Kurvan fylls på för varje handelsdag.</p>'
    w, h, pad_l, pad_r, pad_y = 480, 220, 74, 10, 16
    lo, hi = min(values), max(values)
    if hi - lo < 1:
        lo, hi = lo - 50, hi + 50
    x = lambda i: pad_l + (w - pad_l - pad_r) * i / (len(history) - 1)
    y = lambda v: pad_y + (h - 2 * pad_y) * (hi - v) / (hi - lo)
    parts = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="Utveckling sedan omstarten" class="chart">']
    for v in (lo, (lo + hi) / 2, hi):
        parts.append(f'<line x1="{pad_l}" x2="{w - pad_r}" y1="{y(v):.1f}" y2="{y(v):.1f}" class="grid"/>'
                     f'<text x="{pad_l - 6}" y="{y(v) + 4:.1f}" text-anchor="end" class="axis">{_kr(v)}</text>')
    for label_i in sorted({0, len(history) - 1}):
        anchor = "start" if label_i == 0 else "end"
        parts.append(f'<text x="{x(label_i):.1f}" y="{h - 1}" text-anchor="{anchor}" class="axis">'
                     f'{html.escape(history[label_i]["date"])}</text>')
    legend = []
    for key, label, color in series:
        pts = [(x(i), y(p[key])) for i, p in enumerate(history) if p.get(key) is not None]
        if not pts:
            continue
        path = " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
        parts.append(f'<polyline points="{path}" fill="none" stroke="{color}" stroke-width="2.5"/>')
        parts += [f'<circle cx="{a:.1f}" cy="{b:.1f}" r="3" fill="{color}"/>' for a, b in pts]
        legend.append(f'<span><i style="background:{color}"></i>{html.escape(label)}</span>')
    parts.append("</svg>")
    return "".join(parts) + f'<div class="legend">{"".join(legend)}</div>'


def build_html(h: dict, report_md: str, history: list[dict], updated: str) -> str:
    base, total = h["base_sek"], h["total_sek"]
    rot_stake, rot_value = _rotation_part(h)
    index_pct = h.get("index_pct") or 0.0
    index_stake = base * index_pct / 100
    spy_pct = h.get("index_sek_pct")
    cards = [
        ("S&P 500-fonden", _kr(index_stake), _pct(spy_pct), spy_pct) if index_pct else None,
        ("Rotationen (boten)", _kr(rot_stake), _pct((rot_value / rot_stake - 1) * 100 if rot_stake else None),
         (rot_value / rot_stake - 1) * 100 if rot_stake else None),
        ("Om allt låg i S&P 500", _kr(base), _kr(base * (1 + spy_pct / 100)) if spy_pct is not None else "—", spy_pct),
        ("Raketportfölj (papper, på kul)", _kr(base),
         _kr(h["rocket_paper_sek"]) if h.get("rocket_paper_sek") is not None else "inga raketer ännu",
         (h["rocket_paper_sek"] / base - 1) * 100 if h.get("rocket_paper_sek") is not None else None),
    ]
    card_html = "\n".join(
        f'<div class="card"><div class="label">{html.escape(t)}</div><div class="sub">insats {html.escape(stake)}</div>'
        f'<div class="value {_tone(v)}">{html.escape(now)}</div></div>'
        for t, stake, now, v in (c for c in cards if c)
    )
    rows = "\n".join(
        f'<tr><td>{html.escape(p["symbol"])}</td><td>{"öppen" if p["status"] == "open" else "stängd" if p["status"] == "closed" else "väntar"}</td>'
        f'<td class="{_tone(p.get("sek_return_pct"))}">{_pct(p.get("sek_return_pct"))}</td></tr>'
        for p in h.get("positions", []) if p.get("kind", "rotation") == "rotation"
    ) or '<tr><td colspan="3">Inga innehav sedan omstarten ännu.</td></tr>'
    delta_pct = h["delta_pct"]
    return f"""<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tradingbot — läget</title>
<style>
:root {{ --bg:#f6f7f9; --card:#ffffff; --text:#14171f; --muted:#5f6675; --line:#e3e6eb; --up:#0f7b3f; --down:#c0352b; --accent:#2f5bd3; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#0f1115; --card:#181b22; --text:#e8eaef; --muted:#9aa1ad; --line:#2a2f39; --up:#3fbf72; --down:#ef6a5e; --accent:#7c9dff; }} }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--text); font:16px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif; }}
main {{ max-width:880px; margin:0 auto; padding:20px 16px 48px; }}
h1 {{ font-size:1.4rem; margin:0 0 4px; }} h2 {{ font-size:1.1rem; margin:28px 0 10px; }}
.muted {{ color:var(--muted); font-size:.9rem; }}
.hero {{ background:var(--card); border:1px solid var(--line); border-radius:14px; padding:18px; margin-top:16px; }}
.big {{ font-size:2.2rem; font-weight:700; letter-spacing:-.02em; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(190px,1fr)); gap:10px; margin-top:12px; }}
.card {{ background:var(--card); border:1px solid var(--line); border-radius:12px; padding:12px 14px; }}
.label {{ font-weight:600; }} .sub {{ color:var(--muted); font-size:.85rem; }} .value {{ font-size:1.25rem; font-weight:600; margin-top:4px; }}
.up {{ color:var(--up); }} .down {{ color:var(--down); }}
.chartbox {{ background:var(--card); border:1px solid var(--line); border-radius:12px; padding:12px; }}
.chart {{ width:100%; max-width:640px; height:auto; display:block; margin:0 auto; }} .chart .grid {{ stroke:var(--line); }}
.chart .axis {{ fill:var(--muted); font-size:14px; }}
.legend {{ display:flex; flex-wrap:wrap; gap:14px; font-size:.85rem; color:var(--muted); margin-top:6px; }}
.legend i {{ display:inline-block; width:12px; height:3px; margin-right:6px; vertical-align:middle; }}
table {{ width:100%; border-collapse:collapse; background:var(--card); border:1px solid var(--line); border-radius:12px; overflow:hidden; font-size:.95rem; }}
th, td {{ text-align:left; padding:8px 10px; border-bottom:1px solid var(--line); }}
.report {{ background:var(--card); border:1px solid var(--line); border-radius:12px; padding:4px 16px 12px; overflow-x:auto; }}
.report table {{ border:0; }} .report blockquote {{ margin:8px 0; padding:6px 12px; border-left:3px solid var(--accent); color:var(--muted); }}
.note {{ margin-top:28px; color:var(--muted); font-size:.85rem; }}
</style>
</head>
<body>
<main>
<h1>📈 Tradingbot — läget</h1>
<div class="muted">Allt på papper sedan 2026-11-01. Uppdaterad {html.escape(updated)}.</div>

<div class="hero">
  <div class="muted">Hypotetiska {_kr(base)} sedan {html.escape(h["since"])}</div>
  <div class="big">{_kr(total)}</div>
  <div class="value {_tone(delta_pct)}">{"+" if h["delta_sek"] >= 0 else ""}{_kr(h["delta_sek"])} ({_pct(delta_pct)})</div>
  <div class="grid">{card_html}</div>
</div>

<h2>Utveckling sedan omstarten</h2>
<div class="chartbox">{render_chart(history)}</div>

<h2>Rotationens innehav (i kronor sedan omstarten)</h2>
<table><thead><tr><th>Aktie</th><th>Status</th><th>Resultat</th></tr></thead><tbody>
{rows}
</tbody></table>

<h2>Dagens rapport från boten</h2>
<div class="report">{render_report(report_md)}</div>

<p class="note">Inga riktiga pengar handlas — boten handlar aldrig åt dig. Siffrorna är hypotetiska och räknade på riktiga
kurser och valutakurser. Historik är ingen garanti för framtiden; varje affär kan förlora.</p>
</main>
</body>
</html>
"""


def status_payload(h: dict, report_md: str, history: list[dict], updated: str) -> dict:
    """Everything the page shows, already computed — the same numbers as the
    HTML page, as data (site/status.json) for other front ends, e.g. the
    owner's claude.ai app, which gets it copied into its database."""
    base = h["base_sek"]
    rot_stake, rot_value = _rotation_part(h)
    spy_pct = h.get("index_sek_pct")
    return {
        "updated": updated, "since": h["since"], "base_sek": base, "total_sek": h["total_sek"],
        "delta_sek": h["delta_sek"], "delta_pct": h["delta_pct"],
        "index_pct": h.get("index_pct") or 0.0, "index_sek_pct": spy_pct,
        "rotation_stake_sek": round(rot_stake, 2), "rotation_value_sek": round(rot_value, 2),
        "spy_all_sek": round(base * (1 + spy_pct / 100), 2) if spy_pct is not None else None,
        "rocket_paper_sek": h.get("rocket_paper_sek"),
        "positions": [{"symbol": p["symbol"], "kind": p.get("kind", "rotation"), "status": p["status"],
                       "sek_return_pct": p.get("sek_return_pct")} for p in h.get("positions", [])],
        "history": [{"date": p["date"], "total_sek": p["total_sek"], "spy_sek": p.get("spy_sek"),
                     "rocket_sek": p.get("rocket_sek")} for p in history],
        "report_md": report_md,
    }


def build_site(state_dir: Path, out_dir: Path, now: dt.datetime | None = None) -> Path | None:
    """Reads the run's files from `state_dir`, updates state_dir/history.json
    and writes out_dir/index.html. None when there is no tracker data yet."""
    now = now or dt.datetime.now(dt.timezone.utc)
    hyp_path = state_dir / "hypothetical.json"
    if not hyp_path.exists():
        return None
    h = json.loads(hyp_path.read_text(encoding="utf-8"))
    report_path = state_dir / "reports" / "latest.md"
    report = report_path.read_text(encoding="utf-8") if report_path.exists() else "Ingen rapport ännu."
    history_path = state_dir / "history.json"
    history = json.loads(history_path.read_text(encoding="utf-8")) if history_path.exists() else []
    history = update_history(history, h, now.strftime("%Y-%m-%d"))
    history_path.write_text(json.dumps(history, indent=1), encoding="utf-8")
    out_dir.mkdir(parents=True, exist_ok=True)
    updated = now.strftime("%Y-%m-%d %H:%M UTC")
    page = out_dir / "index.html"
    page.write_text(build_html(h, report, history, updated), encoding="utf-8")
    (out_dir / "status.json").write_text(json.dumps(status_payload(h, report, history, updated), ensure_ascii=False),
                                         encoding="utf-8")
    return page
