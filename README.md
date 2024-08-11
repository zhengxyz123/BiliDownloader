# BiliDownloader
从 Bilibili 下载音频和视频。

## 下载&使用
先从 GitHub 下载该仓库：
```bash
git clone git@github.com:zhengxyz123/Bilidownloader.git --depth=1
```

创建并进入虚拟环境：
```bash
python3 -m venv .
. bin/active
```

下载依赖项：
```bash
pip install -r requirements.txt
```

运行：
```bash
python3 -m BiliDownloader
```

程序可能会使用到 `FFmpeg` 来处理音视频文件，请[下载之](https://ffmpeg.org/download.html)。

### Linux 用户可能还要做的事情
如果你使用 Fcitx5 输入法，那么你需要参考 *[Getting fcitx to work in a Python Qt application with virtualenv](https://blog.stefan-koch.name/2023/03/19/fcitx-python-qt-virtualenv)* 来复制一个文件使输入法工作。
