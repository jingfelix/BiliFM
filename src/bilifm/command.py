import os

import typer
from typing_extensions import Annotated

from .audio import Audio
from .fav import Fav
from .season import Season
from .user import User

app = typer.Typer()


@app.command()
def bv(bv: str):
    audio = Audio(bv)
    audio.download()


@app.command()
def uid(uid: str):
    user = User(uid)

    for video in user.videos:
        bv = video["bvid"]
        audio = Audio(bv)
        audio.download()

    typer.echo("Download complete")


@app.command()
def fav(media_id: str, cookies_path: str):
    with open(cookies_path, "r") as f:
        cookies = f.read()

    fav = Fav(media_id, cookies)

    for bvid in fav.id_list:
        audio = Audio(bvid)
        audio.download()

    typer.echo("Download complete")


@app.command()
def season(
    uid: str,
    sid: str,
    directory: Annotated[str, typer.Option("-o", "--directory")] = "",
):
    sea = Season(uid, sid)
    ret = sea.get_videos()
    if not ret:
        typer.Exit(1)
        return

    if directory:
        os.chdir(directory)

    if not os.path.isdir(sea.name):
        os.makedirs(sea.name)
    os.chdir(sea.name)

    for id in sea.videos:
        audio = Audio(id)
        audio.download()
    typer.echo("Download complete")
