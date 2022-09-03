from datetime import datetime
from typing import Union
import nonebot
from nonebot import on_keyword
from nonebot import require
from nonebot.adapters.onebot.v11 import MessageSegment, PrivateMessageEvent, GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER, PRIVATE_FRIEND
import time

from .nlp_util import get_time_from_text, get_name_from_text, get_priority_from_text
from .todo import TodoToken, TodoUtil
from .config import Config

global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())

add_todo = on_keyword({'提醒', 'nonebot_todo'}, permission=GROUP_ADMIN | GROUP_OWNER | PRIVATE_FRIEND)
remove_todo = on_keyword({'删除', '去掉'}, permission=GROUP_ADMIN | GROUP_OWNER | PRIVATE_FRIEND)
finish_todo = on_keyword({'完成'}, permission=GROUP_ADMIN | GROUP_OWNER | PRIVATE_FRIEND)
change_todo_time = on_keyword({'更正', '改'}, permission=GROUP_ADMIN | GROUP_OWNER | PRIVATE_FRIEND)
get_todo_pic = on_keyword({'获取todo'}, permission=GROUP_ADMIN | GROUP_OWNER | PRIVATE_FRIEND)
scheduler = require("nonebot_plugin_apscheduler").scheduler


@add_todo.handle()
async def add_todo_handle(event: Union[PrivateMessageEvent, GroupMessageEvent]):
    text: str = event.raw_message
    exceed_time, time_valid, time_error_doc = get_time_from_text(text)
    name, name_valid, name_error_doc = get_name_from_text(text)
    priority, priority_valid, priority_error_doc = get_priority_from_text(text)
    if not time_valid:
        await add_todo.finish(time_error_doc)
    elif not name_valid:
        await add_todo.finish(name_error_doc)
    elif not priority_valid:
        await add_todo.finish(priority_error_doc)
    if isinstance(event, PrivateMessageEvent):
        todo_util = TodoUtil(str(event.user_id))
    else:
        todo_util = TodoUtil(str(event.group_id))
    todo_token = TodoToken(name, datetime.today(), exceed_time, priority)
    if todo_util.add_data_to_list(todo_token):
        await add_todo.send(f"已将{name}加入清单，ddl为{exceed_time}，优先级为{priority}。\n当前共{todo_util.list_size}项待办。")
        img = await todo_util.get_list_img()
        await remove_todo.finish(MessageSegment.image(img))
    else:
        await add_todo.finish(f"{name}已在清单中。")


@remove_todo.handle()
async def remove_todo_handle(event: Union[PrivateMessageEvent, GroupMessageEvent]):
    text: str = event.raw_message
    name, name_valid, name_error_doc = get_name_from_text(text)
    if isinstance(event, PrivateMessageEvent):
        todo_util = TodoUtil(str(event.user_id))
    else:
        todo_util = TodoUtil(str(event.group_id))
    if not name_valid:
        await remove_todo.finish(name_error_doc)
    elif todo_util.remove_data(name) == 0:
        await remove_todo.finish(f"不存在名为{name}的表项。")
    else:
        img = await todo_util.get_list_img()
        await remove_todo.send(f"已删除{name}。")
        await remove_todo.finish(MessageSegment.image(img))


@finish_todo.handle()
async def finish_todo_handle(event: Union[PrivateMessageEvent, GroupMessageEvent]):
    text: str = event.raw_message
    name, name_valid, name_error_doc = get_name_from_text(text)
    if isinstance(event, PrivateMessageEvent):
        todo_util = TodoUtil(str(event.user_id))
    else:
        todo_util = TodoUtil(str(event.group_id))
    if not name_valid:
        await remove_todo.finish(name_error_doc)
    elif todo_util.finish_job(name) == 0:
        await remove_todo.finish(f"不存在名为{name}的表项。")
    else:
        await remove_todo.send(f"已完成{name}。还剩{todo_util.list_size}项。")
        img = await todo_util.get_list_img()
        await remove_todo.finish(MessageSegment.image(img))


@change_todo_time.handle()
async def change_todo_time_handle(event: Union[PrivateMessageEvent, GroupMessageEvent]):
    text: str = event.raw_message
    name, name_valid, name_error_doc = get_name_from_text(text)
    expire_time, time_valid, time_error_doc = get_time_from_text(text)
    if isinstance(event, PrivateMessageEvent):
        todo_util = TodoUtil(str(event.user_id))
    else:
        todo_util = TodoUtil(str(event.group_id))
    if not time_valid:
        await add_todo.finish(time_error_doc)
    elif not name_valid:
        await add_todo.finish(name_error_doc)
    else:
        changed_count = todo_util.change_time(name, expire_time)
        if not changed_count == 0:
            await change_todo_time.send(f"将{name}改至{expire_time}")
            img = await todo_util.get_list_img()
            await change_todo_time.finish(MessageSegment.image(img))
        else:
            await change_todo_time.finish(f"没有名为{name}的项目。")


@get_todo_pic.handle()
async def _handle(event: Union[PrivateMessageEvent, GroupMessageEvent]):
    if isinstance(event, PrivateMessageEvent):
        todo_util = TodoUtil(str(event.user_id))
    else:
        todo_util = TodoUtil(str(event.group_id))
    img = await todo_util.get_list_img()
    await get_todo_pic.finish(MessageSegment.image(img))


async def send_todo():
    for user in plugin_config.todo_users:
        todo_util = TodoUtil(str(user))
        img = await todo_util.get_list_img()
        await nonebot.get_bot().send_private_msg(user_id=user, message=MessageSegment.image(img))
        time.sleep(5)
        # 防止风控

    for group in plugin_config.todo_groups:
        todo_util = TodoUtil(str(group))
        img = await todo_util.get_list_img()
        await nonebot.get_bot().send_group_msg(group_id=group, message=MessageSegment.image(img))
        time.sleep(5)
        # 防止风控


for index, _time in enumerate(plugin_config.todo_send_time):
    scheduler.add_job(send_todo, "cron", hour=_time.hour, minute=_time.minute, id=str(f"send_todo_for_{index}"))
