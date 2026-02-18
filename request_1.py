import logging

from request_site import request_url
from list_sites import list_sites
from send_mail import send_from_yandex, to_addr
from send_tel import send_telegram


logging.basicConfig(
level=logging.INFO,
format='%(asctime)s [%(levelname)s] %(message)s',
handlers=[
logging.FileHandler("debug.log"),
logging.StreamHandler()
]
)

logger = logging.getLogger(__name__)

def request_list(sites):

    for site in sites:
        print(site[0])
        req = request_url(site[1])
        if req == None:
            continue

        if req.status_code == 200:
            req_txt = req.text
            ind_1 = req_txt.find(site[2])

            if ind_1 == -1:
                alert = f"Site {site[0]} has changed! \n {site[1]}"
                logging.info(alert)
                send_from_yandex(to_addr, alert, alert)
                send_telegram(alert)
            else:
                ind_2 = req_txt.find(site[3], ind_1)
                text_find = req_txt[ind_1:ind_2]
                with open(f"{site[0]}_check.txt", "w", encoding="utf-8") as f:
                    f.write(text_find)
                    # f.flush()
                with open(f"{site[0]}_check.txt", encoding="utf-8") as f_check, open(f"{site[0]}_fix.txt", encoding="utf-8") as f:
                    text_find = f_check.read()
                    site_txt = f.read()
                # print(text_find)
                # print(site_txt)
                if text_find == site_txt:
                    alert = f"Site {site[0]} is no changed."
                else:
                    alert = f"Site {site[0]} has changed! \n {site[1]}"
                    logging.info(alert)
                    send_from_yandex(to_addr, alert, alert)
                    send_telegram(alert)
        else:
            alert = f"False request the site - {site[0]}"
            logging.info(alert)
            send_from_yandex(to_addr[0:1], alert, alert)
            send_telegram(alert)

        print(alert)

    return None


def request_all():
    request_list(list_sites)
