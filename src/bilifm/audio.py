import os
import time

import requests
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, DownloadColumn, Progress, TransferSpeedColumn

from .util import AudioQualityEnums, get_signed_params

console = Console()


class Audio:
    bvid = ""
    title = ""
    playUrl = "http://api.bilibili.com/x/player/wbi/playurl"
    part_list = []

    headers = {}

    def __init__(self, bvid: str, audio_quality: AudioQualityEnums) -> None:
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

        self.audio_quality = audio_quality.quality_id

        # 获取cid和title
        if len(bvid) == 12:
            # BV号
            self.__get_cid_title(bvid)
        else:
            # AnotherV号
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
                    console.print(
                        Panel(
                            f"{self.title} 已存在，跳过下载",
                            style="yellow",
                            expand=False,
                        )
                    )
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

                if json["data"] is None:
                    console.print(
                        Panel(
                            f"[bold red]数据字段无效[/bold red]\n"
                            f"URL: {self.playUrl}\n"
                            f"参数: {params}",
                            title="错误",
                            expand=False,
                        )
                    )
                    return

                audio = json["data"]["dash"]["audio"]
                if not audio:
                    console.print(
                        Panel(
                            f"[bold red]音频字段为空[/bold red]\n"
                            f"URL: {self.playUrl}\n"
                            f"参数: {params}",
                            title="错误",
                            expand=False,
                        )
                    )
                    return

                base_url = None
                for au in audio:
                    if au["id"] == self.audio_quality:
                        base_url = au["baseUrl"]

                # no audio url corresponding to current audio quality
                if base_url is None:
                    base_url = audio[0]["baseUrl"]

                response = requests.get(url=base_url, headers=self.headers, stream=True)

                total_size = int(response.headers.get("content-length", 0))

                with Progress(
                    "[progress.description]{task.description}",
                    BarColumn(),
                    "[progress.percentage]{task.percentage:>3.0f}%",
                    "•",
                    DownloadColumn(),
                    "•",
                    TransferSpeedColumn(),
                    console=console,
                ) as progress:
                    task = progress.add_task(
                        f"[cyan]下载 {self.title}", total=total_size
                    )

                    with open(file_path, "wb") as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                progress.update(task, advance=len(chunk))

                    # 添加下载完成的提示
                    end_time = time.time()
                    download_time = round(end_time - start_time, 2)
                    console.print(
                        Panel(
                            f"[bold green]下载完成！[/bold green]用时 {download_time} 秒",
                            expand=False,
                        )
                    )

        except Exception as e:
            console.print(
                Panel(
                    f"[bold red]下载失败[/bold red]\n错误: {str(e)}",
                    title="异常",
                    expand=False,
                )
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

            self.cid_list = [str(page.get("cid")) for page in data.get("pages", [])]
            self.part_list = [
                self.__title_process(str(page.get("part")))
                for page in data.get("pages", [])
            ]

        except Exception as e:
            console.print(
                Panel(
                    f"[bold red]获取视频信息失败[/bold red]\n错误: {str(e)}",
                    title="异常",
                    expand=False,
                )
            )
            raise

    def __title_process(self, title: str):
        replaceList = ["?", "\\", "*", "|", "<", ">", ":", "/", " "]
        for ch in replaceList:
            title = title.replace(ch, "-")

        return title
