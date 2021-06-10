# -*- coding: utf-8 -*-
from io import BytesIO, SEEK_SET, SEEK_END
from urllib.parse import urlencode
from json import loads

import requests
from splitstream import splitfile

from rengu.store import RenguStore

ITER_SIZE = 65536

# From https://gist.github.com/obskyr/b9d4b4223e7eaf4eedcd9defabb34f13
class ResponseStream(object):
    def __init__(self, request_iterator):
        self._bytes = BytesIO()
        self._iterator = request_iterator

    def _load_all(self):
        self._bytes.seek(0, SEEK_END)
        for chunk in self._iterator:
            self._bytes.write(chunk)

    def _load_until(self, goal_position):
        current_position = self._bytes.seek(0, SEEK_END)
        while current_position < goal_position:
            try:
                current_position = self._bytes.write(next(self._iterator))
            except StopIteration:
                break

    def tell(self):
        return self._bytes.tell()

    def read(self, size=None):
        left_off_at = self._bytes.tell()
        if size is None:
            self._load_all()
        else:
            goal_position = left_off_at + size
            self._load_until(goal_position)

        self._bytes.seek(left_off_at)
        return self._bytes.read(size)

    def seek(self, position, whence=SEEK_SET):
        if whence == SEEK_END:
            self._load_all()
        else:
            self._bytes.seek(position, whence)


class RenguStoreHttp(RenguStore):
    """Rengu store over HTTP"""

    def __init__(self, name: str, extra: list[str]):
        self.uri = name
        self.extra = extra

    def __repr__(self):
        return f"RenguStoreHttp( {self.uri} )"

    def query(
        self,
        args: list[str],
        start: int = 0,
        count: int = -1,
        default_operator: str = "&",
        result: "RenguStoreHttp.ResultSet" = None,
    ):

        headers = {"Accept": "application/json", "Accept-Encoding": "gzip, deflate"}
        with requests.get(self.uri, {"q": args}, stream=True, headers=headers) as r:
            stream = ResponseStream(r.iter_content(ITER_SIZE))
            yield from (loads(j) for j in splitfile(stream, format="json"))
