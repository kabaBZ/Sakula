import requests

import os
import re
import time
import random

from threading import Thread, local
from DownLoader import M3u8Downloader, DirectDownloader

from requests.packages import urllib3
from lxml import etree
from queue import Queue

# 关闭警告
urllib3.disable_warnings()


movie_queue = Queue()
thread_data = local()
m3u8_dic = {}


class SakulaDownloader:
    def __init__(self, keyWord) -> None:
        if os.path.exists("./file.ts"):
            os.remove("./file.ts")
        self.keyword = keyWord
        self.m3u8_dic = {}

    def Search(self):
        json = {"m": "search", "c": "index", "a": "init", "q": self.keyword}
        res = requests.post(
            "http://www.yinghuacd.com/search/{}".format(self.keyword), json=json
        )
        result = etree.HTML(res.text)

        self.hrefs = result.xpath('.//div[@class="lpic"]//li/a/@href')
        # todo 增加选择
        detail_page = requests.get("http://www.yinghuacd.com/" + self.hrefs[0])
        detail_page.encoding = "utf-8"

        Ep_page_res = etree.HTML(detail_page.text)
        Ep_hrefs = Ep_page_res.xpath('//div[@class="movurl"]/ul/li/a/@href')

        Ep_dic = {}
        for index, ep in enumerate(Ep_hrefs):
            Ep_dic.update({index + 1: "http://www.yinghuacd.com" + ep})

        def get_m3u8_url(thread_data, index):
            ep_page = requests.get(Ep_dic[index])
            ep_page.encoding = "utf-8"

            ep_m3u8_page_url = etree.HTML(ep_page.text).xpath(
                '//div[@id="playbox"]/@data-vid'
            )[0]
            a = requests.get(
                "https://tup.yinghuacd.com/", params={"vid": ep_m3u8_page_url}
            )
            a.encoding = "utf-8"

            m3u8_url = re.findall('url: "(.*?)",', a.text)
            # self.m3u8_dic.update({index: m3u8_url})

            movie_queue.put(m3u8_url, timeout=5)

        # todo 增加选择ep
        threads = []
        for i in range(len(Ep_dic)):
            t = Thread(target=get_m3u8_url, args=(thread_data, i + 1))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        def download_start(m3u8):
            d = M3u8Downloader(m3u8)
            d.start(random.randint(1, int(time.time())))

        download_thread = []
        while movie_queue.not_empty:
            t = Thread(target=download_start, args=(movie_queue.get()))
            t.start()
            download_thread.append(t)

        for thread in download_thread:
            thread.join()

        # with open("1.html", "w", encoding="utf-8") as f:
        #     f.write(a.text)

        # return self.hrefs[0]

    def SelectMovie(self):
        """
        选择序号、翻页、获取页面url
        """
        pass

    def Veryfy_mode(self):
        """
        根据页面内容判断模式、获取下载页面url或m3u8url、初始化下载器
        """
        # self.downloader = DirectDownloader("http://1.com")
        self.downloader = M3u8Downloader("5bb488554e08465a4b57a4ec59852800.m3u8")

    def StartFlow(self):
        self.Search()
        self.Veryfy_mode()
        self.downloader.start()


def say():
    while True:
        sum = 0
        for i in range(10000000):
            sum += i
        print(sum)

    # import threading

    # for i in range(200):
    #     threading.Thread(target=say).start()

    # from multiprocessing import Process

    # for i in range(10):
    #     Process(target=say).start()


if __name__ == "__main__":
    MovieDownloader = SakulaDownloader("电锯")
    MovieDownloader.StartFlow()
    # from threading import Thread

    # downloader1 = M3u8Downloader("635dab19a4c1e3a67af1c436d72380f0.m3u8")
    # downloader2 = M3u8Downloader("5bb488554e08465a4b57a4ec59852800.m3u8")
    # downloader3 = M3u8Downloader("44ead71f598d95d8fc5ca60d2040ba19.m3u8")
    # t1 = Thread(target=downloader1.start, kwargs={"name": 1})
    # t2 = Thread(target=downloader2.start, kwargs={"name": 2})
    # t3 = Thread(target=downloader3.start, kwargs={"name": 3})
    # t1.start()
    # t2.start()
    # t3.start()
    # t1.join()
    # t2.join()
    # t3.join()
