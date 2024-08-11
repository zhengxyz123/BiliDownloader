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

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWizard

from BiliDownloader.pages import PageEnum
from BiliDownloader.pages.get_info import GetInfoWizardPage
from BiliDownloader.pages.start import StartWizardPage


class MainWindow(QWizard):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("BiliDownloader")
        self.setAttribute(Qt.WidgetAttribute.WA_InputMethodEnabled, True)
        self.setGeometry(0, 0, 500, 375)
        self.setMinimumSize(500, 375)

        self.setPage(PageEnum.StartPage, StartWizardPage(self))
        self.setPage(PageEnum.GetInfoPage, GetInfoWizardPage(self))
        self.setStartId(PageEnum.StartPage)


__all__ = ("MainWindow",)
