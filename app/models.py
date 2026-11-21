from typing import Literal, Optional

from pydantic import BaseModel


class SupportRequest(BaseModel):
    message: str


class AnalysisResult(BaseModel):
    # Literal: Pydantic rejects any value that is not in this list
    category: Literal[
        "delivery_issue",
        "refund_request",
        "payment_issue",
        "account_support",
        "product_question",
        "other",
    ]
    priority: Literal["low", "medium", "high"]
    order_id: Optional[str] = None
    summary: str


class OrderStatus(BaseModel):
    order_id: str
    customer_name: str
    status: str
    expected_delivery: str
    current_location: str


class SupportResponse(BaseModel):
    request_id: int
    analysis: AnalysisResult
    order: Optional[OrderStatus] = None
    action: str
    customer_response: str


class RequestHistory(BaseModel):
    id: int
    message: str
    category: str
    priority: str
    order_id: Optional[str] = None
    summary: str
    action: str
    customer_response: str
    created_at: str