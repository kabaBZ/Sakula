from abc import abstractmethod
from DownLoader import M3u8Downloader, DirectDownloader
from queue import Queue
from multiprocessing import Process
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

    def download_start(
        self, mission, targetPath=None, tempPath=G_Temp_path, Downloader=M3u8Downloader
    ):
        fileTempPath = tempPath + self.targetName + "Ep" + str(mission["ep"]) + ".mp4"
        fileTargetFolder = targetPath or os.getcwd() + "\\" + self.targetName
        if not os.path.exists(fileTargetFolder):
            os.mkdir(fileTargetFolder)
        downloader = Downloader(mission["m3u8"])
        downloader.start(fileTempPath)
        print(self.targetName + "Ep" + str(mission["ep"]) + ".mp4下载成功！")
        shutil.move(
            fileTempPath,
            fileTargetFolder
            + "\\"
            + self.targetName
            + "Ep"
            + str(mission["ep"])
            + ".mp4",
        )

    def get_list_from_input(self):
        x = input("输入<back>:重新选择电影,输入数字确定下载ep(支持范围选择), 输入0下载全部ep")
        while x == "back":
            self.Select_Movie()
            x = input("list:")
        x = x.strip(",").strip("，").replace("，", ",")
        x = x.split(",")
        s = set()
        for char in x:
            if "-" in char:
                for i in range(int(char.split("-")[0]) - 1, int(char.split("-")[1])):
                    s.add(i)
            else:
                s.add(int(char) - 1)
        return s

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
        download_pool = []
        # while not movie_queue.empty():
        p = Process(target=self.download_start, args=(movie_queue.get(),))
        download_pool.append(p)
        p.start()

        # for p in download_pool:
        p.join()

    def start(self):
        # self.Search(input("请输入名称"))
        self.Search("电")
        self.Select_Movie()
        self.Select_Ep()
        self.startDownload()
