const API = "";

function el(tag, cls, html) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (html !== undefined) e.innerHTML = html;
  return e;
}

function fmt(n, digits = 2) {
  if (n === null || n === undefined || Number.isNaN(n)) return "—";
  return Number(n).toFixed(digits);
}

function pct(n, digits = 2) {
  if (n === null || n === undefined || Number.isNaN(n)) return "—";
  return `${(Number(n) * 100).toFixed(digits)}%`;
}

/* ---------------- tabs ---------------- */
document.querySelectorAll(".tab-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
    document.querySelectorAll(".panel").forEach((p) => p.classList.remove("active"));
    btn.classList.add("active");
    document.getElementById(`panel-${btn.dataset.tab}`).classList.add("active");
    if (btn.dataset.tab === "journal") loadJournal();
    if (btn.dataset.tab === "performance") loadPerformance();
    if (btn.dataset.tab === "backtest") loadBacktestRuns();
    if (btn.dataset.tab === "settings") loadSettings();
  });
});

/* ---------------- config / header badges ---------------- */
let CONFIG = null;

async function loadConfig() {
  const res = await fetch(`${API}/api/config`);
  CONFIG = await res.json();
  const newsBadge = document.getElementById("news-badge");
  newsBadge.innerHTML = CONFIG.news_configured
    ? `<span class="badge-dot dot-green"></span>NEWS: CONNECTED`
    : `<span class="badge-dot dot-amber"></span>NEWS: NOT CONFIGURED`;

  const sel = document.getElementById("bt-symbol");
  sel.innerHTML = "";
  CONFIG.watchlist.forEach((sym) => {
    const opt = el("option");
    opt.value = sym;
    opt.textContent = sym;
    sel.appendChild(opt);
  });
}

function setRiskBadge(riskLabel) {
  const badge = document.getElementById("risk-badge");
  const dotClass = riskLabel === "RISK_ON" ? "dot-green" : riskLabel === "RISK_OFF" ? "dot-red" : "dot-gray";
  badge.innerHTML = `<span class="badge-dot ${dotClass}"></span>MARKET: ${riskLabel || "—"}`;
}

/* ---------------- scanner ---------------- */
const btnScan = document.getElementById("btn-scan");
const btnPaperUpdate = document.getElementById("btn-paper-update");
const resultsDiv = document.getElementById("scanner-results");
const scanMeta = document.getElementById("scan-meta");

btnScan.addEventListener("click", runScan);
btnPaperUpdate.addEventListener("click", async () => {
  btnPaperUpdate.disabled = true;
  btnPaperUpdate.innerHTML = `<span class="spinner"></span>Updating…`;
  try {
    const res = await fetch(`${API}/api/paper-trading/update`, { method: "POST" });
    const data = await res.json();
    scanMeta.textContent = `Paper trading: checked ${data.checked}, updated ${data.updated.length}, ${data.still_open_or_unavailable.length} unavailable/still open.`;
  } catch (e) {
    scanMeta.textContent = `Paper trading update failed: ${e}`;
  }
  btnPaperUpdate.disabled = false;
  btnPaperUpdate.innerHTML = `Update Paper Trades`;
});

async function runScan() {
  btnScan.disabled = true;
  btnScan.innerHTML = `<span class="spinner"></span>Scanning…`;
  resultsDiv.innerHTML = "";
  try {
    const res = await fetch(`${API}/api/scan`, { method: "POST" });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      renderScanError(err.detail || "Scan failed");
      return;
    }
    const data = await res.json();
    setRiskBadge(data.market_wide_risk);
    scanMeta.textContent = `Last scan: ${new Date(data.scanned_at).toLocaleString()} · ${data.watchlist.length} symbols watched`;
    renderScanResults(data);
  } catch (e) {
    renderScanError(String(e));
  } finally {
    btnScan.disabled = false;
    btnScan.innerHTML = `Run Scan`;
  }
}

function renderScanError(message) {
  resultsDiv.innerHTML = "";
  const box = el(
    "div",
    "empty-banner",
    `<div class="headline">Scan could not complete</div><div>${message}</div>`
  );
  resultsDiv.appendChild(box);
}

