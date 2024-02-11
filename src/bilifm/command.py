import typer

from bilifm.audio import Audio
from bilifm.fav import Fav
from bilifm.user import User

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
