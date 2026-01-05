import papermill as pm
from datetime import datetime
import os
import sys

# ====== Setup Logging ======
base_path = r"C:\Users\myoge\Contacts\Regression Based Project"
os.makedirs(base_path, exist_ok=True)

log_path = os.path.join(base_path, "run_log.txt")
sys.stdout = open(log_path, "a", buffering=1, encoding="utf-8")
sys.stderr = sys.stdout

print(f"\n----- Run started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -----")

# ====== Setup Paths ======
os.makedirs(os.path.join(base_path, "runs"), exist_ok=True)
today = datetime.now().strftime("%Y-%m-%d")

try:
    # ====== Step 1: Data Pipeline ======
    print("\nStep 1: Running ML_Trading_File1.ipynb...")
    pm.execute_notebook(
        os.path.join(base_path, "ML_Trading_File1.ipynb"),
        os.path.join(base_path, f"runs/ML_Trading_File1_{today}.ipynb"),
        parameters={"run_date": today}
    )

    # ====== Step 2: Alpha Factors ======
    print("\nStep 2: Running Alpha_Research_File2.ipynb...")
    pm.execute_notebook(
        os.path.join(base_path, "Alpha_Research_File2.ipynb"),
        os.path.join(base_path, f"runs/Alpha_Research_File2_{today}.ipynb"),
        parameters={"run_date": today}
    )

    # ====== Step 3: Production Model & Strategy ======
    print("\nStep 3: Running Production_v1.0.ipynb...")
    pm.execute_notebook(
        os.path.join(base_path, "Production_v1.0.ipynb"),
        os.path.join(base_path, f"runs/Production_v1.0_{today}.ipynb"),
        parameters={"run_date": today}
    )

    print("\nAll notebooks executed successfully!")

except Exception as e:
    print(f"\nERROR: {e}")

finally:
    print(f"----- Run finished at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -----\n")
    sys.stdout.close()
