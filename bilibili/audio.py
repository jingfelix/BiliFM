import sys
import time

import requests
import typer


class Audio:
    bvid = ""
    cid = ""
    title = ""
    playUrl = "http://api.bilibili.com/x/player/playurl"
    baseUrl = ""

    def __init__(self, bvid: str) -> None:
        if bvid is None:
            raise ValueError("bvid is None")

        self.bvid = bvid

        # 获取cid和title
        if len(bvid) == 12:
            # BV号
            self.__get_cid_title(bvid)
        else:
            # AV号
            self.__get_cid_title(bvid[:12], int(bvid[13:]))

        params = {
            "fnval": 16,
            "bvid": self.bvid,
            "cid": self.cid,
        }

        self.baseUrl = requests.get(self.playUrl, params=params).json()["data"]["dash"][
            "audio"
        ][0]["baseUrl"]

    def download(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Range": "bytes=0-",
            "Origin": "https://www.bilibili.com",
            "Connection": "keep-alive",
            "Referer": "https://www.bilibili.com/video/{bvid}".format(bvid=self.bvid),
        }

        start_time = time.time()
        try:
            response = requests.get(url=self.baseUrl, headers=headers, stream=True)

            total_size = int(response.headers.get("content-length", 0))
            temp_size = 0

            with open(self.title + ".mp3", "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()

                        temp_size += len(chunk)
                        done = int(50 * temp_size / total_size)
                        sys.stdout.write(
                            "\r[%s%s] %s/%s %s"
                            % (
                                "#" * done,
                                "-" * (50 - done),
                                temp_size,
                                total_size,
                                self.title,
                            )
                        )
                        sys.stdout.flush()

        except:
            typer.echo("Download failed")
            pass

        end_time = time.time()

        sys.stdout.write(
            " " + str(round(end_time - start_time, 2)) + " seconds download finish\n"
        )

    def __get_cid_title(self, bvid: str, p: int = 1):
        url = "https://api.bilibili.com/x/web-interface/view?bvid={bvid}".format(
            bvid=bvid
        )
        try:
            response = requests.get(url)
            data = response.json().get("data")
            self.title = data.get("title")

            # 这里是否也应该也使用get方法？
            self.cid = str(data["pages"][p - 1]["cid"])

        except ValueError as e:
            raise e

        except Exception as e:
            raise e

        replaceList = ["?", "\\", "*", "|", "<", ">", ":", "/", " "]
        for ch in replaceList:
            self.title = self.title.replace(ch, "-")
