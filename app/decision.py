from typing import Optional

from app.models import AnalysisResult, OrderStatus


def decide_action(
    analysis: AnalysisResult,
    order: Optional[OrderStatus],
) -> str:

    if analysis.order_id and order is None:
        return "order_not_found"

    if order:
        if order.status == "delayed":
            return "inform_customer_about_delay"

        if order.status == "delivered":
            return "confirm_delivery"

        if order.status == "processing":
            return "inform_customer_order_is_processing"

    if analysis.category == "refund_request":
        return "forward_to_refund_team"

    if analysis.category == "payment_issue":
        return "forward_to_payment_support"

    return "general_support"