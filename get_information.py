from requests import post
from json import dumps

data = {
    "bounds": {
        "bottomLeft": {
            "lat": 55.77389717291446,
            "lng": 49.0812446373849
        },
        "topRight": {
            "lat": 55.79754742662554,
            "lng": 49.185271431818514
        }
    },
    "filters": {
        "banks": [
            "tcs"
        ],
        "currencies": [
            "USD"
        ],
        "showUnavailable": True
    },
    "zoom": 14
}

URL = "https://api.tinkoff.ru/geo/withdraw/clusters"

HEADERS = {
    "Host": "api.tinkoff.ru",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept": "/",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json",
    "Content-Length": "221",
    "Origin": "https://www.tinkoff.ru/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Referer": "https://www.tinkoff.ru/",
    "Connection": "keep-alive"
}


def get_banks():
    response = post(URL, data=dumps(data), headers=HEADERS).json()
    banks = response.get("payload", {}).get("clusters", [])
    answer = []
    for bank in banks:
        answer.append(bank.get("points", [{}])[0].get("address", "No address"))
    return "  ○  ".join(answer)
