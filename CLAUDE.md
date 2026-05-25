# VIETNAM-GOLD-ARDL — Harness Root

## 📍 Entry point
Invoke `claude` from this directory. All paths are relative to this root.

## 🎯 Mission
Nghiên cứu tác động tỷ giá đến giá vàng SJC — ARDL bounds test + ARIMA/ARIMAX.
Target: JABES Q1 / Cogent Economics Q2 / Resources Policy Q1.

## 📁 Navigation map
```
CLAUDE.md                          ← you are here (overview only)
├── vietnam_gold_data/CLAUDE.md    ← data contracts, column names, variable specs
├── harness/CLAUDE.md              ← tool contracts, check gates, known bugs
├── skills/phase3_ardl.md          ← loaded ON DEMAND for ARDL work
├── skills/phase4_arima.md         ← loaded ON DEMAND for ARIMA work
├── skills/latex_paper.md          ← loaded ON DEMAND for LaTeX edits
└── .claude/settings.json          ← hooks + permissions
```

## 🔄 Phase execution order — STRICT
```
Phase 1 → master_data.xlsx
Phase 2 → phase2_results.xlsx
Phase 3 → phase3_results.xlsx   (needs phase2_results.xlsx)
Phase 4 → phase4_results.xlsx   (needs phase3_results.xlsx)
Phase 5 → manuscript/            (needs phase4_results.xlsx)
LaTeX   → vietnam_gold_paper.tex (needs manuscript/)
```
Never run Phase N without Phase N-1 output present.

## ⚡ Commands
```bash
python harness/check.py --quick          # lint gate (run after any edit)
python harness/eval.py                   # full notebook integrity test
jupyter nbconvert --to notebook --execute vietnam_gold_phase3_ardl.ipynb
# Always: Kernel → Restart & Run All — never re-run single cells
```

## ⛔ HARD RULES (violations break everything)
- NEVER use `cov_type='HC3'` → always `'HAC'`
- NEVER pass `dregs=` to `build_ardl_regressors` — it has no such argument
- NEVER `fillna(method='ffill')` → use `.ffill()`
- NEVER unpack `scipy.jarque_bera` as 4-tuple — it returns 2
- NEVER patch the output file — only patch the file user uploads
- NEVER re-run a single cell after a fix — Restart & Run All

## 📝 Three mandatory paper disclosures
1. HAC SE: "Newey-West HAC standard errors used throughout (BG lag-12 p=0.017)."
2. Bounds: "F=2.627 inconclusive at 10%; ECT=−0.141 (p=0.030) confirms cointegration tendency."
3. IGARCH: "GARCH(1,1) reveals α+β=1.0; OLS estimates remain consistent."