function tierClass(tier) {
  return `tier-${tier.toLowerCase()}`;
}

function breakdownRow(label, value, max) {
  const wrap = el("div", "breakdown-row");
  wrap.appendChild(el("div", "breakdown-label", label));
  const track = el("div", "breakdown-track");
  const fill = el("div", "breakdown-fill");
  fill.style.width = `${Math.max(0, Math.min(100, (value / max) * 100))}%`;
  track.appendChild(fill);
  wrap.appendChild(track);
  wrap.appendChild(el("div", "breakdown-value", `${fmt(value, 1)}/${fmt(max, 0)}`));
  return wrap;
}

function renderSignalCard(signal) {
  const card = el("div", "signal-card");

  const header = el("div", "signal-card-header");
  const left = el("div");
  left.appendChild(el("div", "signal-symbol", signal.symbol));
  left.appendChild(el("div", "signal-strategy", signal.strategy));
  header.appendChild(left);
  const right = el("div", null);
  right.style.textAlign = "right";
  right.appendChild(el("div", `direction-tag direction-${signal.direction.toLowerCase()}`, signal.direction));
  header.appendChild(right);
  card.appendChild(header);

  const scoreBlock = el("div", "score-block");
  scoreBlock.appendChild(el("div", "score-number", fmt(signal.score, 0)));
  scoreBlock.appendChild(el("div", `tier-pill ${tierClass(signal.tier)}`, signal.tier.replace("_", " ")));
  card.appendChild(scoreBlock);

  const levels = el("div", "levels-row");
  [
    ["Entry", signal.entry], ["Target", signal.target], ["Stop", signal.stop],
  ].forEach(([label, value]) => {
    const box = el("div", "level-box");
    box.appendChild(el("div", "level-label", label));
    box.appendChild(el("div", "level-value", fmt(value, value < 1 ? 6 : 4)));
    levels.appendChild(box);
  });
  card.appendChild(levels);

  const rr = el("div", "rr-row");
  rr.innerHTML = `<span>Potential: <b style="color:var(--green)">+${fmt(signal.reward_pct)}%</b></span>` +
    `<span>Risk: <b style="color:var(--red)">-${fmt(signal.risk_pct)}%</b></span>` +
    `<span>R/R: <b>${fmt(signal.rr_ratio)}</b></span>`;
  card.appendChild(rr);

  const breakdown = el("div", "breakdown-bars");
  const b = signal.breakdown;
  breakdown.appendChild(breakdownRow("Momentum", b.momentum, b.momentum_max));
  breakdown.appendChild(breakdownRow("Volume", b.volume, b.volume_max));
  breakdown.appendChild(breakdownRow("Structure", b.structure, b.structure_max));
  breakdown.appendChild(breakdownRow("Regime", b.regime, b.regime_max));
  breakdown.appendChild(breakdownRow("Catalyst", b.catalyst, b.catalyst_max));
  breakdown.appendChild(breakdownRow("Risk/Reward", b.risk_reward, b.risk_reward_max));
  card.appendChild(breakdown);

  const reasons = el("ul", "reasons-list");
  signal.reasons.forEach((r) => reasons.appendChild(el("li", null, r)));
  card.appendChild(reasons);

  if (signal.warning) {
    card.appendChild(el("div", "warning-box", `⚠ ${signal.warning}`));
  }

  if (signal.position_size) {
    const ps = signal.position_size;
    const box = el("div", "hist-prob-box");
    box.innerHTML = `<b>Suggested size:</b> $${fmt(ps.position_size_usd, 2)} (~${fmt(ps.units, 6)} units) — ` +
      `${fmt(ps.position_pct_of_portfolio, 1)}% of portfolio, risking $${fmt(ps.risk_amount_usd, 2)}`;
    card.appendChild(box);
  }

  const invalidation = el("div", "invalidation-box");
  invalidation.innerHTML = `<b>Invalidation:</b> ${fmt(signal.invalidation, 4)} — ${signal.invalidation_reason}<br/><b>Regime:</b> ${signal.regime_label}`;
  card.appendChild(invalidation);

  if (signal.historical_probability) {
    const hp = signal.historical_probability;
    const box = el("div", "hist-prob-box");
    box.innerHTML = `<b>Backtest:</b> ${hp.similar_setups} similar setups · target hit ${pct(hp.target_hit_rate)} · avg return ${fmt(hp.average_return_pct)}%`;
    card.appendChild(box);
  } else {
    card.appendChild(el("div", "hist-prob-box", "No historical backtest on file for this strategy/symbol yet — run one in the Backtest tab."));
  }

  return card;
}

