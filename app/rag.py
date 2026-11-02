from __future__ import annotations
from pathlib import Path
import re

DEFAULT_POLICY_TEXT = """Store policies: PIX payments receive 5% discount and this discount cannot be combined with promotions. Online returns may be requested within 7 calendar days after receipt, subject to the store's conditions. Customer service should be informal but professional. Confirm current prices and stock from operational data before answering. Confirm promotion validity and availability before mentioning a discount."""

def extract_policy_text(pdf_path: str | Path) -> str:
    try:
        from pypdf import PdfReader
        return "\n".join(page.extract_text() or "" for page in PdfReader(str(pdf_path)).pages) or DEFAULT_POLICY_TEXT
    except Exception:
        return DEFAULT_POLICY_TEXT

def search_policy(query: str, policy_text: str) -> list[str]:
    chunks = [c.strip() for c in re.split(r"\n\s*\n|(?<=[.!?])\s+", policy_text) if c.strip()]
    terms = set(re.findall(r"\w+", query.lower()))
    ranked = sorted(chunks, key=lambda c: len(terms & set(re.findall(r"\w+", c.lower()))), reverse=True)
    return ranked[:3]
