"""Compare Pylint results for a rough draft and a refactored model."""

import os
import subprocess
import sys
import tempfile
from importlib.util import find_spec
from pathlib import Path


UNFORMATTED_CODE = """
import math, os, sys
from typing import List,Tuple
class Quantized1DTCNModel:
 def predict_level(self,angles:List[float],speeds:List[float])->int:
  reversals=0
  for i in range(1,len(angles)):
   if abs(angles[i]-angles[i-1])>2.0:reversals+=1
  if reversals>15:return 3
  else:
   return 0
"""

PRODUCTION_CODE = '''"""Core model for the SafeTruck driver-assistance suite."""

from typing import List

from safetruck.config import AIS_MIN_SPEED_KMH, logger
from safetruck.data_processing import FeatureEngine


class Quantized1DTCNModel:  # pylint: disable=too-few-public-methods
    """Simulate inference behavior for the quantized model."""

    def predict_level(self, angles: List[float], speeds: List[float]) -> int:
        """Evaluate steering and speed history to resolve a safety tier."""
        if not speeds or speeds[-1] < AIS_MIN_SPEED_KMH:
            logger.warning("Operational speed threshold not met. Alerts suppressed.")
            return 0

        reversals = FeatureEngine.compute_swrr(angles)
        speed_std = FeatureEngine.compute_speed_std(speeds)
        logger.info(
            "ML Processing Telemetry: Reversals=%d, SpeedStd=%.2f",
            reversals,
            speed_std,
        )

        if reversals > 15 and speed_std < 1.5:
            return 3
        if reversals > 10:
            return 2
        if reversals > 5:
            return 1
        return 0
'''


def run_pylint(path: Path, project_root: Path) -> int:
    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = (
        str(project_root)
        if not existing_pythonpath
        else os.pathsep.join((str(project_root), existing_pythonpath))
    )
    result = subprocess.run(
        [sys.executable, "-m", "pylint", str(path)],
        cwd=project_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    print(result.stdout, end="")
    print(result.stderr, end="", file=sys.stderr)
    return result.returncode


def main() -> int:
    if find_spec("pylint") is None:
        print(
            "Pylint is not installed for this Python interpreter. "
            "Activate the project virtual environment and run "
            "`python -m pip install -r requirements.txt`.",
            file=sys.stderr,
        )
        return 1

    project_root = Path(__file__).resolve().parent
    with tempfile.TemporaryDirectory(prefix="safetruck-lint-") as temp_dir:
        temp_path = Path(temp_dir)
        draft_path = temp_path / "models_raw.py"
        production_path = temp_path / "models_refactored.py"
        draft_path.write_text(UNFORMATTED_CODE, encoding="utf-8")
        production_path.write_text(PRODUCTION_CODE, encoding="utf-8")

        print("=" * 60)
        print("1. RUNNING INITIAL PYLINT ASSESSMENT (RESEARCH CODE DRAFT)")
        print("=" * 60)
        run_pylint(draft_path, project_root)

        print("=" * 60)
        print("2. RUNNING PRODUCTION PYLINT ASSESSMENT (REFACTORED MODULE)")
        print("=" * 60)
        return run_pylint(production_path, project_root)


if __name__ == "__main__":
    raise SystemExit(main())