function renderScanResults(data) {
  resultsDiv.innerHTML = "";

  if (!data.signals.length) {
    const banner = el(
      "div",
      "empty-banner",
      `<div class="headline">NO HIGH-CONVICTION SETUPS TODAY</div><div>No candidate cleared the quality filter (score ≥ ${CONFIG ? CONFIG.score_watch_min : 70}/100) this scan. That is a correct, honest result — not every scan should produce a trade.</div>`
    );
    resultsDiv.appendChild(banner);
  } else {
    const grid = el("div", "signal-grid");
    data.signals.forEach((s) => grid.appendChild(renderSignalCard(s)));
    resultsDiv.appendChild(grid);
  }

  const details = el("details", "data-note");
  const summary = el("summary", null, `Scan diagnostics — ${data.skipped.length} symbol(s) skipped, ${data.no_trade_summary.length} evaluated with no qualifying setup`);
  details.appendChild(summary);
  const list = el("ul");
  data.skipped.forEach((s) => list.appendChild(el("li", null, `<b>${s.symbol}</b>: ${s.reason}`)));
  data.no_trade_summary.forEach((s) => list.appendChild(el("li", null, `<b>${s.symbol}</b>: ${s.reason} (regime: ${s.regime})`)));
  if (!data.skipped.length && !data.no_trade_summary.length) {
    list.appendChild(el("li", null, "Nothing to report."));
  }
  details.appendChild(list);
  resultsDiv.appendChild(details);
}

/* ---------------- journal ---------------- */
async function loadJournal() {
  const res = await fetch(`${API}/api/journal`);
  const data = await res.json();
  const tbody = document.querySelector("#journal-table tbody");
  tbody.innerHTML = "";
  if (!data.entries.length) {
    const tr = el("tr");
    const td = el("td", null, "No journal entries yet — run a scan to generate signals.");
    td.colSpan = 13;
    tr.appendChild(td);
    tbody.appendChild(tr);
    return;
  }
  data.entries.forEach((r) => {
    const tr = el("tr");
    [
      new Date(r.timestamp).toLocaleString(), r.symbol, r.direction, r.strategy,
      fmt(r.entry, 4), fmt(r.target, 4), fmt(r.stop, 4), fmt(r.score, 0), r.market_regime,
      r.result, fmt(r.max_favorable_excursion), fmt(r.max_adverse_excursion),
      r.holding_time_minutes ? `${fmt(r.holding_time_minutes, 0)}m` : "—",
    ].forEach((v) => tr.appendChild(el("td", null, v)));
    tbody.appendChild(tr);
  });
}
document.getElementById("btn-refresh-journal").addEventListener("click", loadJournal);

