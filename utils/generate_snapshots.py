import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# Branches and SKUs definitions
branches = ["JUNDIAI", "PIRACICABA", "RIBEIRAO PRETO"]
skus = [
    "SKU-0001", "SKU-0002", "SKU-0003", "SKU-0004", "SKU-0005"
]

# Function to generate a snapshot for a given date
def make_snapshot(date: datetime) -> dict:
    """
    Generates the snapshot dictionary for the given date,
    with the snapshot in "YYYY-MM-DD" format and random quantities between 0–1000.
    """
    snapshot = {
        "snapshot": date.strftime("%Y-%m-%d"),
        "data": []
    }

    for branch in branches:
        branch_data = {
            "branch": branch,
            "stocks": [
                {"sku": sku, "qty": random.randint(0, 1000)} for sku in skus
            ]
        }
        snapshot["data"].append(branch_data)

    return snapshot

# Function to generate a batch of snapshots from start_date to end_date
def generate_batch(start_date: str, end_date: str, out_folder: str):
    """
    Generates JSON files from start_date to end_date (inclusive).
    - start_date, end_date: "YYYY-MM-DD"
    - out_folder: local path where the JSONs will be saved
    Each file will be saved as: out_folder/YYYY-MM-DD.json
    """
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    Path(out_folder).mkdir(parents=True, exist_ok=True)

    current_date = start_date
    while current_date <= end_date:
        snapshot = make_snapshot(current_date)
        file_path = Path(out_folder) / f"{current_date.strftime("%Y-%m-%d")}.json"
        with open(file_path, "w") as f:
            json.dump(snapshot, f, indent=4)
        current_date += timedelta(days=1)

if __name__ == "__main__":
    generate_batch("2025-05-05", "2025-05-06", "./snapshots/exported")
