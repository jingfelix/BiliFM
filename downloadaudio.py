try:
    import os
    import requests
    import urllib
    import time
except ImportError:
    print("Module not found. Please check requirement.txt")


def getCidAndTitle(bvid: str, p: int = 1):
    """Get audio title and cid by BV id."""

    url = "https://api.bilibili.com/x/web-interface/view?bvid=" + bvid
    data = requests.get(url).json()["data"]
    title = data["title"]
    cid = data["pages"][p - 1]["cid"]
    return str(cid), title


def getInformation(bvid: str) -> list:
    """Deal with audio Bv id with several episode."""
    item = []
    if len(bvid) == 12:
        cid, title = getCidAndTitle(bvid)
        item.append(bvid)
    else:
        cid, title = getCidAndTitle(bvid[:12], int(bvid[13:]))
        item.append(bvid[:12])
    item.append(cid)
    item.append(title)

    return item


def getAudio(item: list, dire: str) -> None:
    """Use cid, bv to download audio."""
    baseUrl = "http://api.bilibili.com/x/player/playurl?fnval=16&"

    st = time.time()
    bvid, cid, title = item[0], item[1], item[2]
    url = baseUrl + "bvid=" + bvid + "&cid=" + cid

    audioUrl = requests.get(url).json()["data"]["dash"]["audio"][0]["baseUrl"]

    opener = urllib.request.build_opener()
    opener.addheaders = [
        (
            "User-Agent",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0",
        ),
        ("Accept", "*/*"),
        ("Accept-Language", "en-US,en;q=0.5"),
        ("Accept-Encoding", "gzip, deflate, br"),
        ("Range", "bytes=0-"),
        (
            "Referer",
            "https://api.bilibili.com/x/web-interface/view?bvid=" + bvid,
        ),
        ("Origin", "https://www.bilibili.com"),
        ("Connection", "keep-alive"),
    ]
    urllib.request.install_opener(opener)
    filename = os.path.join(dire, titleProcess(title)) + ".mp3"
    urllib.request.urlretrieve(url=audioUrl, filename=filename)
    ed = time.time()
    print(str(round(ed - st, 2)) + " seconds download finish:", title)
    

def titleProcess(title: str) -> str:
    """Process the title, avoiding unnormal naming on Windows."""
    replaceList = ["?", "\\", "*", "|", "<", ">", ":", "/", " "]
    for ch in title:
        if ch in replaceList:
            title = title.replace(ch, "-")

    return title
