# BiliFM

## Intro

An script to download all audios of the Bilibili uploader you love.  
下载指定up主全部或指定数量的视频音频。

- 基于 [bilibiliAudioDownloader](https://github.com/nuster1128/bilibiliAudioDownloader) 制作，添加了指定up主和单个音频的功能，完善了命令行参数。

- 新版本中已对代码进行了重构，不使用原 [bilibiliAudioDownloader](https://github.com/nuster1128/bilibiliAudioDownloader) 中的代码。保留原有功能的同时，方便适配新的API。

## Install

```bash
pip install BiliFM --upgrade
```

或在本地使用并安装依赖

```bash
pip install -r requirements.txt
```

## Usage

使用实例：

### uid 模式

```Bash
bilifm uid 261485584
```

```python
uid = "261485584" # uid 为up主的uid
```

### bv 模式

```bash
bilifm bv BV1k341187
```

```python
bvid = "BV1k341187" # bvid 是要下载的音频的视频bv号
```

### fav 模式

```bash
bilifm fav 69361944 cookies.json
```

```python
media_id = "69361954" # media_id 是收藏夹的 media_id，注意不要和 uid 弄混
cookies_path = "cookies.json" # cookies 为是保存 cookies 的文件路径，注意需要转换为 json
```

media_id 的获取：

![media_id](./assets/fav.png)

cookies 的获取：

在开发者工具的控制台中输入 `document.cookie`

cookies 转换为json：[在线 cookies 转换](https://uutool.cn/cookie2json/)

## Features

- ~~python 版本限制未知~~
  - 在函数定义时使用了类型注解，故不建议使用 3.5 以下版本

- 接口简洁方便调用

```python
@app.command()
def bv(bv: str):
    audio = Audio(bv)
    audio.download()


@app.command()
def uid(uid: str):
    user = User(uid)

    for video in user.videos:
        bv = video["bvid"]
        audio = Audio(bv)
        audio.download()

    typer.echo("Download complete")
```

## Issues

- 获取up主视频列表时会出现 UnicodeDecodeError，~~原因未知~~
  - 初步判断是网络不稳定所致，在稳定的网络环境下没有出现此问题
  - 暂时采用 try-except 跳过这一过程
- 在使用前需关闭代理

## Licence

- ~~bilibiliaudioDownloader 的作者没有选取许可证，暂时选择 MIT License~~
- bilibiliAudioDownloader 的作者已添加 GPL-3.0 License，故本项目亦修改为 GPL-3.0
