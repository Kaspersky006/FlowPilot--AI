import sqlite3
from datetime import datetime, timezone
from typing import Optional

from app.config import DATABASE_PATH


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT PRIMARY KEY,
                customer_name TEXT NOT NULL,
                status TEXT NOT NULL,
                expected_delivery TEXT NOT NULL,
                current_location TEXT NOT NULL
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS support_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT NOT NULL,
                category TEXT NOT NULL,
                priority TEXT NOT NULL,
                order_id TEXT,
                summary TEXT NOT NULL,
                action TEXT NOT NULL,
                customer_response TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        existing_orders = connection.execute(
            "SELECT COUNT(*) FROM orders"
        ).fetchone()[0]

        if existing_orders == 0:
            orders = [
                (
                    "5832",
                    "Alex Morgan",
                    "delayed",
                    "2026-09-21",
                    "Munich Distribution Center",
                ),
                (
                    "7391",
                    "Sarah Miller",
                    "delivered",
                    "2026-09-20",
                    "Delivered",
                ),
                (
                    "9124",
                    "Daniel Weber",
                    "processing",
                    "2026-09-25",
                    "Warehouse",
                ),
            ]

            connection.executemany(
                """
                INSERT INTO orders (
                    order_id,
                    customer_name,
                    status,
                    expected_delivery,
                    current_location
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                orders,
            )

        connection.commit()


def get_order(order_id: str) -> Optional[dict]:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT
                order_id,
                customer_name,
                status,
                expected_delivery,
                current_location
            FROM orders
            WHERE order_id = ?
            """,
            (order_id,),
        ).fetchone()

    if row is None:
        return None

    return dict(row)


def save_support_request(
    message: str,
    category: str,
    priority: str,
    order_id: Optional[str],
    summary: str,
    action: str,
    customer_response: str,
) -> int:

    created_at = datetime.now(timezone.utc).isoformat()

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO support_requests (
                message,
                category,
                priority,
                order_id,
                summary,
                action,
                customer_response,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                message,
                category,
                priority,
                order_id,
                summary,
                action,
                customer_response,
                created_at,
            ),
        )

        connection.commit()

        return cursor.lastrowid


def get_request_history(limit: int = 20) -> list[dict]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                id,
                message,
                category,
                priority,
                order_id,
                summary,
                action,
                customer_response,
                created_at
            FROM support_requests
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]