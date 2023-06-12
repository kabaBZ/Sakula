import requests

import os


from DownLoader import M3u8Downloader, DirectDownloader

from requests.packages import urllib3
from lxml import etree

# 关闭警告
urllib3.disable_warnings()


requests.FileModeWarning


class SakulaDownloader:
    def __init__(self, keyWord) -> None:
        if os.path.exists("./file.ts"):
            os.remove("./file.ts")
        self.keyword = keyWord

    def Search(self):
        json = {"m": "search", "c": "index", "a": "init", "q": self.keyword}
        res = requests.post(
            "http://www.yinghuacd.com/search/{}".format(self.keyword), json=json
        )
        result = etree.HTML(res.text)
        self.hrefs = result.xpath('.//div[@class="lpic"]//li')
        return self.hrefs[0]

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


if __name__ == "__main__":
    # MovieDownloader = SakulaDownloader("电锯")
    # MovieDownloader.StartFlow()
    from threading import Thread

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

    import threading

    for i in range(200):
        threading.Thread(target=say).start()

    # from multiprocessing import Process

    # for i in range(10):
    #     Process(target=say).start()
