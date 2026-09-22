from app.decision import decide_action
from app.models import AnalysisResult, OrderStatus


def test_delayed_order():

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

    result = decide_action(analysis, order)

    assert result == "inform_customer_about_delay"


def test_missing_order():

    analysis = AnalysisResult(
        category="delivery_issue",
        priority="medium",
        order_id="9999",
        summary="Order cannot be found.",
    )

    result = decide_action(analysis, None)

    assert result == "order_not_found"


def test_refund_request():

    analysis = AnalysisResult(
        category="refund_request",
        priority="medium",
        summary="Customer wants a refund.",
    )

    result = decide_action(analysis, None)

    assert result == "forward_to_refund_team"