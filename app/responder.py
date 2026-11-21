from app.models import AnalysisResult, OrderStatus


# Fixed reply templates, one per action from the decision engine.
# The AI is not used here: every fact in a reply comes from the
# verified order record in the database, so nothing can be invented.
RESPONSE_TEMPLATES = {
    "inform_customer_about_delay": (
        "Your order {order_id} is currently delayed. "
        "It is at {current_location}, and the expected delivery date "
        "was {expected_delivery}. We apologize for the inconvenience."
    ),
    "confirm_delivery": (
        "Our records show that your order {order_id} was delivered "
        "on {expected_delivery}. If you cannot find it, please reply "
        "and our team will help you."
    ),
    "inform_customer_order_is_processing": (
        "Your order {order_id} is still being processed at {current_location}. "
        "The expected delivery date is {expected_delivery}."
    ),
    "order_not_found": (
        "We could not find an order with the ID {requested_order_id}. "
        "Please check the order number and try again."
    ),
    "forward_to_refund_team": (
        "Thank you for your message. Your refund request has been "
        "forwarded to our refund team, who will contact you."
    ),
    "forward_to_payment_support": (
        "Thank you for your message. Your payment question has been "
        "forwarded to our payment support team, who will contact you."
    ),
    "general_support": (
        "Thank you for your message. Our support team will get back to you shortly."
    ),
}


def generate_customer_response(
    analysis: AnalysisResult,
    order: OrderStatus | None,
    action: str,
) -> str:
    """Build the reply from a fixed template and verified order data only."""

    template = RESPONSE_TEMPLATES.get(
        action,
        RESPONSE_TEMPLATES["general_support"],
    )

    order_data = order.model_dump() if order else {}

    return template.format(
        requested_order_id=analysis.order_id,
        **order_data,
    )
