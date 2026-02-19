import logging

from request_site import request_url
from send_mail import send_from_yandex, to_addr

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


def request_mhatschool():
    url_1 = "https://mhatschool.ru/abiturient/97"
    url_2 = "https://mhatschool.ru/abiturient/133"
    print("mhatschool")
    req = request_url(url_1)
    if not req:
        print("Site mhatschool false1.")
        return None

    if req.status_code == 200:
        if url_2 in req.text:
            req = request_url(url_2)
            if req == None:
                return None
            if req.status_code == 404:
                alert = "Site mhatschool has no changed."
            else:
                alert = "Site mhatschool has changed!"
                logging.info(alert)
                send_from_yandex(to_addr, alert, alert)
        else:
            alert = "Site mhatschool has changed!"
            logging.info(alert)
            send_from_yandex(to_addr, alert, alert)
    else:
        alert = f"False request the site - mhatschool"
        logging.info(alert)
        send_from_yandex(to_addr[0:1], alert, alert)

    print(alert)

    return None


if __name__ == "__main__":
    request_mhatschool()
