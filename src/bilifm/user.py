import typer

from .util import get_w_webid, request


class User:
    uidUrl: str = "https://api.bilibili.com/x/space/wbi/arc/search"
    uid: str = ""
    videos: list = []

    def __init__(self, uid: str):
        self.uid = uid

        w_webid = get_w_webid(uid)

        params = {
            "mid": uid,
            "ps": 1,
            "tid": 0,
            "pn": 1,
            "order": "pubdate",
            "web_location": "333.999",
            "w_webid": w_webid,
        }

        response = request(
            method="get", url=self.uidUrl, params=params, wbi=True, dm=True
        )

        code = response.json().get("code", -400)

        if code != 0:
            typer.echo(f"Error: uid {uid} not found")
            raise typer.Exit(1)

        total = response.json()["data"]["page"]["count"]

        max_pn = total // 50
        surpus = total % 50

        # get all videos
        for i in range(1, max_pn + 2):
            ps = 50 if i != max_pn + 1 else surpus

            params = {
                "mid": uid,
                "ps": ps,
                "tid": 0,
                "pn": i,
                "order": "pubdate",
                "web_location": "333.999",
                "w_webid": w_webid,
            }

            response = request(
                method="get", url=self.uidUrl, params=params, wbi=True, dm=True
            )

            self.videos.extend(response.json()["data"]["list"]["vlist"])
