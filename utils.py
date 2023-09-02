import json
import Crypto.Cipher.AES as AES
import base64

from typing import List, Dict, Tuple
import requests


class CommentScraper:
    i = "khL2YxfIYrPBissa"
    key = (
        "b98fc371de4b4012fbbe64a04282f5b34b6b9a400998f1d5ec23a8c55fcac25d86e4eb6ff"
        "ce7a4d5ff48a228613fe3afe3e9d2db7720c4372349f7dc44bfb98027498efc5dfd828658"
        "53e88aa09ad2395f9ab17aa55c5ffdfbf1a313b88d170cb5d05d2613ccc2eb510dd3702aa"
        "477b8cfd3142c5cf230fa66e813af39192046"
    )
    page_size = 100

    params = {
        "csrf_token": "",
        "cursor": "-1",
        "offset": "0",
        "orderType": "2",
        "pageNo": "1",
        "pageSize": str(page_size),
        "rid": "",
        "threadId": "",
    }
    g = "0CoJUm6Qyw8W8jud"
    url = "https://music.163.com/weapi/comment/resource/comments/get?csrf_token="

    def __init__(self, song_id: str) -> None:
        self.song_id = song_id
        self.page_no = 0
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
            "(KHTML, like Gecko) Chrome/115.0.0.0"
            "Safari/537.36",
            "Referer": "",
            "Origin": "https://music.163.com",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def get_commmet(
        self, cursor_: str = "-1"
    ) -> Tuple[str, Dict[str, str], Dict[str, str]]:
        cls = CommentScraper
        self.headers["Referer"] = "https://music.163.com/song?id=" + self.song_id
        cls.params["rid"] = "R_SO_4_" + self.song_id
        cls.params["threadId"] = "R_SO_4_" + self.song_id
        cls.params["cursor"] = str(cursor_)

        cls.params.update(
            {
                "pageNO": str(self.page_no),
            }
        )
        data = {
            "params": cls._encrypt(
                cls._encrypt(
                    json.dumps(cls.params),
                    cls.g,
                ),
                cls.i,
            ),
            "encSecKey": cls.key,
        }
        self.page_no += 1
        return cls.url, self.headers, data

    @staticmethod
    def _encrypt(text: str, enc_key: str) -> str:
        iv = "0102030405060708".encode()
        pad = 16 - len(text) % 16
        text += pad * chr(pad)
        encryptor = AES.new(enc_key.encode(), mode=AES.MODE_CBC, IV=iv)
        enc_bytes = encryptor.encrypt(text.encode())
        return base64.b64encode(enc_bytes).decode()

    def parse_json(self, json_) -> Tuple[List[Dict[str, str]], str]:
        if json_["code"] != 200 or json_["data"]["comments"] == []:
            print(json_)
            return [], "-1"

        return [
            {
                "content": obj["content"],
                "comment_id": obj["commentId"],
                "user_id": obj["user"]["userId"],
                "user_nickname": obj["user"]["nickname"],
                "song_id": self.song_id,
            }
            for obj in json_["data"]["comments"]
        ], json_["data"]["cursor"]


if __name__ == "__main__":
    from pprint import pprint
    import requests

    song_id = "1329938686"
    scraper = CommentScraper(song_id)

    cursor = "-1"
    for i in range(5):
        url, headers, data = scraper.get_commmet(cursor)
        resp = requests.post(url, headers=headers, data=data)
        data_list, cursor = scraper.parse_json(resp.json())
        pprint(data_list[-1])
        print("-" * 20)
