from __future__ import annotations
import os
import re
from pathlib import Path
from .prompts import SYSTEM_PROMPT
from .database import ingest_csv_directory, query
from .tools import search_products, get_product, get_active_promotions, get_order
from .rag import extract_policy_text, search_policy

class EmporioAssistant:
    def __init__(self, db_path: str = "emporio.db", policy_path: str = "data/store_policies.pdf"):
        self.db_path = db_path
        self._ensure_database()
        self.policy_text = extract_policy_text(policy_path)

    def _ensure_database(self) -> None:
        """Create the local database from bundled CSVs when it is missing or empty."""
        try:
            products = query(self.db_path, "SELECT COUNT(*) AS count FROM products")
            categories = query(self.db_path, "SELECT COUNT(*) AS count FROM categories")
            if not products or products[0]["count"] == 0 or not categories or categories[0]["count"] == 0:
                raise RuntimeError("Operational tables are empty")
        except Exception:
            project_root = Path(__file__).resolve().parents[1]
            data_dir = project_root / "data"
            ingest_csv_directory(data_dir, self.db_path)

    def answer_without_llm(self, message: str) -> str:
        lower = message.lower()
        if any(word in lower for word in ("devolver", "devolução", "troca", "return")):
            return "Você pode solicitar uma devolução online em até 7 dias corridos após o recebimento, conforme as condições da loja."
        if "pix" in lower and ("desconto" in lower or "quanto" in lower):
            return "O pagamento via PIX tem 5% de desconto, sem acumular com outras promoções."
        if "promo" in lower:
            rows = get_active_promotions(self.db_path)
            return "Promoções ativas: " + "; ".join(f"{r['name']} ({r['discount_percent']}% off)" for r in rows) if rows else "No momento, não encontrei promoções ativas."
        if "quanto custa" in lower or "qual o preço" in lower or "qual é o preço" in lower:
            product_name = re.sub(r".*?(?:quanto custa|qual o preço|qual é o preço)\s+(?:o|a|do|da)?\s*", "", message, flags=re.IGNORECASE).rstrip("? .")
            direct_results = get_product(self.db_path, product_name)
            if direct_results:
                product = direct_results[0]
                return f"{product['name']} custa R\\$ {product['price_brl']:.2f} e tem {product['stock_quantity']} unidade(s) em estoque."
        max_price = None
        price_match = re.search(r"(?:r\$|rs\$?)\s*([\d.,]+)|(?:até|ate|under|up to)\s*([\d.,]+)", lower)
        if price_match:
            raw_price = next(value for value in price_match.groups() if value)
            max_price = float(raw_price.replace(".", "").replace(",", "."))
        # Use an accent-neutral stem because SQLite's built-in LOWER/LIKE is not
        # reliably accent-aware across platforms.
        search_term = "viol" if any(term in lower for term in ("violão", "violões", "violao", "violoes", "guitarra acústica", "guitarra acustica")) else message
        results = search_products(self.db_path, search_term, max_price=max_price, only_available=True)
        if results:
            return "Encontrei: " + "; ".join(f"{r['name']} por R\\$ {r['price_brl']:.2f} ({r['stock_quantity']} em estoque)" for r in results[:5])
        policy = search_policy(message, self.policy_text)
        useful_policy = next((item for item in policy if len(item) > 30 and not re.fullmatch(r"[\d. ]+", item)), None)
        return useful_policy or "Não encontrei essa informação. Posso ajudar com produtos, preços, estoque, promoções ou pedidos."

    def answer(self, message: str) -> str:
        if not os.getenv("OPENAI_API_KEY"):
            return self.answer_without_llm(message)
        try:
            from openai import OpenAI
            response = OpenAI().responses.create(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), instructions=SYSTEM_PROMPT, input=message)
            return response.output_text
        except Exception:
            return self.answer_without_llm(message)
