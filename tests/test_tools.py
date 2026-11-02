from app.tools import calculate_pix_price

def test_pix_discount_does_not_stack_with_promotion():
    assert calculate_pix_price(100, 10) == 90

def test_pix_discount_applies_when_no_promotion():
    assert calculate_pix_price(100) == 95
