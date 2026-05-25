# Modeling the Impact of Exchange Rate Volatility on Domestic Gold Prices in Vietnam

> An ARDL Bounds Testing and ARIMA/ARIMAX Forecasting Study
> **Author:** Doan Tung Lam · ID: 11230555 · Class: DSEB65B
> **Instructor:** Tran Thi Ha

---

## Overview

This project investigates the long-run and short-run dynamics between Vietnam's domestic SJC gold price and key macroeconomic determinants over **January 2015 – December 2025** (T = 132 monthly observations). The analysis combines cointegration testing with out-of-sample forecasting to answer three questions:

1. Does a long-run cointegrating relationship exist between the SJC gold price and the USD/VND exchange rate, world gold price, CPI, and SBV refinancing rate?
2. How fast does the market correct deviations from long-run equilibrium?
3. Do ARIMAX models incorporating macro variables significantly outperform a random walk benchmark?

**Key findings:**
- Bounds F-statistic = **5.229** (p = 0.0002) → cointegration confirmed at 1%
- ECT = **−0.141** (p = 0.016) → 14.1% of disequilibrium corrected per month; half-life ≈ 4.6 months
- ARIMAX reduces MAPE by **14.9%** vs. random walk; Diebold–Mariano DM ≈ 4.04 (p = 0.002)

---

## Project Structure

```
.
├── README.md                          ← this file
├── Report.pdf                         ← compiled final report
├── vietnam_gold_paper.tex             ← LaTeX source (pdflatex + bibtex)
│
├── vietnam_gold_pipeline_final.ipynb  ← Phase 1: data ingestion & master dataset
├── vietnam_gold_phase2_unit_root.ipynb ← Phase 2: unit root & stationarity tests
├── vietnam_gold_phase3_ardl.ipynb     ← Phase 3: ARDL bounds test & ECM
├── vietnam_gold_phase4_arima.ipynb    ← Phase 4: ARIMA/ARIMAX forecasting
├── vietnam_gold_phase5_manuscript.ipynb ← Phase 5: manuscript tables & figures
│
├── vietnam_gold_data/
│   ├── master_data.xlsx               ← single source of truth (132 obs, 5 variables)
│   ├── master_data.csv                ← CSV copy
│   ├── phase2_results.xlsx            ← ADF / PP / KPSS / Zivot-Andrews results
│   ├── phase3_results.xlsx            ← ARDL bounds test, ECM coefficients
│   ├── phase4_results.xlsx            ← Forecast accuracy, Diebold-Mariano test
│   ├── correlation_heatmap.png        ← pairwise correlation matrix
│   ├── data_quality_report.txt        ← automated data validation log
│   ├── manuscript/                    ← publication-ready figures & tables
│   │   ├── Figure1_time_series.png
│   │   ├── Figure2_ACF_PACF.png
│   │   ├── Figure3_ARDL_diagnostics.png
│   │   ├── Figure3c_GARCH_volatility.png
│   │   ├── Figure4_forecasts_2025.png
│   │   ├── Table1_descriptive.xlsx
│   │   ├── Table2_unit_root.xlsx
│   │   ├── Table3_ARDL.xlsx
│   │   ├── Table4_forecast_accuracy.xlsx
│   │   └── Table5_diebold_mariano.xlsx
│   ├── phase2_plots/                  ← ACF/PACF, ARCH plots
│   ├── phase3_plots/                  ← ARDL diagnostics, GARCH volatility
│   └── phase4_plots/                  ← ARIMA diagnostics, forecast paths
│
├── core papers/                       ← reference PDFs
│   ├── s43093-021-00101-9.pdf         ← Wang et al. (2021) — safe-haven & FX risk
│   ├── Is gold an inflation hedge...  ← Do et al. (2023) — NARDL inflation hedging
│   └── 1-s2.0-S1057521923003290.pdf   ← Rana & O'Connor (2023) — cross-country ARDL
│
└── harness/
    ├── eval.py                        ← automated integrity test suite (7 test cases)
    └── check.py                       ← quick lint gate (run after every edit)
```

---

## Data

| Variable | Symbol | Source | Period |
|---|---|---|---|
| SJC gold price | ln SJC | Bảo Tín Mạnh Hải via CafeF | Jan 2015 – Dec 2025 |
| USD/VND exchange rate | ln EXRATE | Investing.com (daily avg → monthly) | Jan 2015 – Dec 2025 |
| World gold price | ln GOLD_W | COMEX GC=F via Yahoo Finance | Jan 2015 – Dec 2025 |
| Consumer Price Index | ln CPI | FRED FPCPITOTLZGVNM (World Bank) | Jan 2015 – Dec 2025 |
| SBV refinancing rate | IR | SBV official QĐ-NHNN decisions | Jan 2015 – Dec 2025 |

All price series are log-transformed. The interest rate enters in levels (% p.a.).

**Structural break dummies** included:
- `D_covid` = 1 from March 2020 (COVID-19 pandemic shock)
- `D_sbv24` = 1 from January 2024 (SBV gold market auction reform)
- `D_tet` = 1 in January & February each year (Tết seasonal cycle)

---

## Methodology

### Phase execution order

