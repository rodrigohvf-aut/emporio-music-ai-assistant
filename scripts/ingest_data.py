from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.database import ingest_csv_directory

if __name__ == "__main__":
    ingest_csv_directory(PROJECT_ROOT / "data", PROJECT_ROOT / "emporio.db")
    print("Database ingestion completed.")
