class SearchResult:
    def __init__(self, nameList, hrefList) -> None:
        self.data = [
            {"index": nameList.index(name) + 1, "name": name, "href": href}
            for name, href in zip(nameList, hrefList)
        ]
