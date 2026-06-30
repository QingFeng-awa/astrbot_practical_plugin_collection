from typing import Literal, cast

from astrbot.api import logger
from astrbot.api.event import AstrMessageEvent


def event_filter(
    event: AstrMessageEvent,
    post_type: Literal["message", "notice", "request"] = "message",
    subtype: str = "",
    secondary_subtype: str = "",
) -> bool:
    """检查事件是否与传入的要求类型匹配。

    Args:
        event (AstrMessageEvent): 事件对象。
        post_type (Literal["message", "notice", "request"], optional): 事件的上报类型，默认为`"message"`。
        subtype (str, optional): 事件的子类型，若不填写则不筛选子类型。此参数对应 `post_type` 为 `"message"` 的 `message_type`；为 `"notice"` 的 `notice_type`；为 `"request"` 的 `request_type`。
        secondary_subtype (str, optional): 事件的二级子类型，若不填写则不筛选二级子类型。此参数对应事件中的 `sub_type`。要注意某些事件没有该类型，若不当传参可能导致永远无法通过匹配。

    Returns:
        bool: 事件是否匹配。
    """
    raw_message = cast(dict, event.message_obj.raw_message)
    if raw_message["post_type"] != post_type:
        return False
    match raw_message["post_type"]:
        case "message":
            if subtype and raw_message["message_type"] != subtype:
                return False
        case "notice":
            if subtype and raw_message["notice_type"] != subtype:
                return False
        case "request":
            if subtype and raw_message["request_type"] != subtype:
                return False
        case _:  # 其他未知的神秘事件类型
            logger.warning(
                f"检测到未知的事件子类型: {raw_message.get('sub_type', 'None')}，这似乎不是 Onebot 11 的标准事件类型。请检查插件是否兼容当前 AstrBot / NapCat 版本。"
            )
            return False
    if secondary_subtype:
        if raw_message.get("sub_type", "") != secondary_subtype:
            return False
    return True
