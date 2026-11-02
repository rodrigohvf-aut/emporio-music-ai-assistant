from __future__ import annotations
import csv, sqlite3
from pathlib import Path

TABLES = {
    "products": "product_id INTEGER PRIMARY KEY, price_brl REAL, name TEXT, category_id INTEGER, description TEXT, stock_quantity INTEGER, status TEXT, specs TEXT, created_at TEXT",
    "categories": "category_id INTEGER PRIMARY KEY, name TEXT, description TEXT",
    "promotions": "promotion_id INTEGER PRIMARY KEY, product_id INTEGER, discount_percent REAL, description TEXT, is_active INTEGER",
    "customers": "customer_id INTEGER PRIMARY KEY, name TEXT, phone TEXT, email TEXT, city TEXT",
    "orders": "order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT, total_brl REAL, payment_method TEXT, tracking_code TEXT, estimated_delivery TEXT, notes TEXT",
    "order_items": "order_id INTEGER, quantity INTEGER, product_id INTEGER",
}

def connect(db_path: str | Path = "emporio.db") -> sqlite3.Connection:
    connection = sqlite3.connect(str(db_path))
    connection.row_factory = sqlite3.Row
    return connection

def ingest_csv_directory(data_dir: str | Path, db_path: str | Path = "emporio.db") -> None:
    data_dir = Path(data_dir)
    with connect(db_path) as connection:
        for table, schema in TABLES.items():
            connection.execute(f"CREATE TABLE IF NOT EXISTS {table} ({schema})")
            source = data_dir / f"{table}.csv"
            if not source.exists():
                continue
            rows = list(csv.DictReader(source.open(encoding="utf-8-sig", newline="")))
            if not rows:
                continue
            columns = list(rows[0])
            connection.execute(f"DELETE FROM {table}")
            placeholders = ",".join("?" for _ in columns)
            for row in rows:
                values = [None if row[c] == "" else row[c] for c in columns]
                connection.execute(f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})", values)

def query(db_path: str | Path, sql: str, parameters: tuple = ()) -> list[dict]:
    with connect(db_path) as connection:
        return [dict(row) for row in connection.execute(sql, parameters).fetchall()]
