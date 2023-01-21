# pylint:skip-file
from json import load
from os import environ, getcwd
from os.path import isfile, join
from pathlib import Path

_CONFIG_PATH = join(getcwd(), ".env.json")

psql = Path.home() / ".postgresql"
psql.mkdir(exist_ok=True)
loc = psql / "root.crt"


def setup_env() -> None:
    if isfile(_CONFIG_PATH):
        with open(_CONFIG_PATH, "r") as f:
            js: dict = load(f)
            environ.update(js)

    import os

    import requests

    if loc.exists():
        return
    c = requests.get(os.environ["C_DOWNLOAD_URL"], timeout=60)

    loc.write_bytes(c.content)


del join
del getcwd
