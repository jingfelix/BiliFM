import json

from .util import request


class Fav:
    media_id = ""
    cookies = {}
    fav_url = "https://api.bilibili.com/x/v3/fav/resource/ids"

    id_list = []

    def __init__(self, media_id: str, cookies_str: str) -> None:
        if cookies_str is None or cookies_str is None:
            raise ValueError("Error: Params are Required")

        try:
            self.cookies = json.loads(cookies_str)
        except Exception as e:
            raise ValueError("Error: Cookies is not a json string")

        # 获取 id list

        params = {
            "media_id": media_id.replace("ml", ""),
            "platform": "web",
        }

        try:
            res = request(
                method="get",
                url=self.fav_url,
                params=params,
                cookies=self.cookies,
                wbi=False,
            )
        except Exception as e:
            raise Exception("Error: " + str(e))

        res_json = res.json()

        code = res_json.get("code", -400)

        if code != 0:
            raise ValueError("Error: " + res_json["message"])

        data = res_json["data"]
        for item in data:
            if item["type"] == 2:
                self.id_list.append(item["bvid"])
