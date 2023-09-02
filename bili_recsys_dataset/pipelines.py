# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import mariadb as db
from itemadapter.adapter import ItemAdapter
from twisted.internet.defer import passthru
from utils import CommentScraper


class BiliRecsysDatasetPipeline:
    dic = {
        "user": "z2z63",
        "password": "681769",
        "host": "localhost",
        "port": 3306,
        "database": "bili_recsys_dataset",
    }

    def open_spider(self, spider):
        self.connection = db.connect(**BiliRecsysDatasetPipeline.dic)
        if self.connection is None:
            raise Exception("Cannot connect to database")
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        if "artists_id_list" in item:
            for artist, artist_id in zip(item["artists_list"], item["artists_id_list"]):
                self.cursor.execute(
                    "INSERT IGNORE artist_song ( artist_163_id, song_163_id) VALUES (?, ?)",
                    (artist_id, item["song_id"]),
                )
                self.cursor.execute(
                    "INSERT IGNORE artist ( artist_163_id, name ) VALUES (?, ?) ",
                    (artist_id, artist),
                )
            self.cursor.execute(
                "INSERT IGNORE song ( song_163_id, name ) VALUES (?, ?) ",
                (item["song_id"], item["name"]),
            )

        else:
            comment_list = item["json"]
            for comment in comment_list:
                self.cursor.execute(
                    "INSERT IGNORE user_song (comment_163_id, user_163_id, song_163_id, content) VALUES (?, ?, ?, ?)",
                    (
                        comment["comment_id"],
                        comment["user_id"],
                        comment["song_id"],
                        comment["content"],
                    ),
                )
                self.cursor.execute(
                    "INSERT IGNORE user ( user_163_id, name)  VALUES (?,?)",
                    (comment["user_id"], comment["user_nickname"]),
                )
        self.connection.commit()

        return item