/* ---------------- performance ---------------- */
async function loadPerformance() {
  const res = await fetch(`${API}/api/performance`);
  const data = await res.json();
  const container = document.getElementById("performance-content");
  container.innerHTML = "";
  renderEquityCurve();

  if (data.note) {
    container.appendChild(el("div", "empty-banner", `<div class="headline">No performance data yet</div><div>${data.note}</div>`));
    return;
  }

  const kpis = el("div", "kpi-grid");
  const addKpi = (label, value, cls) => {
    const card = el("div", "kpi-card");
    card.appendChild(el("div", "kpi-label", label));
    card.appendChild(el("div", `kpi-value ${cls || ""}`, value));
    kpis.appendChild(card);
  };
  addKpi("Signals Closed", data.closed_total);
  addKpi("Wins", data.wins, "positive");
  addKpi("Losses", data.losses, "negative");
  addKpi("Win Rate", pct(data.win_rate));
  addKpi("Avg Return", `${fmt(data.average_return_pct)}%`, data.average_return_pct >= 0 ? "positive" : "negative");
  addKpi("Expectancy", `${fmt(data.expectancy_pct)}%`, data.expectancy_pct >= 0 ? "positive" : "negative");
  addKpi("Profit Factor", fmt(data.profit_factor));
  addKpi("Max Drawdown", `${fmt(data.max_drawdown_pct)}%`, "negative");
  container.appendChild(kpis);

  container.appendChild(renderBreakdownTable("By Market Regime", data.by_regime));
  container.appendChild(renderBreakdownTable("By Strategy", data.by_strategy));
}

function renderBreakdownTable(title, breakdown) {
  const block = el("section", "block");
  block.appendChild(el("h2", "section-title", title));
  const keys = Object.keys(breakdown);
  if (!keys.length) {
    block.appendChild(el("div", "toast", "No data yet."));
    return block;
  }
  const wrap = el("div", "table-wrap");
  const table = el("table", "data-table");
  table.innerHTML = "<thead><tr><th>Segment</th><th>Count</th><th>Wins</th><th>Win Rate</th></tr></thead>";
  const tbody = el("tbody");
  keys.forEach((k) => {
    const v = breakdown[k];
    const tr = el("tr");
    [k, v.count, v.wins, pct(v.win_rate)].forEach((val) => tr.appendChild(el("td", null, val)));
    tbody.appendChild(tr);
  });
  table.appendChild(tbody);
  wrap.appendChild(table);
  block.appendChild(wrap);
  return block;
}
document.getElementById("btn-refresh-performance").addEventListener("click", loadPerformance);

/* ---------------- backtest ---------------- */
document.getElementById("btn-run-backtest").addEventListener("click", runBacktest);

async function runBacktest() {
  const symbol = document.getElementById("bt-symbol").value;
  const strategy = document.getElementById("bt-strategy").value;
  const interval = document.getElementById("bt-interval").value;
  const limit = document.getElementById("bt-limit").value;
  const btn = document.getElementById("btn-run-backtest");
  const container = document.getElementById("backtest-results");
  btn.disabled = true;
  btn.innerHTML = `<span class="spinner"></span>Running…`;
  container.innerHTML = "";
  try {
    const res = await fetch(`${API}/api/backtest/run?symbol=${symbol}&strategy=${strategy}&interval=${interval}&limit=${limit}`, { method: "POST" });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      container.appendChild(el("div", "empty-banner", `<div class="headline">Backtest failed</div><div>${err.detail}</div>`));
      return;
    }
    const data = await res.json();
    renderBacktestResult(data);
    loadBacktestRuns();
  } catch (e) {
    container.appendChild(el("div", "empty-banner", `<div class="headline">Backtest failed</div><div>${e}</div>`));
  } finally {
    btn.disabled = false;
    btn.innerHTML = "Run Backtest";
  }
}

function metricsList(m) {
  const dl = el("dl");
  const rows = [
    ["Trades", m.num_trades], ["Win Rate", pct(m.win_rate)],
    ["Avg Win", `${fmt(m.average_win_pct)}%`], ["Avg Loss", `${fmt(m.average_loss_pct)}%`],
    ["Expectancy", `${fmt(m.expectancy_pct)}%`], ["Profit Factor", fmt(m.profit_factor)],
    ["Max Drawdown", `${fmt(m.max_drawdown_pct)}%`], ["Sharpe (per trade)", fmt(m.sharpe_per_trade)],
    ["Avg Holding", m.average_holding_minutes ? `${fmt(m.average_holding_minutes, 0)}m` : "—"],
    ["Return After Costs", `${fmt(m.return_after_costs_pct)}%`],
    ["Classification", m.classification],
  ];
  rows.forEach(([label, value]) => {
    dl.appendChild(el("dt", null, label));
    dl.appendChild(el("dd", null, value));
  });
  return dl;
}

