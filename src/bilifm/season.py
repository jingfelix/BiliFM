"""download bilibili season archive, 视频合集下载"""

import typer

from .util import Retry, request

headers: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Referer": "https://www.bilibili.com",
}


class Season:
    # api refer https://github.com/SocialSisterYi/bilibili-API-collect/blob/f9ee5c3b99335af6bef0d9d902101c565b3bea00/docs/video/collection.md
    season_url: str = (
        "https://api.bilibili.com/x/polymer/web-space/seasons_archives_list"
    )
    retry = 3

    def __init__(self, uid: str, sid: str, page_size=30) -> None:
        self.uid = uid
        self.season_id = sid
        self.page_size = page_size
        self.videos = []

    def get_videos(self):
        params = {
            "mid": self.uid,
            "season_id": self.season_id,
            "sort_reverse": False,
            "page_num": 1,
            "page_size": self.page_size,
        }

        @Retry(self.__response_succeed, self.__handle_error_response)
        def wrapped_request():
            """wrap request with retry"""
            return request(
                method="get", url=self.season_url, params=params, headers=headers
            ).json()

        res = wrapped_request()
        if res is None:
            return False

        self.total = res["data"]["meta"]["total"]
        self.name = res["data"]["meta"]["name"]

        def bvid_generator():
            max_pn = self.total // self.page_size
            for i in range(1, max_pn + 2):
                params["page_num"] = i
                res = wrapped_request()
                if res:
                    bvids = [d["bvid"] for d in res["data"]["archives"]]
                    # self.videos.extend(bvids)
                    yield bvids
                else:
                    typer.echo(
                        f"skip audios from {(i-1)* self.page_size} to {i * self.page_size}"
                    )

        return bvid_generator()

    def __handle_error_response(self, response):
        code = response.get("code", -404)
        if code == -404:
            typer.echo(f"Error: uid {self.uid} or sid {self.season_id} error.")
        elif code == -352:
            typer.echo(
                "Error: Authentication problem or too many requests, please try again later."
            )
        else:
            typer.echo("Error: Unknown problem.")

        typer.echo(f"code: {response['code']}")
        if response.get("message", None):
            typer.echo(f"msg: {response['message']}")

    def __response_succeed(self, response):
        return response.get("code", -404) == 0
