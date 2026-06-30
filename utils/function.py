from . import ProtocolEndApi
from astrbot.api.event import AstrMessageEvent
from astrbot.api import logger


async def check_self_role(event: AstrMessageEvent, group_id: str) -> tuple[bool, bool]:
    """检查机器人在给定群聊的身份。

    Args:
        event (AstrMessageEvent): 事件对象。
        group_id (str): 要检查的群聊 ID。

    Returns:
        tuple[bool, bool]: 是否是管理员，是否是群主。
    """
    try:
        from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import (
            AiocqhttpMessageEvent,
        )

        assert isinstance(event, AiocqhttpMessageEvent)
        self_id = event.get_self_id()
        member_info = await ProtocolEndApi.get_group_member_info(
            event, group_id, self_id
        )
        match member_info["role"]:
            case "member":
                return False, False
            case "admin":
                return True, False
            case "owner":
                return True, True
            case _:
                logger.warning(
                    f"检测到未知的群成员角色: {member_info['role']}，这似乎不是 Onebot 11 的标准返回值。请检查插件是否兼容当前 AstrBot / NapCat 版本。"
                )
                return False, False
    except AssertionError:
        logger.exception(
            "加群请求事件对象类型校验失败。这可能意味着插件源代码遭到了不合理的改动，或不兼容当前的 AstrBot 版本。"
        )
        return False, False
    except Exception:
        logger.exception(f"检查机器人在群 {group_id} 的身份时发生错误。")
        return False, False
