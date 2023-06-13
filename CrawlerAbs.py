from abc import abstractmethod
from DownLoader import M3u8Downloader, DirectDownloader
from queue import Queue
from threading import Thread
import shutil
import os

G_Temp_path = os.getcwd() + "\\Temp\\"

movie_queue = Queue()


class CrawlerAbs:
    def __init__(self) -> None:
        if not os.path.exists(G_Temp_path):
            os.mkdir(G_Temp_path)
        self.proxyPool = []
        self.targetName = None
        self.targetHref = None

    def set_proxy(self, proxy):
        if isinstance(proxy, dict):
            self.proxyPool.append(proxy)
        elif isinstance(proxy, list):
            self.proxyPool.extend(proxy)
        else:
            print("Ivalid Proxy Format (dict or List)!")

    @abstractmethod
    def Search(self, keyWord):
        pass

    @abstractmethod
    def Select_Movie(self):
        pass

    @abstractmethod
    def Select_Ep(self):
        pass

    def startDownload(self, targetPath=None, tempPath=G_Temp_path):
        def download_start(mission, Downloader=M3u8Downloader):
            fileTempPath = (
                tempPath + self.targetName + "Ep" + str(mission["ep"]) + ".mp4"
            )
            fileTargetFolder = targetPath or os.getcwd() + self.targetName
            downloader = Downloader(mission["m3u8"])
            downloader.start(fileTempPath)
            shutil.move(fileTempPath, fileTargetFolder)

        download_thread = []
        while movie_queue.not_empty:
            t = Thread(target=download_start, args=(movie_queue.get(),))
            download_thread.append(t)
            t.start()

        for thread in download_thread:
            thread.join()

    def start(self):
        # self.Search(input("请输入名称"))
        self.Search("电")
        self.Select_Movie()
        self.Select_Ep()
        self.startDownload()
