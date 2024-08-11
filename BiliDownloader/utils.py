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

import urllib3

headers = {
    "User-Agent": "Mozilla/5.0 (Windows U Windows NT 6.1 en-US rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6"
}


def get_json(method: str, url: str, **kwargs) -> dict:
    if "headers" in kwargs:
        del kwargs["headers"]
    return urllib3.request(method, url, headers=headers, **kwargs).json()


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


__all__ = ("get_json", "sec2str")
