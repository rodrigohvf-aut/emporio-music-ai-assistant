from app.tools import calculate_pix_price
from pathlib import Path
from app.agent import EmporioAssistant
from app.database import ingest_csv_directory

def test_pix_discount_does_not_stack_with_promotion():
    assert calculate_pix_price(100, 10) == 90

def test_pix_discount_applies_when_no_promotion():
    assert calculate_pix_price(100) == 95

def test_order_status_lookup(tmp_path):
    db_path = tmp_path / "emporio.db"
    project_root = Path(__file__).resolve().parents[1]
    ingest_csv_directory(project_root / "data", db_path)
    assistant = EmporioAssistant(str(db_path), str(project_root / "data" / "store_policies.pdf"))
    response = assistant.answer_without_llm("Qual o status do pedido 1?")
    assert "entregue" in response
    assert "BRAB1234567BR" in response

def test_out_of_scope_question_is_declined(tmp_path):
    db_path = tmp_path / "emporio.db"
    project_root = Path(__file__).resolve().parents[1]
    ingest_csv_directory(project_root / "data", db_path)
    assistant = EmporioAssistant(str(db_path), str(project_root / "data" / "store_policies.pdf"))
    response = assistant.answer_without_llm("Qual é a previsão do tempo hoje?")
    assert "apenas com produtos" in response
