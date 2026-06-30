from typing import cast
from astrbot.api import logger


class BanSystemCore:
    """封禁系统核心功能类。"""

    ban_system_config = None
    """封禁系统配置。"""
    ban_list = None
    """封禁用户列表。"""

    def __init__(self, ban_system_config: dict):
        """初始化封禁系统。

        Args:
            ban_system_config (dict): 封禁系统配置。
        """
        self.ban_system_config = ban_system_config
        self.ban_list = cast(list[dict], self.ban_system_config["Banlist"])

    def add_ban(self, user_id: str, reason: str) -> bool:
        """添加封禁用户。

        Args:
            user_id (str): 用户 ID。
            reason (str): 封禁原因。

        Returns:
            bool: 是否请求保存配置。当此值为 True 时，调用处应当调用 `config.save_config` 方法保存配置以使封禁列表真正被写入。
        """
        if any(item["User"] == user_id for item in self.ban_list):
            logger.info(f"用户 {user_id} 已被封禁，无需重复添加。")
            return False
        self.ban_list.append(
            {"__template_key": "SingleBan", "User": user_id, "Reason": reason}
        )
        return True

    def remove_ban(self, user_id: str) -> bool:
        """移除封禁用户。

        Args:
            user_id (str): 用户 ID。

        Returns:
            bool: 是否请求保存配置。当此值为 True 时，调用处应当调用 `config.save_config` 方法保存配置以使封禁列表真正被写入。
        """
        self.ban_list = [item for item in self.ban_list if item["User"] != user_id]
        return True

    def list_ban(self) -> list[dict]:
        """获取封禁用户列表。

        Returns:
            list[dict]: 封禁用户列表。
        """
        return self.ban_list
