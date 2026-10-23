"""Repository: сырой SQL, без ORM."""

from __future__ import annotations

from typing import Any, List, Optional

from db import get_connection


class OrderRepository:
    def create(
        self,
        trader_id: int,
        instrument_id: int,
        side: str,
        price: float,
        quantity: int,
    ) -> dict:
        with get_connection() as conn:
            cur = conn.execute(
                """INSERT INTO orders(trader_id, instrument_id, side, price, quantity)
                   VALUES (?, ?, ?, ?, ?)""",
                (trader_id, instrument_id, side, price, quantity),
            )
            conn.commit()
            return self.get_by_id(cur.lastrowid)  # type: ignore

    def get_by_id(self, order_id: int) -> Optional[dict]:
        with get_connection() as conn:
            row = conn.execute(
                """SELECT o.*, i.ticker, i.name AS instrument_name, t.name AS trader_name
                   FROM orders o
                   JOIN instruments i ON i.id = o.instrument_id
                   JOIN traders t ON t.id = o.trader_id
                   WHERE o.id = ?""",
                (order_id,),
            ).fetchone()
            return dict(row) if row else None

    def list_all(
        self,
        status: str | None = None,
        ticker: str | None = None,
    ) -> List[dict]:
        sql = """
            SELECT o.*, i.ticker, i.name AS instrument_name, t.name AS trader_name
            FROM orders o
            JOIN instruments i ON i.id = o.instrument_id
            JOIN traders t ON t.id = o.trader_id
            WHERE 1=1
        """
        params: list[Any] = []
        if status:
            sql += " AND o.status = ?"
            params.append(status)
        if ticker:
            sql += " AND i.ticker = ?"
            params.append(ticker.upper())
        sql += " ORDER BY o.id"
        with get_connection() as conn:
            rows = conn.execute(sql, params).fetchall()
            return [dict(r) for r in rows]

    def update_status(self, order_id: int, status: str) -> Optional[dict]:
        with get_connection() as conn:
            conn.execute(
                "UPDATE orders SET status = ? WHERE id = ?",
                (status, order_id),
            )
            conn.commit()
        return self.get_by_id(order_id)

    def delete(self, order_id: int) -> bool:
        with get_connection() as conn:
            cur = conn.execute("DELETE FROM orders WHERE id = ?", (order_id,))
            conn.commit()
            return cur.rowcount > 0

    def active_volume(self) -> float:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT COALESCE(SUM(price * quantity), 0) FROM orders WHERE status = 'active'"
            ).fetchone()
            return float(row[0])

    def stats_by_ticker(self) -> List[dict]:
        with get_connection() as conn:
            rows = conn.execute(
                """SELECT i.ticker,
                          COUNT(o.id) AS orders_count,
                          SUM(CASE WHEN o.status='active' THEN 1 ELSE 0 END) AS active_count,
                          COALESCE(SUM(o.price * o.quantity), 0) AS total_volume
                   FROM instruments i
                   LEFT JOIN orders o ON o.instrument_id = i.id
                   GROUP BY i.ticker
                   ORDER BY total_volume DESC"""
            ).fetchall()
            return [dict(r) for r in rows]

    def transfer_orders(self, from_trader: int, to_trader: int) -> int:
        with get_connection() as conn:
            try:
                conn.execute("BEGIN")
                cur = conn.execute(
                    """UPDATE orders SET trader_id = ?
                       WHERE trader_id = ? AND status = 'active'""",
                    (to_trader, from_trader),
                )
                conn.execute("COMMIT")
                return cur.rowcount
            except Exception:
                conn.execute("ROLLBACK")
                raise