```
Phase 1  →  master_data.xlsx          (data assembly & quality check)
Phase 2  →  phase2_results.xlsx       (unit root: ADF, PP, KPSS, Zivot-Andrews)
Phase 3  →  phase3_results.xlsx       (ARDL bounds test + ECM, HAC standard errors)
Phase 4  →  phase4_results.xlsx       (ARIMA/ARIMAX order selection + DM test)
Phase 5  →  manuscript/               (publication tables & figures)
LaTeX    →  vietnam_gold_paper.tex    (final report)
```

> **Never run Phase N without Phase N-1 output present.**

### Key specifications

| Step | Specification | Criterion |
|---|---|---|
| Lag length | ARDL(1,0,1,1,0) | AIC minimisation over max lag = 2 |
| Standard errors | Newey-West HAC | BG lag-12 autocorrelation (p = 0.017) |
| Bounds test | Case III, k = 4 | Pesaran et al. (2001) |
| ARIMA | ARIMA(0,1,0) — random walk | Lowest AIC across (p,q) ∈ {0,1,2}² |
| Forecast evaluation | Diebold-Mariano + HLN correction | 12-month hold-out (2025) |

---

## Results Summary

### ARDL Bounds Test

| | |
|---|---|
| F-statistic | **5.229** (p = 0.0002) |
| 1% critical bounds I(0)/I(1) | 3.74 / 5.06 |
| Verdict | **Cointegration confirmed at 1%** |
| ECT | −0.141 (p = 0.016) → half-life **4.6 months** |

### Short-run ECM (selected coefficients)

| Variable | Coefficient | p-value |
|---|---|---|
| Δln EXRATE_t | +1.039 | 0.010 ** |
| Δln GOLD_W,t | +0.504 | < 0.001 *** |
| Δln GOLD_W,t−1 | +0.345 | 0.001 *** |
| Δln CPI_t | +20.059 | 0.024 ** |
| Δln CPI_t−1 | −23.361 | 0.004 *** |
| ΔIR_t | +0.026 | 0.016 ** |

### Forecast Accuracy (hold-out: Jan–Dec 2025)

| Model | RMSE (log) | MAPE (%) | MAPE (VND%) |
|---|---|---|---|
| ARIMA(0,1,0) — baseline | 0.387 | 1.82 | 27.62 |
| ARIMAX-EX | 0.331 | 1.55 | 24.23 |
| ARIMAX-GW | 0.331 | 1.55 | 24.24 |
| **ARIMAX-BOTH** | **0.331** | **1.55** | **24.22** |

All ARIMAX models: DM ≈ 4.04, p = 0.002 → reject equal accuracy at **1%**

---

## Reproducing the Analysis

### Requirements

```
Python 3.10+
pandas, numpy, statsmodels==0.14.5
scipy, arch, matplotlib, openpyxl
jupyter
```

Install all dependencies:

```bash
pip install pandas numpy "statsmodels==0.14.5" scipy arch matplotlib openpyxl jupyter
```

### Run notebooks in order

```bash
jupyter nbconvert --to notebook --execute vietnam_gold_pipeline_final.ipynb
jupyter nbconvert --to notebook --execute vietnam_gold_phase2_unit_root.ipynb
jupyter nbconvert --to notebook --execute vietnam_gold_phase3_ardl.ipynb
jupyter nbconvert --to notebook --execute vietnam_gold_phase4_arima.ipynb
jupyter nbconvert --to notebook --execute vietnam_gold_phase5_manuscript.ipynb
```

> Always use **Kernel → Restart & Run All** in Jupyter, never re-run individual cells.

### Run integrity tests

```bash
python harness/eval.py        # full test suite (7 test cases)
python harness/check.py --quick  # quick lint gate
```

### Compile the LaTeX report

```bash
pdflatex vietnam_gold_paper.tex
bibtex vietnam_gold_paper
pdflatex vietnam_gold_paper.tex
pdflatex vietnam_gold_paper.tex
```

---

## Important Notes

- `statsmodels 0.14.5` requires `cov_kwds={'maxlags': None, 'use_correction': True}` when using `cov_type='HAC'` — this is already applied in Phase 3.
- `NEVER` substitute `cov_type='HC3'` for `'HAC'` — this violates the HAC disclosure requirement and changes the F-statistic.
- The 2025 SJC price data for some months are estimates. Replace with actuals from CafeF before final submission.

---

## References

| Citation | Paper |
|---|---|
| Wang et al. (2021) | Is gold a safe haven for the dynamic risk of foreign exchange? *Future Business Journal* 7(1):56 |
| Do et al. (2023) | Is gold an inflation hedge in Vietnam? A non-linear approach. *Cogent Economics & Finance* 11(2):2244857 |
| Rana & O'Connor (2023) | Domestic macroeconomic determinants of precious metals prices. *International Review of Financial Analysis* 89:102813 |
| Pesaran et al. (2001) | Bounds testing approaches to the analysis of level relationships. *Journal of Applied Econometrics* 16(3):289–326 |
| Diebold & Mariano (1995) | Comparing predictive accuracy. *Journal of Business & Economic Statistics* 13(3):253–263 |

---

*Submitted for DSEB65B · Instructor: Tran Thi Ha*
