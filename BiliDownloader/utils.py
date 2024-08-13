# BiliDownloader, a tool for downloading audio or video from Bilibili.
# Copyright (C) 2024 zhengxyz123
#
# This program is free software: you can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program. If not, see <https://www.gnu.org/licenses/>.

from functools import lru_cache

import urllib3


user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0"


@lru_cache()
def bilibili_api(method: str, url: str, **kwargs) -> dict:
    if "headers" not in kwargs:
        kwargs["headers"] = {}
    kwargs["headers"]["User-Agent"] = user_agent
    return urllib3.request(method, f"https://api.bilibili.com/x/{url}", **kwargs).json()


def sec2str(duration: int) -> str:
    assert duration >= 0
    hour = duration // 3600
    minute = (duration % 3600) // 60
    second = (duration % 3600) % 60
    if hour != 0:
        return f"{hour}:{minute:02}:{second:02}"
    elif minute != 0:
        return f"{minute:02}:{second:02}"
    return f"00:{second:02}"


__all__ = ("bilibili_api", "sec2str")
