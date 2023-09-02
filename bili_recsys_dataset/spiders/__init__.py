import scrapy
from scrapy.http import HtmlResponse
from utils import CommentScraper
from urllib.parse import urlencode


class QuotesSpider(scrapy.Spider):
    name = "bili"
    start_urls = ["https://music.163.com/song?id=64443"]

    count = 0

    def parse(self, response: HtmlResponse, **kwargs):
        song_id_str = response.url.split("=")[1]
        name = response.xpath('//div[@class="tit"]/em/text()')[0].get()
        artists_list = response.xpath('//p[@class="des s-fc4"]/span/a/text()').getall()
        artists_id_list = response.xpath(
            '//p[@class="des s-fc4"]/span/a/@href'
        ).getall()
        artists_id_list = [int(i.split("=")[1]) for i in artists_id_list]
        yield {
            "name": name,
            "song_id": song_id_str,
            "artists_list": artists_list,
            "artists_id_list": artists_id_list,
        }

        helper = CommentScraper(song_id_str)
        url, headers, data = helper.get_commmet()
        yield scrapy.Request(
            url=url,
            callback=self.parse_comment,
            method="POST",
            headers=headers,
            body=urlencode(data),
            cb_kwargs={"helper": helper},
        )

        self.count += 1
        if self.count > 2:
            scrapy.Spider.close(self, f"count = {self.count}")

        a_list = response.xpath(
            '//ul[@class="m-sglist f-cb"]/li/div[@class="txt"]/div[@class="f-thide"]/a'
        )
        yield from response.follow_all(a_list)

    def parse_comment(self, response: HtmlResponse, **kwargs):
        helper: CommentScraper = kwargs["helper"]
        comment_data_list, cursor = helper.parse_json(response.json())
        yield {
            "json": comment_data_list,
            "song_id": helper.song_id,
        }
        url, headers, data = helper.get_commmet(cursor)
        if cursor != "-1":
            yield scrapy.Request(
                url=url,
                callback=self.parse_comment,
                method="POST",
                headers=headers,
                body=urlencode(data),
                cb_kwargs={"helper": helper},
            )
