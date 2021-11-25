try:
    import os
    import click
    import urllib
    import time
    import downloadaudio
    from json import loads

except ImportError:
    print("Module not found. Please check requirement.txt")

jsonUrl = "https://api.bilibili.com/x/space/arc/search?mid={0}&ps=30&tid=0&pn={1}&keyword=&order=pubdate&jsonp=jsonp"
configPath = "./config.json"
workingPath = os.getcwd()


@click.group()
def main():
    pass


@click.command()
@click.argument("uid")
def uid(uid: str) -> None:
    """download audio with uid"""

    config = loadConfig()

    vd = os.path.join(workingPath, config["directory"])
    page = int(config["min-page"])  # define min page

    if not os.path.isdir(vd):
        os.mkdir(vd)

    while True:
        try:
            json_uid = loads(urllib.request.urlopen(jsonUrl.format(uid, page)).read())

            if json_uid["data"]["list"]["vlist"] == []:
                if page == 1:
                    return "uid 错误或该用户无投稿"
                else:
                    break

            for vinfo in json_uid["data"]["list"]["vlist"]:
                downloadaudio.getAudio(downloadaudio.getInformation(vinfo["bvid"]), vd)

            page += 1

        except UnicodeDecodeError:
            print("Download Complete!")
            break

    pass


@click.command()
@click.argument("bvid")
def bv(bvid: str) -> None:
    """download audio with BV id"""
    config = loadConfig()
    vd = os.path.join(workingPath, config["directory"])
    downloadaudio.getAudio(downloadaudio.getInformation(bvid), vd)


@click.command()
@click.argument("file")
def dirs(fileName: str) -> None:
    """Download audio by file with BV id list."""
    config = loadConfig()
    vd = os.path.join(workingPath, config["directory"])

    with open(fileName, "r") as f:
        BVlist = f.readlines()
        for bvid in BVlist:
            bvid = bvid.replace("\n", "")
            downloadaudio.getAudio(downloadaudio.getInformation(bvid), vd)


def loadConfig() -> dict:
    try:
        configFile = open(configPath, mode="r")
    except FileNotFoundError:
        print("config file not found!")
        return None

    config = loads(configFile.read())
    configFile.close()

    return config


main.add_command(uid)
main.add_command(bv)
main.add_command(dirs)

if __name__ == "__main__":
    st = time.time()
    main()
    ed = time.time()
    print("Download ALLFinish! Time consuming:", str(round(ed - st, 2)) + " seconds")


# TODO: 修改min_page的逻辑使之能下载某up的全部视频 DONE
# TODO: 检查是否已经下载，若已下载则不重复下载 NO
# TODO: 总下载时间的计数器 DONE
# TODO: 完整注释
# TODO: 针对下载的文件名进行适配操作系统的修改 DONE
# TODO: 按列表下载 DONE
# TODO: 彩色字符输出
# TODO: 音质选择
