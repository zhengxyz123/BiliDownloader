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

import os
import shutil
import stat
import webbrowser

from PySide6.QtWidgets import (
    QFileDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QWizard,
    QWizardPage,
)

from BiliDownloader.pages import PageEnum


class StartWizardPage(QWizardPage):
    def __init__(self, parent: QWizard | None = None) -> None:
        super().__init__(parent)
        self.setTitle(self.tr("Welcome to use BiliDownloader!"))
        self.setSubTitle(
            self.tr(
                "In the first step, downloader will check that several external programs are installed."
            )
        )

        self.dialog = QFileDialog(self)
        self.dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.main_layout = QGridLayout(self)

        self.ffmpeg_path_edit = QLineEdit(self)
        self.ffmpeg_path_edit.setPlaceholderText(
            self.tr("Input the location of FFmpeg")
        )
        self.browse_ffmpeg_button = QPushButton(self.tr("Browse..."), self)
        self.ffmpeg_download_label = QLabel(
            self.tr("<a href='https://ffmpeg.org/download.html'>Download FFmpeg</a>")
        )
        self.main_layout.addWidget(QLabel(self.tr("FFmpeg:")), 0, 0)
        self.main_layout.addWidget(self.ffmpeg_path_edit, 0, 1)
        self.main_layout.addWidget(self.browse_ffmpeg_button, 0, 2)
        self.main_layout.addWidget(self.ffmpeg_download_label, 1, 1)

        self.browse_ffmpeg_button.clicked.connect(self.browse_ffmpeg)
        self.ffmpeg_download_label.linkActivated.connect(
            lambda url: webbrowser.open_new_tab(url)
        )
        self.registerField("ffmpeg_path*", self.ffmpeg_path_edit)

    def initializePage(self) -> None:
        exec_path = shutil.which("ffmpeg")
        if exec_path:
            self.ffmpeg_path_edit.setText(exec_path)

    def isComplete(self) -> bool:
        if not super().isComplete():
            return False
        if not os.path.isfile(self.ffmpeg_path_edit.text()):
            return False
        if os.stat(self.ffmpeg_path_edit.text()).st_mode & stat.S_IXUSR:
            return True
        return False

    def nextId(self) -> int:
        return PageEnum.GetInfoPage

    def browse_ffmpeg(self) -> None:
        file_name, _ = self.dialog.getOpenFileName()
        if len(file_name) > 0:
            self.ffmpeg_path_edit.setText(file_name)


__all__ = ("StartWizardPage",)
