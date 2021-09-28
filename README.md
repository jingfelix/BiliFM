# BiliFM
## Intro
An script to download all videos of the Bilibili uploader you love.  
使用 Bilili 库的脚本，用于下载指定up主全部或指定数量的视频，并转换为音乐格式（是否转换可选）
## Usage
使用实例：
'''Bash
python 261485584 --save=0 --music=1 
'''
## Status quo
* python 版本应不低于3.8（Bilili库的要求）
* 需要安装 ffmpeg 并加入path
## Issues
* Linux下FFmpeg缺少mp3编码器
  * 可以依赖 libmp3lame 但会使使用成本上升不少
* win下，安装合理的第三方编译版可以避开这个问题（大概）
* requirement.txt对依赖库的描述不准确
## Licence
Bilili 采用 GPLv3，ffmpy 采用 MIT 依照 GPLv3 的要求，本项目采用 GPLv3.