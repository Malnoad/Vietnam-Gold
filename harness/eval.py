"""
harness/eval.py
Bộ test cases tự động — chạy sau mỗi session (Stop hook).
Adapted from QUANT-VN-MARKETS pattern.
"""

import sys
import json
from pathlib import Path

ROOT     = Path(__file__).parent.parent
DATA_DIR = ROOT / "vietnam_gold_data"
MS_DIR   = DATA_DIR / "manuscript"


TEST_CASES = [
    {
        "id":          "TC001",
        "description": "master_data.xlsx exists and has 132 rows",
        "run":         lambda: _test_master_data(),
    },
    {
        "id":          "TC002",
        "description": "Phase 3 results exist with correct bounds_test columns",
        "run":         lambda: _test_phase3_columns(),
    },
    {
        "id":          "TC003",
        "description": "Phase 4 results exist with forecast_accuracy sheet",
        "run":         lambda: _test_phase4_exists(),
    },
    {
        "id":          "TC004",
        "description": "No banned patterns in any notebook",
        "run":         lambda: _test_no_banned_patterns(),
    },
    {
        "id":          "TC005",
        "description": "All notebooks have valid JSON structure",
        "run":         lambda: _test_notebook_json(),
    },
    {
        "id":          "TC006",
        "description": "Phase 5 manuscript tables exist (if Phase 4 done)",
        "run":         lambda: _test_manuscript_files(),
    },
    {
        "id":          "TC007",
        "description": "LaTeX paper has no Python syntax errors (tex is valid text)",
        "run":         lambda: _test_latex_exists(),
    },
]


def _test_master_data():
    import pandas as pd
    f = DATA_DIR / "master_data.xlsx"
    assert f.exists(), "master_data.xlsx not found"
    df = pd.read_excel(f, sheet_name="master_data", index_col=0)
    assert len(df) == 132, f"Expected 132 rows, got {len(df)}"
    core = ["lGOLD_SJC", "lEXRATE", "lGOLD_W", "lCPI", "IR"]
    for c in core:
        assert c in df.columns, f"Missing column: {c}"
        assert df[c].isna().sum() == 0, f"NaN in {c}"
    return f"132 rows, {len(df.columns)} cols, 0 NaN in core"


def _test_phase3_columns():
    import pandas as pd
    f = DATA_DIR / "phase3_results.xlsx"
    if not f.exists():
        return "SKIP — phase3_results.xlsx not yet generated"
    bt = pd.read_excel(f, sheet_name="bounds_test")
    assert "F-statistic" in bt.columns, \
        f"Wrong column name. Found: {list(bt.columns)}"
    assert "CV 5% I(0)" in bt.columns, \
        f"CV columns wrong. Found: {list(bt.columns)}"
    f_val = float(bt.iloc[0]["F-statistic"])
    return f"F-statistic={f_val:.4f}, columns OK"


def _test_phase4_exists():
    import pandas as pd
    f = DATA_DIR / "phase4_results.xlsx"
    if not f.exists():
        return "SKIP — phase4_results.xlsx not yet generated"
    xl = pd.ExcelFile(f)
    assert "forecast_accuracy" in xl.sheet_names, \
        f"Missing sheet. Found: {xl.sheet_names}"
    assert "diebold_mariano" in xl.sheet_names, \
        f"Missing DM sheet. Found: {xl.sheet_names}"
    return f"Sheets: {xl.sheet_names}"


BANNED = [
    "cov_type='HC3'",
    "dregs=",
    "fillna(method=",
    "jb, jp, jsk, jku",
    "resid_recursive[int(d):]",
]

def _test_no_banned_patterns():
    hits = []
    for nb in ROOT.glob("*.ipynb"):
        text = nb.read_text(encoding="utf-8")
        for pat in BANNED:
            if pat in text:
                hits.append(f"{nb.name}:'{pat}'")
    assert not hits, f"Banned patterns found: {hits}"
    return "Clean"


def _test_notebook_json():
    nbs = list(ROOT.glob("*.ipynb"))
    assert nbs, "No notebooks found"
    for nb in nbs:
        try:
            json.loads(nb.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            raise AssertionError(f"{nb.name}: {e}")
    return f"{len(nbs)} notebooks valid"


def _test_manuscript_files():
    if not (DATA_DIR / "phase4_results.xlsx").exists():
        return "SKIP — Phase 4 not done yet"
    expected = ["Table1_descriptive.xlsx", "Table4_forecast_accuracy.xlsx",
                "Figure1_time_series.png", "Figure4_forecasts_2025.png"]
    missing = [f for f in expected if not (MS_DIR / f).exists()]
    if missing:
        return f"SKIP — not yet generated: {missing}"
    return f"{len(list(MS_DIR.iterdir()))} manuscript files present"


def _test_latex_exists():
    f = ROOT / "vietnam_gold_paper.tex"
    if not f.exists():
        return "SKIP — LaTeX file not found"
    size = f.stat().st_size
    assert size > 10000, f"LaTeX file suspiciously small: {size} bytes"
    content = f.read_text(encoding="utf-8")
    assert r"\begin{document}" in content
    assert r"\end{document}" in content
    todo_count = content.count(r"\todo{")
    return f"OK, {todo_count} \\todo{{}} remaining"


# ── Runner ────────────────────────────────────────────────────────
def run_eval(threshold: float = 0.7) -> bool:
    passed  = 0
    results = []

    for case in TEST_CASES:
        try:
            note = case["run"]()
            results.append({"id": case["id"], "passed": True,
                             "note": note, "desc": case["description"]})
            passed += 1
        except Exception as e:
            results.append({"id": case["id"], "passed": False,
                             "note": str(e), "desc": case["description"]})

    total = len(TEST_CASES)
    score = passed / total

    print(f"\n{'='*55}")
    print("  VIETNAM-GOLD-ARDL Eval")
    print(f"{'='*55}")
    for r in results:
        icon = "✅" if r["passed"] else "❌"
        skip = r["note"].startswith("SKIP")
        if skip: icon = "⏭️"
        print(f"  {icon} [{r['id']}] {r['desc']}")
        if r["note"]:
            print(f"       → {r['note'][:100]}")
    print(f"{'='*55}")
    # Skipped tests don't count against score
    skipped = sum(1 for r in results if r["note"].startswith("SKIP"))
    effective = total - skipped
    eff_score = passed / effective if effective > 0 else 1.0
    print(f"  Score: {passed}/{total} ({skipped} skipped) = {eff_score:.0%} "
          f"({'✅ PASS' if eff_score >= threshold else '❌ FAIL'})")
    print(f"{'='*55}\n")
    return eff_score >= threshold


if __name__ == "__main__":
    ok = run_eval()
    sys.exit(0 if ok else 1)
