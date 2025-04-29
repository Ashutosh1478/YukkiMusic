#
# Copyright (C) 2024-2025 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#
import asyncio
import logging
import re

from async_lru import alru_cache
from youtubesearchpython.__future__ import VideosSearch
from yt_dlp import YoutubeDL

import config
from config import cookies
from YukkiMusic.utils.decorators import asyncify
from YukkiMusic.utils.formatters import time_to_seconds

from ..core.enum import SourceType
from .base import PlatformBase

logger = logging.getLogger(__name__)


class YouTube(PlatformBase):
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    async def valid(self, link: str) -> bool:
        return bool(re.search(self.regex, link))

    @alru_cache(maxsize=None)
    #@asyncify
    async def formats(self, link: str, videoid: bool | str = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]

        ytdl_opts = {
            "quiet": True,
            "cookiefile": f"{cookies()}",
        }

        ydl = YoutubeDL(ytdl_opts)
        with ydl:
            formats_available = []
            r = ydl.extract_info(link, download=False)
            for format in r["formats"]:
                try:
                    str(format["format"])
                except Exception:
                    continue
                if "dash" not in str(format["format"]).lower():
                    try:
                        formats_available.append(
                            {
                                "format": format["format"],
                                "filesize": format["filesize"],
                                "format_id": format["format_id"],
                                "ext": format["ext"],
                                "format_note": format["format_note"],
                                "yturl": link,
                            }
                        )
                    except KeyError:
                        continue
        return formats_available, link

    @alru_cache(maxsize=None)
    async def playlist(
        self, link, limit: int = config.PLAYLIST_FETCH_LIMIT
    ) -> list[Track]:
        if "&" in link:
            link = link.split("&")[0]

        cmd = (
            f"yt-dlp -i --compat-options --no-youtube-unavailable-videos "
            f'--get-id --flat-playlist --playlist-end {limit} --skip-download "{link}" '
            f"2>/dev/null"
        )
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        out, errorz = await proc.communicate()
        if errorz:
            if "unavailable videos are hidden" in (errorz.decode("utf-8")).lower():
                playlist = out.decode("utf-8")
            else:
                raise Exception(errorz.decode("utf-8"))

        playlist = out.decode("utf-8")

        result = []
        try:
            for key in playlist.split("\n"):
                if key:
                    result.append(key)
        except Exception:
            pass
        if result:
            item = result.pop(0)
            result.insert(0, await self.track(self.base + item))
        return result  # FIRST ELEMET IS Track AND OTHER(S) VIDEOID

    @alru_cache(maxsize=None)
    @staticmethod
    async def track(url: str):
        if "playlist" in url:
            return await self.playlist(url)

        try:
            results = VideosSearch(url, limit=1)
            for result in (await results.next())["result"]:
                duration = result.get("duration")
                return Track(
                    title=result["title"],
                    link=result["link"],
                    duration=(time_to_seconds(duration) if duration is not None else 0),
                    thumb=result["thumbnails"][0]["url"].split("?")[0],
                    streamtype=SourceType.YOUTUBE,
                    video=None,
                )
        except Exception:
            logger.info("", exc_info=True)
            return await YouTube._track(url)

    @alru_cache(maxsize=None)
    @staticmethod
    async def _track(
        url,
    ):  # implement getting track with help of oembed url use ytdlp for fallback
        return await YouTube._track_from_ytdlp(url)

    @alru_cache(maxsize=None)
    @staticmethod
    #@asyncify
    async def _track_from_ytdlp(query: str):
        options = {
            "format": "best",
            "noplaylist": True,
            "quiet": True,
            "extract_flat": "in_playlist",
            "cookiefile": cookies(),
        }
        logger.info(f"Searching Song from yt-dlp for {query}")
        with YoutubeDL(options) as ydl:
            info_dict = ydl.extract_info(
                f"ytsearch: {query}", download=False
            )  # TODO: THIS CAN RETURN SEARCH RESULT OF A CHANNEL FIX IT
            details = info_dict.get("entries", [None])[0]
            if not details:
                raise ValueError("No results found.")

            return Track(
                title=details["title"],
                link=(
                    details["webpage_url"].split("&")[0]
                    if "&" in details["webpage_url"]
                    else details["webpage_url"]
                ),
                duration=details["duration"],
                thumb=details["thumbnails"][0]["url"],
                streamtype=SourceType.YOUTUBE,
                video=None,
            )
