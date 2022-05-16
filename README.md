# BiliFM

## Intro

An script to download all audios of the Bilibili uploader you love.  
下载指定up主全部或指定数量的视频音频，基于[bilibiliAudioDownloader](https://github.com/nuster1128/bilibiliAudioDownloader)制作，添加了指定up主和单个音频的功能，完善了命令行参数

## Usage

使用实例：

### uid 模式

```Bash
python main.py uid 261485584
```

```python
uid = "261485584" # uid 为up主的uid
```

### bv 模式

```bash
python main.py bv BV1k341187
```

```python
bvid = "BV1k341187" # bvid 是要下载的音频的视频bv号
```

### list 模式

```bash
python main.py dirs ./list.txt
```

```python
file = "./list.txt" # file 是要下载的bv号目录文件
```

## Status quo

* ~~python 版本限制未知~~
  * 在函数定义时使用了类型注解，故不建议使用3.5以下版本

## Issues

* json解析在获取up主视频列表时会出现UnicodeDecodeError，~~原因未知~~
  * 初步判断是网络不稳定所致，在稳定的网络环境下没有出现此问题
  * 暂时采用try-except跳过这一过程
* 在使用前需关闭代理

## Licence

* ~~bilibiliaudioDownloader 的作者没有选取许可证，暂时选择 MIT License~~
* bilibiliAudioDownloader的作者已添加GPL-3.0 License，故本项目亦修改为GPL-3.0
