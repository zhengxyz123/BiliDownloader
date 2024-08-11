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

import sys

from PySide6.QtCore import QLibraryInfo, QLocale, QTranslator
from PySide6.QtWidgets import QApplication

import BiliDownloader.resources
from BiliDownloader.main import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    translator = QTranslator(app)
    if translator.load(
        f"qtbase_{QLocale.system().name()}",
        QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath),
    ):
        app.installTranslator(translator)
    translator = QTranslator(app)
    if translator.load(QLocale.system(), "", "", ":/translations"):
        app.installTranslator(translator)
    window = MainWindow()
    window.show()
    return app.exec()
