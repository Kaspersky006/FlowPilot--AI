from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.classifier import classify_request
from app.database import (
    get_request_history,
    initialize_database,
    save_support_request,
)
from app.decision import decide_action
from app.models import (
    OrderStatus,
    RequestHistory,
    SupportRequest,
    SupportResponse,
)
from app.responder import generate_customer_response
from app.tools import get_order_status


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="FlowPilot AI",
    description="AI-powered customer support automation API",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def root():
    return {
        "status": "running",
        "service": "FlowPilot AI",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


@app.get("/orders/{order_id}", response_model=OrderStatus)
def read_order(order_id: str):
    order = get_order_status(order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    return OrderStatus(**order)


@app.get("/history", response_model=list[RequestHistory])
def history(limit: int = 20):
    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 100.",
        )

    return get_request_history(limit)


@app.post("/analyze", response_model=SupportResponse)
def analyze_request(request: SupportRequest):
    try:
        analysis = classify_request(request.message)

        order = None

        if analysis.order_id:
            order_data = get_order_status(analysis.order_id)

            if order_data:
                order = OrderStatus(**order_data)

        action = decide_action(
            analysis=analysis,
            order=order,
        )

        customer_response = generate_customer_response(
            analysis=analysis,
            order=order,
            action=action,
        )

        request_id = save_support_request(
            message=request.message,
            category=analysis.category,
            priority=analysis.priority,
            order_id=analysis.order_id,
            summary=analysis.summary,
            action=action,
            customer_response=customer_response,
        )

        return SupportResponse(
            request_id=request_id,
            analysis=analysis,
            order=order,
            action=action,
            customer_response=customer_response,
        )

    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail=f"AI service temporarily unavailable: {error}",
        )