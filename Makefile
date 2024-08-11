i18n_files := i18n/zh_CN.ts

py_files := BiliDownloader/main.py
py_files += BiliDownloader/pages/get_info.py
py_files += BiliDownloader/pages/playlist.py
py_files += BiliDownloader/pages/set_info.py
py_files += BiliDownloader/pages/start.py

.PHONY: clean

lupdate: $(py_files)
	@pyside6-lupdate $(py_files) -ts i18n/zh_CN.ts

lrelease: $(i18n_files)
	@pyside6-lrelease i18n/zh_CN.ts -qm i18n/zh_CN.qm

rcc: resources.qrc
	@pyside6-rcc resources.qrc -o BiliDownloader/resources.py

clean:
	-@rm -r dist/ build/ *.spec i18n/*.qm
