from request_site import request_url

url = "https://vgik.info/abiturient/higher/spetsialitet/aktyerskiy-fakultet/"


def request_site(url=url):
    req = request_url(url)

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
