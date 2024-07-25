import os
import random
import time
import urllib.parse
from enum import Enum
from functools import reduce
from hashlib import md5
from typing import Callable

import requests
import typer
from typing_extensions import Annotated

HEADERS = {
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
    "Referer": "https://www.bilibili.com/",
}

mixinKeyEncTab = [
    46,
    47,
    18,
    2,
    53,
    8,
    23,
    32,
    15,
    50,
    10,
    31,
    58,
    3,
    45,
    35,
    27,
    43,
    5,
    49,
    33,
    9,
    42,
    19,
    29,
    28,
    14,
    39,
    12,
    38,
    41,
    13,
    37,
    48,
    7,
    16,
    24,
    55,
    40,
    61,
    26,
    17,
    0,
    1,
    60,
    51,
    30,
    4,
    22,
    25,
    54,
    21,
    56,
    59,
    6,
    63,
    57,
    62,
    11,
    36,
    20,
    34,
    44,
    52,
]


# 音质映射到具体值
audio_quality_map = {
    "64": 30216,
    "132": 30232,
    "192": 30280,
}


class AudioQualityEnums(str, Enum):
    k64 = "64"
    k132 = "132"
    k192 = "192"

    @property
    def quality_id(self):
        return audio_quality_map[self._value_]


def getMixinKey(orig: str):
    "对 imgKey 和 subKey 进行字符顺序打乱编码"
    return reduce(lambda s, i: s + orig[i], mixinKeyEncTab, "")[:32]


def encWbi(params: dict, img_key: str, sub_key: str):
    "为请求参数进行 wbi 签名"
    mixin_key = getMixinKey(img_key + sub_key)
    curr_time = round(time.time())
    params["wts"] = curr_time  # 添加 wts 字段
    params = dict(sorted(params.items()))  # 按照 key 重排参数
    # 过滤 value 中的 "!'()*" 字符
    params = {
        k: "".join(filter(lambda chr: chr not in "!'()*", str(v)))
        for k, v in params.items()
    }
    query = urllib.parse.urlencode(params)  # 序列化参数
    wbi_sign = md5((query + mixin_key).encode()).hexdigest()  # 计算 w_rid
    params["w_rid"] = wbi_sign
    return params


def getWbiKeys() -> tuple[str, str]:
    "获取最新的 img_key 和 sub_key"
    resp = requests.get("https://api.bilibili.com/x/web-interface/nav", headers=HEADERS)
    resp.raise_for_status()
    json_content = resp.json()
    img_url: str = json_content["data"]["wbi_img"]["img_url"]
    sub_url: str = json_content["data"]["wbi_img"]["sub_url"]
    img_key = img_url.rsplit("/", 1)[1].split(".")[0]
    sub_key = sub_url.rsplit("/", 1)[1].split(".")[0]
    return img_key, sub_key


def get_signed_params(params: dict):
    img_key, sub_key = getWbiKeys()
    return encWbi(params, img_key, sub_key)


def gen_dm_args(params: dict):
    """reference: https://github.com/SocialSisterYi/bilibili-API-collect/issues/868"""

    dm_rand = "ABCDEFGHIJK"
    dm_img_list = "[]"
    dm_img_str = "".join(random.sample(dm_rand, 2))
    dm_cover_img_str = "".join(random.sample(dm_rand, 2))
    dm_img_inter = '{"ds":[],"wh":[0,0,0],"of":[0,0,0]}'

    params.update(
        {
            "dm_img_list": dm_img_list,
            "dm_img_str": dm_img_str,
            "dm_cover_img_str": dm_cover_img_str,
            "dm_img_inter": dm_img_inter,
        }
    )

    return params


def request(
    method: str,
    url: str,
    params: dict = None,
    wbi: bool = False,
    dm: bool = False,
    headers: dict = HEADERS,
    **kwargs,
) -> requests.Response:
    if dm and params is not None:
        params = gen_dm_args(params)
    if wbi and params is not None:
        params = get_signed_params(params)

    return requests.request(method, url, params=params, headers=headers, **kwargs)


def change_directory(directory: str):
    if directory:
        if not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.isdir(directory):
            raise typer.BadParameter(f"{directory} is not a directory")

        os.chdir(directory)


def check_path(path: str):
    if not os.path.exists(path):
        raise typer.BadParameter(f"{path} does not exist")
    return path


Directory = Annotated[str, typer.Option("-o", "--directory", callback=change_directory)]
Path = typer.Argument(callback=check_path)


class Retry:
    """Retry decorator"""

    def __init__(self, response_succeed, handle_error_response, total=3) -> None:
        self.total = total
        self.__response_succeed = response_succeed
        self.__handle_error_response = handle_error_response
        pass

    def __call__(self, request_func: Callable) -> Callable:
        def wrapped_request(*args, **kwargs):
            for _ in range(self.total):
                res = request_func(*args, **kwargs)
                if self.__response_succeed(res):
                    return res
            self.__handle_error_response(res)
            return None

        return wrapped_request


AudioQuality = Annotated[
    AudioQualityEnums,
    typer.Option("--quality", "-q", help="audio quality", case_sensitive=False),
]
