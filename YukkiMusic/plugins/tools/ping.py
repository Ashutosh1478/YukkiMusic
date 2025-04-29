#
# Copyright (C) 2024-2025 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#
from datetime import datetime

from config import PING_IMG_URL
from YukkiMusic import tbot
from YukkiMusic.core import filters
from YukkiMusic.core.call import Yukki
from YukkiMusic.misc import BANNED_USERS
from YukkiMusic.utils import bot_sys_stats, language
from YukkiMusic.utils.inline import support_group_markup


@tbot.on_message(filters.command("PING_COMMAND", True) & ~BANNED_USERS)
@language
async def ping_com(event, _):
    response = await event.reply(
        file=PING_IMG_URL,
        message=_["ping_1"].format(tbot.mention),
    )
    start = datetime.now()
    pytgping = await Yukki.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    await response.edit(
        _["ping_2"].format(
            resp,
            tbot.mention,
            UP,
            RAM,
            CPU,
            DISK,
            pytgping,
        ),
        buttons=support_group_markup(_),
    )
