import pytest
from pydantic import ValidationError

from app.models import AnalysisResult, OrderStatus
from app.responder import generate_customer_response


def test_delay_reply_uses_only_database_facts():

    analysis = AnalysisResult(
        category="delivery_issue",
        priority="medium",
        order_id="5832",
        summary="Order is delayed.",
    )

    order = OrderStatus(
        order_id="5832",
        customer_name="Alex Morgan",
        status="delayed",
        expected_delivery="2026-09-21",
        current_location="Munich Distribution Center",
    )

    reply = generate_customer_response(
        analysis, order, "inform_customer_about_delay"
    )

    assert "5832" in reply
    assert "Munich Distribution Center" in reply
    assert "2026-09-21" in reply


def test_unknown_order_reply_asks_to_check_order_id():

    analysis = AnalysisResult(
        category="delivery_issue",
        priority="medium",
        order_id="9999",
        summary="Order cannot be found.",
    )

    reply = generate_customer_response(analysis, None, "order_not_found")

    assert "9999" in reply
    assert "check the order number" in reply


def test_invalid_ai_category_is_rejected():

    with pytest.raises(ValidationError):
        AnalysisResult.model_validate_json(
            '{"category": "banana", "priority": "medium", "summary": "x"}'
        )
