# 📻 BiliFM: Best BiliBili Audio Downloader

[![PyPI](https://img.shields.io/pypi/v/BiliFM?style=flat-square)](https://pypi.org/project/BiliFM/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/BiliFM?style=flat-square)](https://pypi.org/project/BiliFM/)
[![PyPI - License](https://img.shields.io/pypi/l/BiliFM?style=flat-square)](https://github.com/jingfelix/BiliFM/blob/main/LICENSE)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm-project.org)

## Intro

An script to download all audios of the Bilibili uploader you love.  
轻松下载指定up主全部或指定的视频音频。

- ~~基于 [bilibiliAudioDownloader](https://github.com/nuster1128/bilibiliAudioDownloader) 制作，添加了指定up主和单个音频的功能，完善了命令行参数。~~

- 新版本中已对代码进行了重构，不使用原 [bilibiliAudioDownloader](https://github.com/nuster1128/bilibiliAudioDownloader) 中的代码。保留原有功能的同时，方便适配新的API。

- 参照 [bilibili-API-Collection](https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/misc/sign/wbi.md) 的文档修复了 412 报错问题。

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

> **Note**  
bv 模式现已支持多 P 下载，使用方式和普通 bv 模式相同  
同理，其他模式的下载也支持分 P 视频

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
media_id = "69361954" # media_id 是收藏夹的 media_id，注意不要和 uid/fid 弄混
cookies_path = "cookies.json" # cookies 是保存 cookies 的文件路径，注意需要转换为 json
```

media_id 的获取：

![media_id](./assets/fav.png)

cookies 的获取：

- 在开发者工具的控制台中输入 `document.cookie`

- cookies 转换为 json：[在线 cookies 转换](https://uutool.cn/cookie2json/)

### season 模式

下载视频合集

```bash
bilifm season $uid $sid [OPTIONS]
```

- uid, sid 的获取:
  打开视频合集网页, 从 URL 中获取

https://space.bilibili.com/23263470/channel/collectiondetail?sid=1855309

例如上面链接, uid 为 23263470, sid 为 1855309 (目前 uid 可以随意填写)

```bash
bilifm season 23263470 1855309
```

- Options:
  - -o, --directory 选择音频保存地址

### series 模式

下载视频列表

```bash
bilifm series $uid $sid [OPTIONS]
```

- uid, sid 的获取:
  打开用户空间中的合集和列表, 找到列表点击更多, 然后从URL中获取

https://space.bilibili.com/488978908/channel/seriesdetail?sid=888434

例如上面链接, uid 为 488978908, sid 为 888434. 使用下面命令

```bash
bilifm series 488978908 888434
```

- Options:
  - -o, --directory 选择音频保存地址

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

- 获取 UP 主视频列表时会出现 UnicodeDecodeError，~~原因未知~~
  - 初步判断是网络不稳定所致，在稳定的网络环境下没有出现此问题
  - 暂时采用 try-except 跳过这一过程
- 在使用前需关闭代理

## Licence

- ~~bilibiliaudioDownloader 的作者没有选取许可证，暂时选择 MIT License~~
- bilibiliAudioDownloader 的作者已添加 GPL-3.0 License，故本项目亦修改为 GPL-3.0

## Thanks

感谢以下产品对 BiliFM 的赞助：

![https://www.jetbrains.com](https://camo.githubusercontent.com/830c8bd550b48827eb78c6ce81a378aeed729d8db4a8bdd460ee500db7bda0d8/68747470733a2f2f7265736f75726365732e6a6574627261696e732e636f6d2f73746f726167652f70726f64756374732f636f6d70616e792f6272616e642f6c6f676f732f6a625f6265616d2e737667)
