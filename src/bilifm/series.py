"""download bilibili video series, 视频列表"""

import typer

from .util import Retry, request


class Series:
    series_url: str = "https://api.bilibili.com/x/series/archives"
    retry: int = 3

    def __init__(self, uid: str, series_id: str, page_size=30) -> None:
        self.uid = uid
        self.series_id = series_id
        self.page_size = page_size
        self.videos = []
        self.total = 0

    def get_videos(self):
        """return a generator that contain page_size videos"""
        params = {
            "mid": self.uid,
            "series_id": self.series_id,
            "pn": 1,
            "ps": self.page_size,
            "current_id": self.uid,
        }

        @Retry(self.__response_succeed, self.__handle_error_response)
        def wrapped_request():
            """wrap request with retry"""
            return request(method="get", url=self.series_url, params=params).json()

        res = wrapped_request()
        if res is None:
            return 0

        self.total = res["data"]["page"]["total"]

        def bvid_generator():
            for i in range(1, self.total // self.page_size + 2):
                params["pn"] = i
                res = wrapped_request()
                if res:
                    bvids = [ar["bvid"] for ar in res["data"]["archives"]]
                    # self.videos.extend(bvids)
                    yield bvids
                else:
                    typer.echo(
                        f"skip audios from {(i-1)* self.page_size} to {i * self.page_size}"
                    )

        return bvid_generator()

    def __handle_error_response(self, response):
        try:
            archives = response["data"]["archives"]
        except KeyError:
            archives = 0  # something null not none
        if archives is None:
            typer.echo(f"Error: uid {self.uid} or sid {self.series_id} error.")
        else:
            typer.echo("Error: Unknown problem.")
        typer.echo(f"resp: {response}")

    def __response_succeed(self, response) -> bool:
        try:
            return response["data"]["archives"] is not None
        except KeyError:
            return False
