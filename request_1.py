import logging
import os
from pprint import pprint

from dotenv import find_dotenv, load_dotenv

from list_sites import list_sites
from request_site import request_url
from send_mail import send_from_yandex, to_addr
from send_tel import send_telegram

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

chat_id_g = os.environ.get("CHAT_ID_G", "")
chat_id_v = os.environ.get("CHAT_ID_V", "")
chat_id_d = os.environ.get("CHAT_ID_D", "")


def request_list(sites):

    resp = []

    for site in sites:
        print(site[0])
        req = request_url(site[1])
        if req == None:
            alert = f"Error request the site - {site[0]}"
            logging.info(alert)
            send_from_yandex(to_addr[0:1], alert, alert)
            send_telegram(alert, chat_id_d)
            resp.append([site[0], site[1], alert])
            continue

        if req.status_code == 200:
            req_txt = req.text
            ind_1 = req_txt.find(site[2])

            if ind_1 == -1:
                alert = f"Site {site[0]} has changed! \n {site[1]}"
                logging.info(alert)
                send_telegram(alert, chat_id_v)
                send_telegram(alert, chat_id_d)
                send_from_yandex(to_addr, alert, alert)
                send_telegram(alert, chat_id_g)
                resp.append([site[0], site[1], alert])
            else:
                ind_2 = req_txt.find(site[3], ind_1)
                text_find = req_txt[ind_1:ind_2]
                with open(f"check_{site[0]}.txt", "w", encoding="utf-8") as f:
                    f.write(text_find)
                    # f.flush()
                with open(f"check_{site[0]}.txt", encoding="utf-8") as f_check, open(
                    f"fix_{site[0]}.txt", encoding="utf-8"
                ) as f:
                    text_find = f_check.read()
                    site_txt = f.read()
                # print(text_find)
                # print(site_txt)
                if text_find == site_txt:
                    alert = f"Site {site[0]} is no changed."
                    resp.append([site[0], site[1], alert])
                else:
                    alert = f"Site {site[0]} has changed! \n {site[1]}"
                    logging.info(alert)
                    send_telegram(alert, chat_id_v)
                    send_telegram(alert, chat_id_d)
                    send_from_yandex(to_addr, alert, alert)
                    send_telegram(alert, chat_id_g)
                    resp.append([site[0], site[1], alert])
        else:
            alert = f"False request the site - {site[0]}"
            logging.info(alert)
            send_from_yandex(to_addr[0:1], alert, alert)
            send_telegram(alert, chat_id_d)
            resp.append([site[0], site[1], alert])

        print(alert)

    return resp


def request_all():
    return request_list(list_sites)
