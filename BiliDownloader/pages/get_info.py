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
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QWizard,
    QWizardPage,
)

from BiliDownloader.pages import PageEnum
from BiliDownloader.utils import bilibili_api, sec2str


class GetInfoWizardPage(QWizardPage):
    def __init__(self, parent: QWizard | None = None) -> None:
        super().__init__(parent)
        self.setTitle(self.tr("Please enter the BV id of the video."))
        self.setSubTitle(
            self.tr(
                "Please follow the prompts and the program will "
                "automatically get related information."
            )
        )
        self._is_playlist = False

        self.main_layout = QGridLayout(self)
        self.bvid_edit = QLineEdit(self)
        self.bvid_edit.setPlaceholderText(self.tr("Please enter the BV id"))
        self.submit_button = QPushButton(self.tr("Submit"), self)
        self.title_label = QLabel(self.tr("Unknown"), self)
        self.title_label.setWordWrap(True)
        self.duration_label = QLabel(self.tr("Unknown"), self)
        self.main_layout.addWidget(
            QLabel(self.tr("BV id:")), 0, 0, Qt.AlignmentFlag.AlignRight
        )
        self.main_layout.addWidget(self.bvid_edit, 0, 1)
        self.main_layout.addWidget(self.submit_button, 0, 2)
        self.main_layout.addWidget(
            QLabel(self.tr("Title:")),
            1,
            0,
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight,
        )
        self.main_layout.addWidget(self.title_label, 1, 1, 1, 2)
        self.main_layout.addWidget(
            QLabel(self.tr("Duration:")), 2, 0, Qt.AlignmentFlag.AlignRight
        )
        self.main_layout.addWidget(self.duration_label, 2, 1, 1, 2)

        self.bvid_edit.textChanged.connect(self.disable_next)
        self.submit_button.clicked.connect(self.check_bvid)
        self.registerField("bvid*", self.bvid_edit)

    def cleanupPage(self) -> None:
        pass

    def isComplete(self) -> bool:
        if not super().isComplete():
            return False
        if self.duration_label.text() != self.tr("Unknown"):
            return True
        return False

    def nextId(self) -> int:
        if self._is_playlist:
            return PageEnum.PlaylistPage
        return PageEnum.SetInfoPage

    def check_bvid(self) -> None:
        bvid = self.bvid_edit.text()
        if not (len(bvid) == 12 and bvid.startswith("BV1")):
            return
        data = bilibili_api("GET", f"web-interface/view?bvid={bvid}")
        if data["code"] != 0:
            self.title_label.setText(self.tr("Unknown"))
            self.duration_label.setText(self.tr("Unknown"))
            self.completeChanged.emit()
            return
        self.title_label.setText(data["data"]["title"])
        duration = data["data"]["duration"]
        duration_text = sec2str(duration)
        if (n := data["data"]["videos"]) > 1:
            duration_text += self.tr(" (include {n} videos)").format(n=n)
            self._is_playlist = True
        else:
            self._is_playlist = False
        self.duration_label.setText(duration_text)
        self.completeChanged.emit()

    def disable_next(self):
        self.title_label.setText(self.tr("Unknown"))
        self.duration_label.setText(self.tr("Unknown"))
        self.completeChanged.emit()


__all__ = ("GetInfoWizardPage",)
