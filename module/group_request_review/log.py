from astrbot.api import logger
from pathlib import Path
import aiosqlite
from datetime import datetime


class GroupRequestLog:
    """加群请求记录。"""

    db_path: Path = None
    """数据库文件路径。"""

    def __init__(self, plugin_data_path: Path):
        """**请使用 GroupRequestLog.init 方法初始化加群请求记录数据库。**"""
        try:
            self.plugin_data_path = plugin_data_path
            self.db_path = self.plugin_data_path / "group_request_review" / "log.db"
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
        except Exception:
            logger.exception("初始化加群请求记录数据库时发生错误。")

    @classmethod
    async def init(cls, plugin_data_path: Path):
        """初始化加群请求记录数据库。

        Args:
            plugin_data_path (Path): 插件数据目录。

        Returns:
            GroupRequestLog: 加群请求记录数据库实例。若初始化失败返回 None。
        """
        try:
            log = cls(plugin_data_path)
            async with aiosqlite.connect(log.db_path) as db:
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS request_log (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        request_time TEXT NOT NULL,
                        user_id TEXT NOT NULL
                    )
                """)
                await db.execute("""
                    CREATE INDEX IF NOT EXISTS idx_request_log_user_id
                    ON request_log(user_id)
                """)
                await db.commit()
            logger.info("加群请求记录系统初始化完成。")
            return log
        except Exception:
            logger.exception("初始化加群请求记录数据库时发生错误。")
            return None

    async def add_request(self, user_id: str) -> bool:
        """写入加群请求记录。

        Args:
            user_id (str): 加群者 ID。

        Returns:
            bool: 如果写入成功则返回 True，否则返回 False。
        """
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "INSERT INTO request_log (request_time, user_id) VALUES (?, ?)",
                    (now, user_id),
                )
                await db.commit()
            return True
        except Exception:
            logger.exception(f"写入用户 {user_id} 的加群请求记录时发生错误。")
            return False

    async def get_requests(self, user_id: str) -> list[dict]:
        """查询指定用户的加群请求记录。

        Args:
            user_id (str): 要查询的用户 ID。

        Returns:
            list[dict]: 加群请求记录列表，每条记录格式为：
            ```
            {
                "id": 0,                    // 自增 ID
                "request_time": "string",   // 请求时间，格式为 YYYY-MM-DD HH:MM:SS
                "user_id": "string"         // 加群者 ID
            }
            ```
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute(
                    "SELECT * FROM request_log WHERE user_id = ?",
                    (user_id,),
                )
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception:
            logger.exception(f"查询用户 {user_id} 的加群请求记录时发生错误。")
            return []

    async def get_requests_since(self, user_id: str, since: str) -> list[dict]:
        """查询指定用户自某个时间点以来的加群请求记录。

        Args:
            user_id (str): 要查询的用户 ID。
            since (str): 起始时间，格式为 YYYY-MM-DD HH:MM:SS。

        Returns:
            list[dict]: 加群请求记录列表。
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute(
                    "SELECT * FROM request_log WHERE user_id = ? AND request_time >= ?",
                    (user_id, since),
                )
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception:
            logger.exception(f"查询用户 {user_id} 的加群请求记录时发生错误。")
            return []

    async def del_request(self, user_id: str) -> bool:
        """删除指定用户的所有加群请求记录。

        Args:
            user_id (str): 要删除的用户 ID。

        Returns:
            bool: 如果删除成功则返回 True，否则返回 False。
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "DELETE FROM request_log WHERE user_id = ?",
                    (user_id,),
                )
                await db.commit()
            return True
        except Exception:
            logger.exception(f"删除用户 {user_id} 的加群请求记录时发生错误。")
            return False
