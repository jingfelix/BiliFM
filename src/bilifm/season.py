"""download bilibili season archive, 视频合集下载"""

import typer

from .util import request


class Season:
    # api refer https://github.com/SocialSisterYi/bilibili-API-collect/blob/f9ee5c3b99335af6bef0d9d902101c565b3bea00/docs/video/collection.md
    season_url: str = (
        "https://api.bilibili.com/x/polymer/web-space/seasons_archives_list"
    )

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

        res = request(
            method="get", url=self.season_url, params=params, wbi=True, dm=True
        ).json()

        code = res.get("code", -404)
        if code != 0:
            # uid 错误好像无影响
            if code == "-404":
                typer.echo(f"Error: uid {self.uid} or sid {self.season_id} error.")
            else:
                type.echo("Error: unknown error")
            typer.echo(f"code: {res['code']}")
            if res.get("message", None):
                typer.echo(f"msg: {res['message']}")
            return False

        self.total = res["data"]["meta"]["total"]
        self.name = res["data"]["meta"]["name"]

        max_pn = self.total // 50
        for i in range(1, max_pn + 2):
            params["page_num"] = i

            res = request(
                method="get", url=self.season_url, params=params, wbi=True, dm=True
            ).json()
            bvids = [d["bvid"] for d in res["data"]["archives"]]
            self.videos.extend(bvids)

        return True
