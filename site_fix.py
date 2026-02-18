import requests

from list_sites import list_sites

def request_site():
    url = "https://gitis.net/postupayushim/bachelor/proslushivania/#artist"
    st_accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    # имитируем подключение через браузер Mozilla
    st_useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
    headers = {"Accept": st_accept, "User-Agent": st_useragent}
    req = requests.get(url, headers=headers, verify=False)

    if req.status_code == 200:
        req_txt = req.text
        with open(f"{url[8:15]}_fix.txt", "w+", encoding="utf-8") as f:
            f.write(req_txt)
        alert = f"Request for site {url[8:14]} is OK."
    else:
        print(req)
        alert = f"Request for site {url[8:14]} is wrong."

    print(alert)

    return None


if __name__ == "__main__":
    request_site()