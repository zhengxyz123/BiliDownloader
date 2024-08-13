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

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpacerItem,
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
                "In the first step, the downloader will ask you to enter some information."
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
        self.ffmpeg_download_label.setOpenExternalLinks(True)
        self.bili_jct_edit = QLineEdit(self)
        self.DedeUserID_edit = QLineEdit(self)
        self.DedeUserID__ckMd5_edit = QLineEdit(self)
        self.SESSDATA_edit = QLineEdit(self)
        self.sid_edit = QLineEdit(self)
        self.cookies_notes_label = QLabel(
            self.tr(
                "If you want to use cookies, all five of the above input boxes must be filled in. "
                "To get them, you have to log in <a href='https://bilibili.com'>bilibili.com</a> "
                "and get them from DevTools."
            ),
            self,
        )
        self.cookies_notes_label.setOpenExternalLinks(True)
        self.cookies_notes_label.setWordWrap(True)
        self.main_layout.addWidget(
            QLabel(self.tr("<big><b>External Program</b></big>")),
            0,
            0,
            1,
            3,
            Qt.AlignmentFlag.AlignCenter,
        )
        self.main_layout.addWidget(
            QLabel(self.tr("FFmpeg:")), 1, 0, Qt.AlignmentFlag.AlignRight
        )
        self.main_layout.addWidget(self.ffmpeg_path_edit, 1, 1)
        self.main_layout.addWidget(self.browse_ffmpeg_button, 1, 2)
        self.main_layout.addWidget(self.ffmpeg_download_label, 2, 1)
        self.main_layout.addItem(QSpacerItem(1, 10), 3, 0, 1, 3)
        self.main_layout.addWidget(
            QLabel(self.tr("<big><b>Cookies</b></big>")),
            4,
            0,
            1,
            3,
            Qt.AlignmentFlag.AlignCenter,
        )
        self.main_layout.addWidget(
            QLabel(self.tr("bili_jct:")), 5, 0, Qt.AlignmentFlag.AlignRight
        )
        self.main_layout.addWidget(self.bili_jct_edit, 5, 1, 1, 2)
        self.main_layout.addWidget(
            QLabel(self.tr("DedeUserID:")), 6, 0, Qt.AlignmentFlag.AlignRight
        )
        self.main_layout.addWidget(self.DedeUserID_edit, 6, 1, 1, 2)
        self.main_layout.addWidget(
            QLabel(self.tr("DedeUserID__ckMd5:")), 7, 0, Qt.AlignmentFlag.AlignRight
        )
        self.main_layout.addWidget(self.DedeUserID__ckMd5_edit, 7, 1, 1, 2)
        self.main_layout.addWidget(
            QLabel(self.tr("SESSDATA:")), 8, 0, Qt.AlignmentFlag.AlignRight
        )
        self.main_layout.addWidget(self.SESSDATA_edit, 8, 1, 1, 2)
        self.main_layout.addWidget(
            QLabel(self.tr("sid:")), 9, 0, Qt.AlignmentFlag.AlignRight
        )
        self.main_layout.addWidget(self.sid_edit, 9, 1, 1, 2)
        self.main_layout.addWidget(self.cookies_notes_label, 10, 1, 1, 2)

        self.browse_ffmpeg_button.clicked.connect(self.browse_ffmpeg)
        self.bili_jct_edit.textChanged.connect(self.completeChanged)
        self.DedeUserID_edit.textChanged.connect(self.completeChanged)
        self.DedeUserID__ckMd5_edit.textChanged.connect(self.completeChanged)
        self.SESSDATA_edit.textChanged.connect(self.completeChanged)
        self.sid_edit.textChanged.connect(self.completeChanged)
        self.registerField("ffmpeg_path*", self.ffmpeg_path_edit)
        self.registerField("cookies_bili_jct", self.bili_jct_edit)
        self.registerField("cookies_DedeUserID", self.DedeUserID_edit)
        self.registerField("cookies_DedeUserID__ckMd5", self.DedeUserID__ckMd5_edit)
        self.registerField("cookies_SESSDATA", self.SESSDATA_edit)
        self.registerField("cookies_sid", self.sid_edit)

    def initializePage(self) -> None:
        exec_path = shutil.which("ffmpeg")
        if exec_path:
            self.ffmpeg_path_edit.setText(exec_path)

    def isComplete(self) -> bool:
        if not super().isComplete():
            return False
        if not os.path.isfile(self.ffmpeg_path_edit.text()):
            return False
        if not os.stat(self.ffmpeg_path_edit.text()).st_mode & stat.S_IXUSR:
            return False
        cookies = [
            self.bili_jct_edit.text(),
            self.DedeUserID_edit.text(),
            self.DedeUserID__ckMd5_edit.text(),
            self.SESSDATA_edit.text(),
            self.sid_edit.text(),
        ]
        if not (any(cookies) and not all(cookies)):
            return True
        return False

    def nextId(self) -> int:
        return PageEnum.GetInfoPage

    def browse_ffmpeg(self) -> None:
        file_name, _ = self.dialog.getOpenFileName()
        if len(file_name) > 0:
            self.ffmpeg_path_edit.setText(file_name)


__all__ = ("StartWizardPage",)
