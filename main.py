import requests

import os
import re
import time
import random

from threading import Thread


from CrawlerStruct import SearchResult
from CrawlerAbs import CrawlerAbs, movie_queue


from requests.packages import urllib3
from lxml import etree


# 关闭警告
urllib3.disable_warnings()


class SakulaCrawler(CrawlerAbs):
    def __init__(self) -> None:
        CrawlerAbs.__init__(self)

    def Search(self, keyWord):
        json = {"m": "search", "c": "index", "a": "init", "q": keyWord}
        res = requests.post(
            "http://www.yinghuavideo.com/search/{}".format(keyWord), json=json
        )
        result = etree.HTML(res.text)

        resultHrefs = result.xpath('.//div[@class="lpic"]//li/a/@href')
        resultNames = result.xpath('.//div[@class="lpic"]//li/a/img/@alt')

        self.searchResult = SearchResult(resultNames, resultHrefs).data

    def Select_Movie(self):
        for result in self.searchResult:
            print("{}.{}".format(result["index"], result["name"]))

        while True:
            try:
                index = int(input()) - 1
                if index > len(self.searchResult):
                    print("请输入存在的序号")
                    continue
                break
            except ValueError:
                print("请输入数字序号")
        # index = 2

        self.targetHref = self.searchResult[index]["href"]
        self.targetName = self.searchResult[index]["name"]

    def Select_Ep(self):
        print("选择的电影为：{}".format(self.targetName))
        detail_page = requests.get("http://www.yinghuacd.com/" + self.targetHref)
        detail_page.encoding = "utf-8"

        Ep_page_res = etree.HTML(detail_page.text)
        Ep_hrefs = Ep_page_res.xpath('//div[@class="movurl"]/ul/li/a/@href')

        Ep_dic = {}
        for index, ep in enumerate(Ep_hrefs):
            Ep_dic.update({index + 1: "http://www.yinghuacd.com" + ep})

        for item in Ep_dic:
            print("EP" + str(item))

        targetEp = self.get_list_from_input()

        def get_m3u8_url(index):
            ep_page = requests.get(Ep_dic[index])
            ep_page.encoding = "utf-8"

            ep_m3u8_page_url = etree.HTML(ep_page.text).xpath(
                '//div[@id="playbox"]/@data-vid'
            )[0]
            a = requests.get(
                "https://tup.yinghuacd.com/", params={"vid": ep_m3u8_page_url}
            )
            a.encoding = "utf-8"

            m3u8_url = re.findall('url: "(.*?)",', a.text)[0]

            movie_queue.put({"ep": index, "m3u8": m3u8_url}, timeout=5)

        threads = []
        if -1 in targetEp:
            indexs = range(len(Ep_dic))
        else:
            indexs = targetEp
        for i in indexs:
            t = Thread(target=get_m3u8_url, args=(i + 1,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()


if __name__ == "__main__":
    MovieDownloader = SakulaCrawler()
    MovieDownloader.start()
