from astrbot.api.star import Context, Star
from astrbot.api import logger, AstrBotConfig
from astrbot.api.event import filter, AstrMessageEvent
from .core import BanSystem
from .module import handle_request_review
from .module.group_request_review.log import GroupRequestLog
from pathlib import Path
from astrbot.core.utils.astrbot_path import get_astrbot_data_path
from typing import cast


class PracticalPluginCollection(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.context = context
        """插件上下文对象。"""
        self.config = config
        """插件配置。"""
        self.module_config = cast(dict, self.config["ModuleConfig"])
        """插件模块配置。"""
        self.plugin_data_path = (
            Path(get_astrbot_data_path()) / "plugin_data" / self.name
        )
        """插件数据目录。"""

    async def initialize(self):
        """初始化插件。"""
        if not self.config["GlobalEnable"]:
            logger.info(
                "插件全局开关已关闭，将不会进行任何操作。如果这不是预期行为，请检查你的插件配置。"
            )
        else:
            self.ban_system = await BanSystem.init(self.plugin_data_path)
            self.group_request_log = GroupRequestLog(self.plugin_data_path)
            await self.group_request_log.initialize()
            logger.info("插件初始化完成。")

    async def terminate(self):
        logger.info("插件已终止。")

    @filter.platform_adapter_type(filter.PlatformAdapterType.AIOCQHTTP)
    @filter.event_message_type(filter.EventMessageType.ALL)
    async def group_request_review(self, event: AstrMessageEvent):
        """加群请求自动审核模块事件接收器。"""
        if not self._event_filter(event, self.config["Whitelist"]):
            return
        await handle_request_review(
            event,
            self.module_config["GroupRequestReview"],
            self.ban_system,
            self.group_request_log,
        )

    def _event_filter(self, event: AstrMessageEvent, whitelist_config: dict) -> bool:
        """事件过滤器。

        Args:
            event (AstrMessageEvent): 事件对象。
            whitelist_config (dict): 插件白名单配置对象。

        Returns:
            bool: 如果通过检查则返回 True，否则返回 False。
        """
        if not self.config["GlobalEnable"]:
            return False
        user_id = event.get_sender_id()
        group_id = event.get_group_id()
        if user_id and group_id:  # 临时会话
            return (
                whitelist_config["AllowTemporaryConversationFromAllowedGroup"]
                and group_id in whitelist_config["WhitelistGroups"]
            )
        elif user_id:  # 私聊
            return user_id in whitelist_config["WhitelistFriends"]
        else:  # 群聊
            return group_id in whitelist_config["WhitelistGroups"]
