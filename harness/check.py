"""
harness/check.py
Gate tự động — chạy sau mỗi lần Claude Code sửa file notebook.
Adapted from QUANT-VN-MARKETS pattern.
"""

import sys
import json
import subprocess
import argparse
from pathlib import Path

ROOT      = Path(__file__).parent.parent
DATA_DIR  = ROOT / "vietnam_gold_data"

# ── Quick checks: JSON validity of all notebooks ──────────────────
def check_notebooks() -> tuple[bool, str]:
    notebooks = list(ROOT.glob("*.ipynb"))
    if not notebooks:
        return True, "No notebooks found"
    for nb_path in notebooks:
        try:
            json.loads(nb_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            return False, f"{nb_path.name}: invalid JSON — {e}"
    return True, f"{len(notebooks)} notebooks valid"


# ── Check no deprecated patterns in notebooks ─────────────────────
BANNED_PATTERNS = [
    ("cov_type='HC3'",           "Use HAC not HC3"),
    ("dregs=",                   "build_ardl_regressors has no dregs arg"),
    ("fillna(method=",           "Use .ffill() instead"),
    ("jb, jp, jsk, jku",         "scipy.jarque_bera returns 2-tuple not 4"),
    ("resid_recursive[int(d):]", "Use .dropna() not int(d) slice"),
]

def check_patterns() -> tuple[bool, str]:
    issues = []
    for nb_path in ROOT.glob("*.ipynb"):
        content = nb_path.read_text(encoding="utf-8")
        for pattern, msg in BANNED_PATTERNS:
            if pattern in content:
                issues.append(f"{nb_path.name}: '{pattern}' — {msg}")
    if issues:
        return False, "\n     ".join(issues)
    return True, "No banned patterns found"


# ── Full check: result files exist ────────────────────────────────
def check_result_files() -> tuple[bool, str]:
    required = [
        DATA_DIR / "master_data.xlsx",
    ]
    missing = [str(f) for f in required if not f.exists()]
    if missing:
        return False, f"Missing: {missing}"
    return True, "Core data files present"


QUICK_CHECKS = [
    ("Notebook JSON",    check_notebooks),
    ("Banned patterns",  check_patterns),
]

FULL_CHECKS = QUICK_CHECKS + [
    ("Result files",     check_result_files),
]


def run(checks) -> bool:
    failed = []
    for name, fn in checks:
        ok, msg = fn()
        icon = "✅" if ok else "❌"
        print(f"  {icon} {name}: {msg}")
        if not ok:
            failed.append(name)
    print()
    if failed:
        print(f"⛔ Harness blocked — failed: {', '.join(failed)}\n")
        return False
    print("✅ All checks passed.\n")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true", help="JSON + pattern check only")
    args = parser.parse_args()

    print("\n🔍 VIETNAM-GOLD-ARDL Harness Check")
    print("─" * 40)
    ok = run(QUICK_CHECKS if args.quick else FULL_CHECKS)
    sys.exit(0 if ok else 1)
