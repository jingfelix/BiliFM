import requests
import typer


class User:
    uidUrl: str = "https://api.bilibili.com/x/space/arc/search"
    videos: list = []

    def __init__(self, uid: str):
        headers = {
            "authority": "api.bilibili.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        }

        params = {"mid": uid, "ps": 1, "tid": 0, "pn": 1, "order": "pubdate"}

        response = requests.get(self.uidUrl, params=params, headers=headers)

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

            response = requests.get(self.uidUrl, params=params, headers=headers)

            self.videos.extend(response.json()["data"]["list"]["vlist"])
