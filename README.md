# BiliFM-dev
**警告**：该分支下的脚本处于未测试状态，可能造成文件损坏
## Intro
An script to download all audios of the Bilibili uploader you love.  
下载指定up主全部或指定数量的视频音频
## Usage
使用实例：

### uid 模式

```Bash
python __main__.py uid 261485584
```
```python
uid = "261485584" # uid 为up主的uid
```
### bv 模式
```bash
python __main__.py bv BV1k341187
```
```python
bvid = "BV1k341187" # bvid 是要下载的音频的视频bv号
```
### list 模式
```bash
python __main__.py dirs ./list.txt
```
```python
file = "./list.txt" # file 是要下载的bv号目录文件
```

## Status quo
* python 版本限制未知

## Issues
* json解析在获取up主视频列表时会出现UnicodeDecodeError，原因未知
* 暂时采用try-except跳过这一过程
## Licence
* bilibiliaudioDownloader 的作者没有选取许可证，暂时选择 MIT License
