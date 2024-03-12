import os
import sys
import time

import requests
import typer

from .util import get_signed_params


class Audio:
    bvid = ""
    title = ""
    playUrl = "http://api.bilibili.com/x/player/wbi/playurl"
    part_list = []

    headers = {}

    def __init__(self, bvid: str) -> None:
        if bvid is None:
            raise ValueError("bvid is None")

        self.bvid = bvid
        self.headers = {
            "authority": "api.bilibili.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "dnt": "1",
            "pragma": "no-cache",
            "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Referer": "https://www.bilibili.com/video/{bvid}".format(bvid=self.bvid),
        }

        # 获取cid和title
        if len(bvid) == 12:
            # BV号
            self.__get_cid_title(bvid)
        else:
            # AV号
            self.__get_cid_title(bvid[:12])

    def download(self):
        start_time = time.time()
        try:
            for cid, part in zip(self.cid_list, self.part_list):
                if len(self.part_list) > 1:
                    file_path = f"{self.title}-{part}.mp3"
                else:
                    file_path = f"{self.title}.mp3"

                if len(file_path) > 255:
                    file_path = file_path[:255]

                # 如果文件已存在，则跳过下载
                if os.path.exists(file_path):
                    typer.echo(f"{self.title} already exists, skip for now")
                    return

                params = get_signed_params(
                    {
                        "fnval": 16,
                        "bvid": self.bvid,
                        "cid": cid,
                    }
                )
                json = requests.get(
                    self.playUrl, params=params, headers=self.headers
                ).json()

                baseUrl = json["data"]["dash"]["audio"][0]["baseUrl"]

                response = requests.get(url=baseUrl, headers=self.headers, stream=True)

                total_size = int(response.headers.get("content-length", 0))
                temp_size = 0

                with open(file_path, "wb") as f:
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

        except Exception as e:
            typer.echo("Download failed")
            typer.echo("Error: " + str(e))
            pass

        end_time = time.time()

        sys.stdout.write(
            " " + str(round(end_time - start_time, 2)) + " seconds download finish\n"
        )

    def __get_cid_title(self, bvid: str):
        url = "https://api.bilibili.com/x/web-interface/view"
        params = {"bvid": bvid}

        try:
            response = requests.get(
                url=url,
                params=params,
                headers=self.headers,
            )
            data = response.json().get("data")
            self.title = self.__title_process(data.get("title"))

            # 这里是否也应该也使用get方法？
            self.cid_list = [str(page["cid"]) for page in data["pages"]]
            self.part_list = [
                self.__title_process(str(page["part"])) for page in data["pages"]
            ]

        except ValueError as e:
            raise e

        except Exception as e:
            raise e

    def __title_process(self, title: str):
        replaceList = ["?", "\\", "*", "|", "<", ">", ":", "/", " "]
        for ch in replaceList:
            title = title.replace(ch, "-")

        return title