function renderBacktestResult(data) {
  const container = document.getElementById("backtest-results");
  container.innerHTML = "";

  container.appendChild(
    el(
      "div",
      "data-note",
      `<b>${data.symbol}</b> · ${data.strategy} · ${data.interval} · ${data.bars_analyzed} bars (${data.period.start} → ${data.period.end}) · fees ${data.fees_slippage.fee_bps}bps + slippage ${data.fees_slippage.slippage_bps}bps applied to every fill`
    )
  );

  const verdict = el(
    "div",
    `verdict-banner ${data.split.reliable ? "verdict-reliable" : "verdict-unreliable"}`,
    `<b>${data.split.reliable ? "RELIABLE" : "FLAGGED AS UNRELIABLE"}</b> — ${data.split.reliability_reason}`
  );
  container.appendChild(verdict);

  const splitGrid = el("div", "split-grid");
  [["Overall", data.overall], ["Train", data.split.train], ["Validation", data.split.validation], ["Out-of-Sample", data.split.out_of_sample]].forEach(
    ([label, m]) => {
      const card = el("div", "split-card");
      card.appendChild(el("h3", null, label));
      card.appendChild(metricsList(m));
      splitGrid.appendChild(card);
    }
  );
  container.appendChild(splitGrid);

  const wfBlock = el("section", "block");
  wfBlock.appendChild(el("h2", "section-title", "Walk-Forward Windows"));
  wfBlock.appendChild(
    el(
      "div",
      `verdict-banner ${data.walk_forward.consistent ? "verdict-reliable" : "verdict-unreliable"}`,
      data.walk_forward.consistency_reason
    )
  );
  if (data.walk_forward.windows.length) {
    const wrap = el("div", "table-wrap");
    const table = el("table", "data-table");
    table.innerHTML = "<thead><tr><th>Window</th><th>Period</th><th>Trades</th><th>Win Rate</th><th>Expectancy</th><th>Classification</th></tr></thead>";
    const tbody = el("tbody");
    data.walk_forward.windows.forEach((w) => {
      const tr = el("tr");
      [
        w.window_index, `${new Date(w.start).toLocaleDateString()} → ${new Date(w.end).toLocaleDateString()}`,
        w.metrics.num_trades, pct(w.metrics.win_rate), `${fmt(w.metrics.expectancy_pct)}%`, w.metrics.classification,
      ].forEach((v) => tr.appendChild(el("td", null, v)));
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    wrap.appendChild(table);
    wfBlock.appendChild(wrap);
  }
  container.appendChild(wfBlock);
}

async function loadBacktestRuns() {
  const res = await fetch(`${API}/api/backtest/runs`);
  const data = await res.json();
  const tbody = document.querySelector("#backtest-runs-table tbody");
  tbody.innerHTML = "";
  if (!data.runs.length) {
    const tr = el("tr");
    const td = el("td", null, "No saved backtest runs yet.");
    td.colSpan = 6;
    tr.appendChild(td);
    tbody.appendChild(tr);
    return;
  }
  data.runs.forEach((r) => {
    const tr = el("tr");
    [
      new Date(r.created_at).toLocaleString(), r.symbol, r.strategy, r.interval,
      `${new Date(r.start).toLocaleDateString()} → ${new Date(r.end).toLocaleDateString()}`,
      r.reliable ? "✅ yes" : "❌ no",
    ].forEach((v) => tr.appendChild(el("td", null, v)));
    tbody.appendChild(tr);
  });
}

/* ---------------- equity curve ---------------- */
async function renderEquityCurve() {
  const container = document.getElementById("equity-curve-container");
  container.innerHTML = "";
  const res = await fetch(`${API}/api/performance/equity-curve`);
  const data = await res.json();
  const points = data.points || [];

  if (points.length < 2) {
    container.appendChild(
      el("div", "chart-empty", points.length === 0
        ? "No closed signals yet — the curve appears once paper trading or a backtest has real outcomes to plot."
        : "Only one closed signal so far — need at least two points to draw a curve.")
    );
    return;
  }

  const W = 900, H = 220, PAD_L = 46, PAD_R = 16, PAD_T = 16, PAD_B = 28;
  const values = points.map((p) => p.cumulative_return_pct);
  const minV = Math.min(0, ...values);
  const maxV = Math.max(0, ...values);
  const range = maxV - minV || 1;

  const x = (i) => PAD_L + (i / (points.length - 1)) * (W - PAD_L - PAD_R);
  const y = (v) => PAD_T + (1 - (v - minV) / range) * (H - PAD_T - PAD_B);

  const pathD = points.map((p, i) => `${i === 0 ? "M" : "L"}${x(i).toFixed(1)},${y(p.cumulative_return_pct).toFixed(1)}`).join(" ");
  const zeroY = y(0);
  const finalValue = values[values.length - 1];
  const lineColor = finalValue >= 0 ? "var(--green)" : "var(--red)";
  const dotColor = (r) => (r.result === "TARGET_HIT" ? "var(--green)" : r.result === "STOP_HIT" ? "var(--red)" : "var(--text-faint)");

  const svgNS = "http://www.w3.org/2000/svg";
  const svg = document.createElementNS(svgNS, "svg");
  svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
  svg.style.width = "100%";
  svg.style.height = "auto";
  svg.style.overflow = "visible";

  const zeroLine = document.createElementNS(svgNS, "line");
  zeroLine.setAttribute("x1", PAD_L); zeroLine.setAttribute("x2", W - PAD_R);
  zeroLine.setAttribute("y1", zeroY); zeroLine.setAttribute("y2", zeroY);
  zeroLine.setAttribute("stroke", "var(--border)"); zeroLine.setAttribute("stroke-dasharray", "4 4");
  svg.appendChild(zeroLine);

  [minV, 0, maxV].forEach((v) => {
    const label = document.createElementNS(svgNS, "text");
    label.setAttribute("x", 4); label.setAttribute("y", y(v) + 4);
    label.setAttribute("font-size", "10"); label.setAttribute("fill", "var(--text-faint)");
    label.setAttribute("font-family", "var(--mono)");
    label.textContent = `${v.toFixed(1)}%`;
    svg.appendChild(label);
  });

  const path = document.createElementNS(svgNS, "path");
  path.setAttribute("d", pathD);
  path.setAttribute("fill", "none");
  path.setAttribute("stroke", lineColor);
  path.setAttribute("stroke-width", "2");
  svg.appendChild(path);

  points.forEach((p, i) => {
    const c = document.createElementNS(svgNS, "circle");
    c.setAttribute("cx", x(i)); c.setAttribute("cy", y(p.cumulative_return_pct));
    c.setAttribute("r", "3.5"); c.setAttribute("fill", dotColor(p));
    const title = document.createElementNS(svgNS, "title");
    title.textContent = `${p.symbol} · ${p.strategy} · ${p.result} (${p.trade_return_pct > 0 ? "+" : ""}${p.trade_return_pct}%) · cumulative ${p.cumulative_return_pct}%` +
      (p.closed_at ? ` · ${new Date(p.closed_at).toLocaleString()}` : "");
    c.appendChild(title);
    svg.appendChild(c);
  });

  container.appendChild(svg);
  const summary = el(
    "div", "toast",
    `${points.length} closed signals · cumulative return ${finalValue >= 0 ? "+" : ""}${finalValue.toFixed(2)}% (sum of independent per-trade % returns, not compounded)`
  );
  summary.style.marginTop = "8px";
  container.appendChild(summary);
}

/* ---------------- settings ---------------- */
const DAY_CODES = [["mon", "Mon"], ["tue", "Tue"], ["wed", "Wed"], ["thu", "Thu"], ["fri", "Fri"], ["sat", "Sat"], ["sun", "Sun"]];
let selectedDays = new Set(DAY_CODES.map(([c]) => c));

function renderDayToggles() {
  const wrap = document.getElementById("set-hours-days");
  wrap.innerHTML = "";
  DAY_CODES.forEach(([code, label]) => {
    const btn = el("div", `day-toggle${selectedDays.has(code) ? " active" : ""}`, label);
    btn.addEventListener("click", () => {
      if (selectedDays.has(code)) selectedDays.delete(code); else selectedDays.add(code);
      renderDayToggles();
    });
    wrap.appendChild(btn);
  });
}

async function loadSettings() {
  const res = await fetch(`${API}/api/settings`);
  const s = await res.json();

  document.getElementById("set-telegram-token").value = s.telegram_bot_token || "";
  document.getElementById("set-telegram-chat").value = s.telegram_chat_id || "";
  document.getElementById("set-notify-min-score").value = s.notify_min_score;
  document.getElementById("set-watchlist").value = (s.watchlist || []).join(",");
  document.getElementById("set-score-watch").value = s.score_watch_min;
  document.getElementById("set-score-hq").value = s.score_high_quality_min;
  document.getElementById("set-score-exceptional").value = s.score_exceptional_min;
  document.getElementById("set-scheduler-enabled").checked = !!s.enable_scheduler;
  document.getElementById("set-scan-loop").value = s.scan_loop_minutes;
  document.getElementById("set-monitor-loop").value = s.monitor_loop_minutes;
  document.getElementById("set-hours-enabled").checked = !!s.trading_hours_enabled;
  document.getElementById("set-hours-start").value = s.trading_hours_start;
  document.getElementById("set-hours-end").value = s.trading_hours_end;
  document.getElementById("set-hours-tz").value = s.trading_hours_timezone;
  document.getElementById("set-portfolio-size").value = s.portfolio_size_usd;
  document.getElementById("set-risk-per-trade").value = s.risk_per_trade_pct;

  selectedDays = new Set(s.trading_days || []);
  renderDayToggles();
}

async function saveSettings() {
  const btn = document.getElementById("btn-save-settings");
  const note = document.getElementById("settings-saved-note");
  btn.disabled = true;
  btn.innerHTML = `<span class="spinner"></span>Saving…`;

  const payload = {
    telegram_bot_token: document.getElementById("set-telegram-token").value.trim() || null,
    telegram_chat_id: document.getElementById("set-telegram-chat").value.trim() || null,
    notify_min_score: Number(document.getElementById("set-notify-min-score").value),
    watchlist: document.getElementById("set-watchlist").value.split(",").map((s) => s.trim()).filter(Boolean),
    score_watch_min: Number(document.getElementById("set-score-watch").value),
    score_high_quality_min: Number(document.getElementById("set-score-hq").value),
    score_exceptional_min: Number(document.getElementById("set-score-exceptional").value),
    enable_scheduler: document.getElementById("set-scheduler-enabled").checked,
    scan_loop_minutes: Number(document.getElementById("set-scan-loop").value),
    monitor_loop_minutes: Number(document.getElementById("set-monitor-loop").value),
    trading_hours_enabled: document.getElementById("set-hours-enabled").checked,
    trading_hours_start: document.getElementById("set-hours-start").value,
    trading_hours_end: document.getElementById("set-hours-end").value,
    trading_hours_timezone: document.getElementById("set-hours-tz").value.trim(),
    trading_days: Array.from(selectedDays),
    portfolio_size_usd: Number(document.getElementById("set-portfolio-size").value),
    risk_per_trade_pct: Number(document.getElementById("set-risk-per-trade").value),
  };

  try {
    const res = await fetch(`${API}/api/settings`, {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      note.textContent = `Failed: ${err.detail}`;
      note.style.color = "var(--red)";
    } else {
      note.textContent = "Saved — takes effect immediately (scheduler changes within ~60s).";
      note.style.color = "var(--green)";
      loadConfig();
    }
  } catch (e) {
    note.textContent = `Failed: ${e}`;
    note.style.color = "var(--red)";
  } finally {
    btn.disabled = false;
    btn.innerHTML = "Save Settings";
    setTimeout(() => { note.textContent = ""; }, 6000);
  }
}
document.getElementById("btn-save-settings").addEventListener("click", saveSettings);

/* ---------------- init ---------------- */
loadConfig();
