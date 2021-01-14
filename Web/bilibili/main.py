import json
import requests


def get_fans(uid):
    res = requests.get("http://api.bilibili.com/x/web-interface/card?mid={}".format(uid))
    res = json.loads(res.text)
    if res.get("code") == 0:
        data = res.get("data")
        print(data)
        return data
    return None


if __name__ == '__main__':
    get_fans(uid="35680373")
