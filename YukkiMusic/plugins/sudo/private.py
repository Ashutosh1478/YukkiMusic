#
# Copyright (C) 2024-2025 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#


import config
from YukkiMusic import app, tbot
from YukkiMusic.core import filters as flt
from YukkiMusic.misc import SUDOERS
from YukkiMusic.utils.database import (
    add_private_chat,
    get_private_served_chats,
    is_served_private_chat,
    remove_private_chat,
)
from YukkiMusic.utils.decorators.language import language


@tbot.on_message(flt.command("AUTHORIZE_COMMAND", True) & flt.user(SUDOERS))
@language
async def authorize(event, _):
    if not config.PRIVATE_BOT_MODE:
        return await event.reply(_["pbot_12"])
    if len(event.text.split()) != 2:
        return await event.reply(_["pbot_1"])
    try:
        chat_id = int(event.text.strip().split()[1])
    except Exception:
        return await event.reply(_["pbot_7"])
    if not await is_served_private_chat(chat_id):
        await add_private_chat(chat_id)
        await event.reply(_["pbot_3"])
    else:
        await event.reply(_["pbot_5"])


@tbot.on_message(flt.command("UNAUTHORIZE_COMMAND", True) & flt.user(SUDOERS))
@language
async def unauthorize(event, _):
    if not config.PRIVATE_BOT_MODE:
        return await event.reply(_["pbot_12"])
    if len(event.text.split()) != 2:
        return await event.reply(_["pbot_2"])
    try:
        chat_id = int(event.text.strip().split()[1])
    except Exception:
        return await event.reply(_["pbot_7"])
    if not await is_served_private_chat(chat_id):
        return await event.reply(_["pbot_6"])
    else:
        await remove_private_chat(chat_id)
        return await event.reply(_["pbot_4"])


@tbot.on_message(flt.command("AUTHORIZED_COMMAND", True) & flt.user(SUDOERS))
@language
async def authorized(event, _):
    if not config.PRIVATE_BOT_MODE:
        return await event.reply(_["pbot_12"])
    m = await event.reply(_["pbot_8"])
    served_chats = []
    text = _["pbot_9"]
    chats = await get_private_served_chats()
    for chat in chats:
        served_chats.append(int(chat["chat_id"]))
    count = 0
    co = 0
    msg = _["pbot_13"]
    for served_chat in served_chats:
        try:
            title = (await app.get_entity(served_chat)).title
            count += 1
            text += f"{count}:- {title[:15]} [{served_chat}]\n"
        except Exception:
            title = _["pbot_10"]
            co += 1
            msg += f"{co}:- {title} [{served_chat}]\n"
    if co == 0:
        if count == 0:
            return await m.edit(_["pbot_11"])
        else:
            return await m.edit(text)
    else:
        if count == 0:
            await m.edit(msg)
        else:
            text = f"{text} {msg}"
            return await m.edit(text)
