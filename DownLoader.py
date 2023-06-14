import os
import requests
from abc import abstractmethod
from tqdm import tqdm
from Myrequests import SakulaReq
from threading import Thread
import threading


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

    def download_as_data(self, links, index, desc):
        SakulaRequest = SakulaReq()
        data = b""
        for link in tqdm(links, desc):
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
        links = self.getData()

        def divideIntoNstrand(lst, n):
            length = len(lst)
            sublist_length = length // n
            remainder = length % n

            sublists = []
            start = 0

            for i in range(n):
                sublist_size = sublist_length + (1 if i < remainder else 0)
                end = start + sublist_size
                sublists.append(lst[start:end])
                start = end

            return sublists

        devide_list = divideIntoNstrand(links, 4)
        # self.download_as_data(links, 0)
        thread_pool = []
        for list1 in devide_list:
            t = Thread(
                target=self.download_as_data,
                args=(list1, devide_list.index(list1)),
                kwargs={
                    "desc": filePath.split("\\")[-1]
                    + " part"
                    + str(devide_list.index(list1))
                },
            )
            thread_pool.append(t)
            t.start()

        for t in thread_pool:
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


def download_chunk(url, start, end, filename):
    headers = {"Range": f"bytes={start}-{end}"}
    response = requests.get(url, headers=headers, stream=True)

    with open(filename, "r+b") as file:
        file.seek(start)
        file.write(response.content)


def download_file(url, num_threads):
    response = requests.head(url)
    file_size = int(response.headers["Content-Length"])

    chunk_size = file_size // num_threads
    last_chunk_size = chunk_size + (file_size % num_threads)

    threads = []
    with open("downloaded_file", "wb") as file:
        file.write(b"\0" * file_size)

        for i in range(num_threads):
            if i == num_threads - 1:
                # 最后一个线程下载剩余的数据
                start = (num_threads - 1) * chunk_size
                end = start + last_chunk_size - 1
                thread = threading.Thread(
                    target=download_chunk, args=(url, start, end, "downloaded_file")
                )
                thread.start()
                threads.append(thread)
            else:
                start = i * chunk_size
                end = start + chunk_size - 1

                thread = threading.Thread(
                    target=download_chunk, args=(url, start, end, "downloaded_file")
                )
                thread.start()
                threads.append(thread)

        # 等待所有线程完成
        for thread in threads:
            thread.join()

    print("文件下载完成")


if __name__ == "__main__":
    url = "https://example.com/file.jpg"
    num_threads = 4

    download_file(url, num_threads)
