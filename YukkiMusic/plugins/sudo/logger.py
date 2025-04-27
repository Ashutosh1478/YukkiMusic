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
from YukkiMusic.core import filters
from YukkiMusic.misc import SUDOERS
from YukkiMusic.utils import add_off, add_on, language


@tbot.on_message(filters.command("LOGGER_COMMAND", True) & filters.user(SUDOERS))
@language
async def logger(event, _):
    usage = _["log_1"]
    if len(event.text.split()) != 2:
        return await event.reply(usage)
    state = event.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        await add_on(config.LOG)
        await event.reply(_["log_2"])
    elif state == "disable":
        await add_off(config.LOG)
        await event.reply(_["log_3"])
    else:
        await event.reply(usage)
