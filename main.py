import logging
import os
import time
from datetime import datetime, timedelta

from dotenv import find_dotenv, load_dotenv

from list_sites import list_sites
from request_1 import request_all

# from request_2 import request_mhatschool
from send_mail import send_from_yandex, to_addr
from send_vk import MessageVk

# from send_tel import send_telegram
from sites_fix import request_site

# from pprint import pprint


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
period_sec = int(os.environ.get("PERIOD_REQ", "20"))  # sec период повторения запросов
send_time_min = int(
    os.environ.get("SEND_TIME", "30")
)  # min как часто отправлять сообщение о работе
work_time_days = int(os.environ.get("WORK_TIME", "30"))
check_time = int(
    os.environ.get("CHECK_TIME", "12")
)  # час когдау прислать напоминание о проверке и логи
# chat_id_g = os.environ.get("CHAT_ID_G", "")
# chat_id_v = os.environ.get("CHAT_ID_V", "")
# chat_id_d = os.environ.get("CHAT_ID_D", "")
vk_token = os.environ.get("VK_TOKEN", "")
vk_id_d = os.environ.get("VK_ID_D", "")
vk_id_v = os.environ.get("VK_ID_V", "")
server_name = os.environ.get("SERVER_NAME", "?")


def check_sites(per=period_sec, send_time=send_time_min, work_time=work_time_days):
    with open("debug_old.log", "a+") as f:
        f.seek(0)
        log = f.read()
    with open("debug.log", "w"), open("debug_old.log", "w"):
        pass

    start = datetime.now()
    check_day = start.day - 1
    time_work = start + timedelta(minutes=send_time)
    alert = f"Start the program on server {server_name} at {start}"
    logging.info(alert)
    vk_message = MessageVk(vk_token)
    send_mail = send_from_yandex(to_addr, alert, f"{alert}\nOld logs:\n{log}")
    logging.info(send_mail)
    vk_message.send_message(vk_id_d, alert)
    # send_telegram(alert, chat_id_g)

    changed_time = 1

    while True:
        time_now = datetime.now()
        logging.info(f"Request the websites on server {server_name} at {time_now}")
        time.sleep(1)
        resp = request_all()
        # pprint(resp)
        for i in range(len(resp)):
            if "has changed" in resp[i][2]:
                alert = (
                    f"{resp[i][0]} has changed (server {server_name}), {changed_time=}."
                )
                logging.info(alert)
                if changed_time > 2:
                    request_site(list_sites[i])
                    alert = f"{resp[i][0]} has renewed (server {server_name})."
                    logging.info(alert)
                    # send_telegram(alert, chat_id_d)
                    vk_message.send_message(vk_id_d, alert)
                    changed_time = 1
                else:
                    changed_time += 1
            else:
                pass
                # print(f"{resp[i][0]} has no changed.")
        # request_mhatschool()
        time.sleep(per)

        if (start + timedelta(days=work_time)) < time_now:
            alert = f"Stop the program on server {server_name} at {time_now}"
            logging.info(alert)
            send_mail = send_from_yandex(to_addr, alert, alert)
            logging.info(send_mail)
            # send_telegram(alert, chat_id_g)
            vk_message.send_message(vk_id_d, alert)
            break

        if time_now.day > check_day and time_now.hour >= check_time:
            check_day = time_now.day
            alert = f"Check the websites by yourself (server {server_name})\n{list_sites[0][1]}\n{list_sites[2][1]}\n{list_sites[3][1]}\n{list_sites[4][1]}"
            logging.info(alert)
            # send_telegram(alert, chat_id_v)
            # send_telegram(alert, chat_id_d)
            vk_message.send_message(vk_id_v, alert)
            vk_message.send_message(vk_id_d, alert)
            # send logs for last day on email-address
            log = "Logs was not read!"
            alert = f"Logs for {time_now.isoformat()[:10]}"
            with open("debug.log") as f:
                log = f.read()
            send_mail = send_from_yandex(to_addr, alert, log)
            logging.info(send_mail)
            with open("debug_old.log", "a") as f:
                f.write(f"\n{time_now}\n{log}")
            with open("debug.log", "w") as f:
                f.write(f"{alert}\n")

        if time_now > time_work:
            alert = f"Working on server {server_name}! {time_now}"
            logging.info(alert)
            # send_telegram(alert, chat_id_g)
            vk_message.send_message(vk_id_d, alert)
            time_work += timedelta(minutes=send_time)
            log = "Logs was not read!"
            # with open("debug.log") as f:
            #     log = f.read()
            send_mail = send_from_yandex(to_addr, alert, log)
            logging.info(send_mail)
            # with open("debug_old.log", "a") as f:
            #     f.write(f"\n{time_now}\n{log}")
            # with open("debug.log", "w") as f:
            #     f.write(f"{alert}\n")


if __name__ == "__main__":
    check_sites()
