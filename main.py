import logging
import os
import time
from datetime import datetime, timedelta

from dotenv import find_dotenv, load_dotenv

from list_sites import list_sites
from request_1 import request_all

# from request_2 import request_mhatschool
from send_mail import send_from_yandex, to_addr
from send_tel import send_telegram

period_sec = 30  # sec период повторения запросов
send_time_min = 30  # min как часто отправлять сообщение о работе
work_time_days = 2  # day сколько всего работает программа

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


def request_sites(per=period_sec, send_time=send_time_min, work_time=work_time_days):
    with open("de]bug.log", "w"):
        pass
    start = datetime.now()
    time_work = start + timedelta(minutes=send_time)
    alert = f"Start the program at {start}"
    logging.info(alert)
    send_from_yandex(to_addr, alert, alert)
    send_telegram(alert, chat_id_g)

    check_ready = True

    while True:
        time_now = datetime.now()
        logging.info(f"Request the websites at {time_now}")
        time.sleep(1)
        request_all()
        # request_mhatschool()
        time.sleep(per)

        if (start + timedelta(days=work_time)) < time_now:
            alert = f"Stop the program at {time_now}"
            logging.info(alert)
            send_from_yandex(to_addr, alert, alert)
            send_telegram(alert, chat_id_g)
            break

        if (start + timedelta(hours=3)) < time_now and check_ready:
            check_ready = False
            alert = f"Check the websites by yourself \n{list_sites[0][1]}\n{list_sites[2][1]}\n{list_sites[3][1]}\n{list_sites[4][1]}"
            logging.info(alert)
            send_telegram(alert, chat_id_v)
            send_telegram(alert, chat_id_d)

        if time_now > time_work:
            alert = f"Working! {time_now}"
            logging.info(alert)
            with open("debug.log") as f:
                log = f.read()
                send_from_yandex(to_addr, alert, log)
                send_telegram(alert, chat_id_g)
            time_work += timedelta(minutes=send_time)
            with open("debug.log", "w") as f:
                f.write(f"{alert}\n")


if __name__ == "__main__":
    request_sites()
