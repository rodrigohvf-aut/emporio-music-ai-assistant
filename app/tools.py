from __future__ import annotations
from .database import query

def search_products(db_path: str, search_term: str = "", max_price: float | None = None, only_available: bool = True) -> list[dict]:
    clauses, params = ["LOWER(p.name || ' ' || COALESCE(p.description, '')) LIKE ?"], [f"%{search_term.lower()}%"]
    if max_price is not None: clauses.append("p.price_brl <= ?"); params.append(max_price)
    if only_available: clauses.append("p.stock_quantity > 0 AND p.status = 'active'")
    return query(db_path, f"SELECT p.*, c.name AS category_name FROM products p LEFT JOIN categories c ON c.category_id=p.category_id WHERE {' AND '.join(clauses)} ORDER BY p.price_brl", tuple(params))

def get_product(db_path: str, name: str) -> list[dict]:
    return query(db_path, "SELECT * FROM products WHERE LOWER(name) LIKE ?", (f"%{name.lower()}%",))

def get_active_promotions(db_path: str) -> list[dict]:
    return query(db_path, "SELECT p.name, x.discount_percent, x.description FROM promotions x JOIN products p ON p.product_id=x.product_id WHERE x.is_active=1 AND p.stock_quantity>0")

def get_order(db_path: str, order_id: int) -> list[dict]:
    return query(db_path, "SELECT o.*, c.name AS customer_name FROM orders o JOIN customers c ON c.customer_id=o.customer_id WHERE o.order_id=?", (order_id,))

def calculate_pix_price(price_brl: float, promotion_percent: float = 0) -> float:
    """Apply the store rule: PIX discount does not stack with promotions."""
    discount = promotion_percent if promotion_percent > 0 else 5
    return round(price_brl * (1 - discount / 100), 2)
