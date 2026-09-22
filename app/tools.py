from typing import Optional

from app.database import get_order


def get_order_status(order_id: str) -> Optional[dict]:
    return get_order(order_id)