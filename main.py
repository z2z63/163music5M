import json

import requests
import Crypto.Cipher.AES as AES
import base64
from pprint import pprint

url = "https://music.163.com/weapi/comment/resource/comments/get?csrf_token="
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    "(KHTML, like Gecko) Chrome/115.0.0.0"
    "Safari/537.36",
    "Referer": "https://music.163.com/song?id=1329938686",
    "Origin": "https://music.163.com",
    "Content-Type": "application/x-www-form-urlencoded",
}

i = "khL2YxfIYrPBissa"
key = (
    "b98fc371de4b4012fbbe64a04282f5b34b6b9a400998f1d5ec23a8c55fcac25d86e4eb6ff"
    "ce7a4d5ff48a228613fe3afe3e9d2db7720c4372349f7dc44bfb98027498efc5dfd828658"
    "53e88aa09ad2395f9ab17aa55c5ffdfbf1a313b88d170cb5d05d2613ccc2eb510dd3702aa"
    "477b8cfd3142c5cf230fa66e813af39192046"
)
e = "010001"
f = (
    "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab1"
    "7a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870"
    "114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97dd"
    "ef52741d546b8e289dc6935b3ece0462db0a22b8e7"
)
g = "0CoJUm6Qyw8W8jud"


def encrypt(text: str, enc_key: str) -> str:
    iv = "0102030405060708".encode()
    pad = 16 - len(text) % 16
    text += pad * chr(pad)
    encryptor = AES.new(enc_key.encode(), mode=AES.MODE_CBC, IV=iv)
    enc_bytes = encryptor.encrypt(text.encode())
    return base64.b64encode(enc_bytes).decode()


params = {
    "csrf_token": "",
    "cursor": "1693474272315",
    "offset": "0",
    "orderType": "2",
    "pageNo": "3",
    "pageSize": "100",
    "rid": "R_SO_4_1329938686",
    "threadId": "R_SO_4_1329938686",
}

data = {"params": encrypt(encrypt(json.dumps(params), g), i), "encSecKey": key}
resp = requests.post(url, headers=headers, data=data)

if resp.json()["code"] != 200:
    print(resp.json())
pprint(
    [
        {
            "content": obj["content"],
            "comment_id": obj["commentId"],
            "user_id": obj["user"]["userId"],
            "user_nickname": obj["user"]["nickname"],
            "song_id": "1329938686",
        }
        for obj in resp.json()["data"]["comments"]
    ]
)
