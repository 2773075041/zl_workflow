import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional


class HistoryStorage:
    """执行历史存储 - SQLite"""

    def __init__(self, db_path: str = "workflow_history.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """初始化数据库"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS execution_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    workflow_id TEXT NOT NULL,
                    workflow_name TEXT,
                    started_at TEXT NOT NULL,
                    finished_at TEXT,
                    status TEXT,
                    node_states TEXT,
                    error_message TEXT
                )
            """)

    def add_execution(self, workflow_id: str, workflow_name: str = "") -> int:
        """添加执行记录"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO execution_history (workflow_id, workflow_name, started_at, status)
                VALUES (?, ?, ?, ?)
            """, (workflow_id, workflow_name, datetime.now().isoformat(), "running"))
            return cursor.lastrowid

    def finish_execution(self, execution_id: int, status: str, node_states: Dict = None, error_message: str = None):
        """完成执行记录"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE execution_history
                SET finished_at = ?, status = ?, node_states = ?, error_message = ?
                WHERE id = ?
            """, (
                datetime.now().isoformat(),
                status,
                json.dumps(node_states or {}),
                error_message,
                execution_id
            ))

    def get_history(self, workflow_id: str = None, limit: int = 50) -> List[Dict]:
        """获取执行历史"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            if workflow_id:
                cursor = conn.execute("""
                    SELECT * FROM execution_history
                    WHERE workflow_id = ?
                    ORDER BY started_at DESC
                    LIMIT ?
                """, (workflow_id, limit))
            else:
                cursor = conn.execute("""
                    SELECT * FROM execution_history
                    ORDER BY started_at DESC
                    LIMIT ?
                """, (limit,))
            return [dict(row) for row in cursor.fetchall()]

    def get_execution(self, execution_id: int) -> Optional[Dict]:
        """获取单条执行记录"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM execution_history WHERE id = ?
            """, (execution_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def clear_history(self, workflow_id: str = None):
        """清空历史记录"""
        with sqlite3.connect(self.db_path) as conn:
            if workflow_id:
                conn.execute("DELETE FROM execution_history WHERE workflow_id = ?", (workflow_id,))
            else:
                conn.execute("DELETE FROM execution_history")
