import requests


class SakulaReq:
    def __init__(self) -> None:
        pass

    @staticmethod
    def getDefaultHeaders(headers):
        # todo
        if headers:
            return {}.update(headers)
        return {}

    def Request(self, method: str, url: str, data, headers=None, **args):
        try:
            res = requests.request(
                method=method.upper(),
                url=url,
                data=data,
                headers=self.getDefaultHeaders(headers),
                **args
            )
            if res.status_code != 200:
                return {"suc": False, "data": res.text}
            return {"suc": True, "data": res}
        except Exception as e:
            return {"suc": False, "data": str(e)}
