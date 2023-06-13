import os
import requests
from abc import abstractmethod
from tqdm import tqdm
from Myrequests import SakulaReq
from threading import Thread


class Downloader:
    def __init__(self) -> None:
        pass

    @abstractmethod
    def start():
        pass


class M3u8Downloader(Downloader):
    def __init__(self, fileName) -> None:
        if not os.path.exists("./m3u8"):
            os.mkdir("./m3u8")
        self.filePath = "./m3u8/" + fileName.split("/")[-1]
        self.url = (
            fileName
            if fileName.startswith("http")
            else "https://tup.yinghuacd.com/feifan/" + fileName
        )
        self.data = {}

    def readLinks(self):
        with open(self.filePath, "r") as f:
            lines = f.readlines()
        links = [line[:-1] for line in lines if line[:6] == "https:"]
        return links

    def getData(self):
        if not os.path.exists(self.filePath):
            res = requests.get(self.url)
            with open(self.filePath, "wb") as f:
                f.write(res.content)
        return self.readLinks()

    def download_as_data(self, links, index):
        SakulaRequest = SakulaReq()
        data = None
        for link in tqdm(links):
            ts = SakulaRequest.Request(
                method="GET", url=link, data=None, headers=None, verify=False
            )
            if ts["suc"]:
                data += ts["data"].content
            else:
                ts = SakulaRequest.Request(
                    method="GET", url=link, data=None, headers=None, verify=False
                )
                if ts["suc"]:
                    data += ts["data"].content
                else:
                    with open("error.html", "w") as f:
                        f.write(ts["data"])
                    print(ts)
        return self.data.update({index: data})

    def start(self, filePath):
        links = self.getData()[1:4]

        def divideIntoNstrand(listTemp, n):
            twoList = [[] for i in range(n)]
            for i, e in enumerate(listTemp):
                twoList[i % n].append(e)
            return twoList

        devide_list = divideIntoNstrand(links, 4)
        self.download_as_data(links, 0)
        thread_pool = []
        # for list1 in devide_list:
        t = Thread(
            target=self.download_as_data,
            args=(devide_list[0] + devide_list[1] + devide_list[2] + devide_list[3], 0),
        )
        thread_pool.append(t)
        t.start()

        # for t in thread_pool:
        t.join()
        if os.path.exists(filePath):
            os.remove(filePath)
        with open(filePath, "ab") as f:
            f.write(self.data[0])
            f.write(self.data[1])
            f.write(self.data[2])
            f.write(self.data[3])
        print("over:{}".format(filePath))


class DirectDownloader(Downloader):
    def __init__(self, url) -> None:
        self.link = url

    def start(self):
        ts = SakulaReq.Request(
            method="GET", url=self.link, data=None, headers=None, verify=False
        )
        if ts["suc"]:
            with open("file.ts", "ab") as f:
                f.write(ts["data"].content)
        else:
            print(ts)
