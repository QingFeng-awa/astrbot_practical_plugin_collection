from typing import Literal, cast

from astrbot.api import logger
from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import (
    AiocqhttpMessageEvent,
)


class ProtocolEndApi:
    """调用 NapCat（协议端）API。"""

    @staticmethod
    async def set_group_add_request(
        event: AiocqhttpMessageEvent,
        request_flag: str,
        sub_type: Literal["invite", "add"],
        approve: bool,
        reason: str = "",
    ):
        """## 处理加群请求

        同意或拒绝加群请求或邀请。

        Args:
            event (AiocqhttpMessageEvent): 事件对象。
            request_flag (str): 加群请求 flag。
            sub_type (Literal["invite", "add"]): 加群请求类型，`"invite"` 表示邀请登录号入群，`"add"` 表示他人加群请求。
            approve (bool): 是否同意加群请求。
            reason (str, optional): 拒绝原因，仅在拒绝加群请求时有效。若不传入或传入空字符串则表示无理由拒绝。

        Raises:
            Exception: 在发生错误时方法会在输出错误日志后原样抛出异常。
        """
        try:
            payloads = {
                "flag": request_flag,
                "sub_type": sub_type,
                "approve": approve,
                "reason": reason,
                "self_id": event.get_self_id(),
            }
            client = event.bot
            logger.debug(
                f"准备请求协议端 API /set_group_add_request，请求参数：{payloads}。"
            )
            await client.api.set_group_add_request(**payloads)
            # 没返回值只能这么写
            logger.debug("请求了协议端 API /set_group_add_request。")
        except Exception:
            logger.exception(
                f"调用 API /set_group_add_request 时发生错误，请求参数：{payloads}。"
            )
            raise

    @staticmethod
    async def get_group_member_info(
        event: AiocqhttpMessageEvent,
        group_id: str,
        user_id: str,
        no_cache: bool = False,
    ) -> dict:
        """## 获取群成员信息

        获取群聊中指定成员的信息。

        Args:
            event (AiocqhttpMessageEvent): 事件对象。
            group_id (str): 群聊 ID。
            user_id (str): 要获取信息的用户 ID。
            no_cache (bool, optional): 是否绕过缓存获取信息。通过缓存获取信息更快，但可能存在更新延迟。默认优先使用缓存数据即不绕过缓存。

        Returns:
            dict: 给定的群成员的信息。

        Raises:
            Exception: 在发生错误时方法会在输出错误日志后原样抛出异常。
        """
        try:
            payloads = {
                "group_id": group_id,
                "user_id": user_id,
                "no_cache": no_cache,
                "self_id": event.get_self_id(),
            }
            client = event.bot
            logger.debug(
                f"准备请求协议端 API /get_group_member_info，请求参数：{payloads}。"
            )
            member_info = await client.api.get_group_member_info(**payloads)
            logger.debug(
                f"协议端 API /get_group_member_info 返回群成员信息：{member_info}"
            )
            return cast(dict, member_info)
        except Exception:
            logger.exception(
                f"调用 API /get_group_member_info 时发生错误，请求参数：{payloads}。"
            )
            raise

    @staticmethod
    async def get_stranger_info(
        event: AiocqhttpMessageEvent, user_id: str, no_cache: bool = False
    ) -> dict:
        """## 获取陌生人信息

        获取指定非好友用户的信息。

        Args:
            event (AiocqhttpMessageEvent): 事件对象。
            user_id (str): 要获取信息的用户 ID。
            no_cache (bool, optional): 是否绕过缓存获取信息。通过缓存获取信息更快，但可能存在更新延迟。默认优先使用缓存数据即不绕过缓存。

        Returns:
            dict: 给定的用户的信息。

        Raises:
            Exception: 在发生错误时方法会在输出错误日志后原样抛出异常。
        """
        try:
            payloads = {
                "user_id": user_id,
                "no_cache": no_cache,
                "self_id": event.get_self_id(),
            }
            client = event.bot
            logger.debug(
                f"准备请求协议端 API /get_stranger_info，请求参数：{payloads}。"
            )
            stranger_info = await client.api.get_stranger_info(**payloads)
            logger.debug(f"协议端 API /get_stranger_info 返回用户信息：{stranger_info}")
            return cast(dict, stranger_info)
        except Exception:
            logger.exception(
                f"调用 API /get_stranger_info 时发生错误，请求参数：{payloads}。"
            )
            raise
