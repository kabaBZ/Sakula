import os
import requests
from abc import abstractmethod
from tqdm import tqdm
from Myrequests import SakulaReq


class Downloader:
    def __init__(self) -> None:
        pass

    @abstractmethod
    def start():
        pass


class M3u8Downloader(Downloader):
    def __init__(self, fileName) -> None:
        self.filePath = "./" + fileName.split("/")[-1]
        self.url = (
            fileName
            if fileName.startswith("http")
            else "https://tup.yinghuacd.com/feifan/" + fileName
        )

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

    def start(self, name="name"):
        SakulaRequest = SakulaReq()
        links = self.getData()

        for link in tqdm(links):
            ts = SakulaRequest.Request(
                method="GET", url=link, data=None, headers=None, verify=False
            )
            if ts["suc"]:
                with open("{}.ts".format(name), "ab") as f:
                    f.write(ts["data"].content)
            else:
                ts = SakulaRequest.Request(
                    method="GET", url=link, data=None, headers=None, verify=False
                )
                if ts["suc"]:
                    with open("{}.ts".format(name), "ab") as f:
                        f.write(ts["data"].content)
                else:
                    print(ts.text)


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
