#
# Copyright (C) 2024-2025 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#

from telethon import Button as _Button


def queue_markup(
    _,
    duration,
    cplay,
    videoid,
    played: bool | int = None,
    dur: bool | int = None,
):
    not_dur = [
        [
            _Button.inline(
                text=_["QU_B_1"],
                data=f"GetQueued {cplay}|{videoid}",
            ),
            _Button.inline(
                text=_["CLOSEMENU_BUTTON"],
                data="close",
            ),
        ]
    ]
    dur = [
        [
            _Button.inline(
                text=_["QU_B_2"].format(played, dur),
                data="GetTimer",
            )
        ],
        [
            _Button.inline(
                text=_["QU_B_1"],
                data=f"GetQueued {cplay}|{videoid}",
            ),
            _Button.inline(
                text=_["CLOSEMENU_BUTTON"],
                data="close",
            ),
        ],
    ]
    upl = not_dur if duration == "UNKNOWN" else dur
    return upl


def queue_back_markup(_, cplay):
    upl = [
        [
            _Button.inline(
                text=_["BACK_BUTTON"],
                data=f"queue_back_timer {cplay}",
            ),
            _Button.inline(
                text=_["CLOSE_BUTTON"],
                data="close",
            ),
        ]
    ]
    return upl
