import logging
import requests
import urllib3

urllib3.disable_warnings()

def request_url(url):
    # st_accept = {"text/html", "application/json", "*/*"}
    st_accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    # имитируем подключение через браузер Mozilla
    st_useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    headers = {"Accept": st_accept, "User-Agent": st_useragent}
    try:
        req = requests.get(url, headers=headers, timeout=(10,30), verify=False)
    except requests.exceptions.Timeout:
        alert = f"Timed out on {url}"
        logging.info(alert)
        return None
    except Exception as ex:
        alert = f"Error: {ex}"
        logging.info(alert)
        return None

    return req