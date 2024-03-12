import typer

from .util import request


class User:
    uidUrl: str = "https://api.bilibili.com/x/space/wbi/arc/search"
    videos: list = []

    def __init__(self, uid: str):
        params = {"mid": uid, "ps": 1, "tid": 0, "pn": 1, "order": "pubdate"}

        response = request(
            method="get", url=self.uidUrl, params=params, wbi=True, dm=True
        )

        code = response.json().get("code", -400)

        if code != 0:
            typer.echo(f"Error: uid {uid} not found")
            return

        total = response.json()["data"]["page"]["count"]

        max_pn = total // 50
        surpus = total % 50

        # get all videos
        for i in range(1, max_pn + 2):
            ps = 50 if i != max_pn + 1 else surpus

            params = {"mid": uid, "ps": ps, "tid": 0, "pn": i, "order": "pubdate"}

            response = request(
                method="get", url=self.uidUrl, params=params, wbi=True, dm=True
            )

            self.videos.extend(response.json()["data"]["list"]["vlist"])
