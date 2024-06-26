#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyrogram.types import Message


async def admin_check(message: Message) -> bool:
    if not message.from_user:
        return False

    if message.chat.type not in ["supergroup", "channel"]:
        return False

    client = message._client
    chat_id = message.chat.id
    user_id = message.from_user.id

    check_status = await client.get_chat_member(
        chat_id=chat_id,
        user_id=user_id
    )
    admin_strings = [
        "creator",
        "administrator"
    ]
    # https://git.colinshark.de/PyroBot/PyroBot/src/branch/master/pyrobot/modules/admin.py#L69
    return check_status.status in admin_strings
