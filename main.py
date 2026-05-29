import logging
import os
import time
from datetime import datetime, timedelta

from dotenv import find_dotenv, load_dotenv

from list_sites import list_sites
from request_3 import request_all
from send_mail import send_from_yandex, to_addr
from send_tel import send_telegram
from send_vk import MessageVk
from sites_fix import request_site

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
)  # час когда прислать напоминание о проверке и логи
tg_id_g = os.environ.get("TG_ID_G", "")
tg_id_v = os.environ.get("TG_ID_V", "")
tg_id_d = os.environ.get("TG_ID_D", "")
vk_token = os.environ.get("VK_BOT_TOKEN", "")
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
    alert = (
        f"Start the program on server {server_name} at {start.isoformat(sep=' ')[:16]}"
    )
    logging.info(alert)
    vk_message = MessageVk(vk_token)
    send_mail = send_from_yandex([to_addr[0]], alert, f"{alert}\nOld logs:\n{log}")
    logging.info(send_mail)
    send_vk = vk_message.send_message(vk_id_d, alert)
    logging.info(send_vk)
    send_tg = send_telegram(tg_id_d, alert)
    logging.info(send_tg)

    for site in list_sites:

        file_name = f"fix_{site[0]}.txt"
        if not os.path.exists(file_name):
            logging.info(f"{site[0]} does not exist.")
            request_site(site)
            logging.info(f"{site[0]} - file was renewed.")
        else:
            logging.info(f"{site[0]} - file exist.")

    changed_time = 1

    while True:
        time_now = datetime.now()
        logging.info(
            f"Request the websites on server {server_name} at {time_now.time().isoformat()[:5]}"
        )
        time.sleep(1)

        resp = request_all()
        add_alert = []

        for i in range(len(resp)):

            if "has changed" in resp[i][2]:
                alert = f"{resp[i][2]}\n{changed_time=}."
                subj_alert = f"{resp[i][0]} Site has changed (server {server_name}, {changed_time=})!"
                if changed_time == 3:
                    alert += f"\n{resp[i][3]}"
                    send_from_yandex(to_addr, subj_alert, alert, f"diff_{resp[i][0]}.html")
                vk_message.send_message(vk_id_v, alert)
                vk_message.send_message(vk_id_d, alert)
                send_from_yandex([to_addr[0]], subj_alert, alert)
                send_telegram(alert, tg_id_v)
                send_telegram(alert, tg_id_d)
                send_telegram(alert, tg_id_g)
                logging.info(alert)

                if changed_time > 2:
                    request_site(list_sites[i])
                    alert = f"{resp[i][0]} Site has renewed (server {server_name})."
                    logging.info(alert)
                    send_telegram(tg_id_d, alert)
                    vk_message.send_message(vk_id_d, alert)
                    changed_time = 1
                else:
                    changed_time += 1
            elif "Error request" in resp[i][2]:
                add_alert.append(resp[i][2])

        if (start + timedelta(days=work_time)) < time_now:
            alert = f"Stop the program on server {server_name} at {time_now.isoformat(sep=' ')[:16]}"
            logging.info(alert)
            send_mail = send_from_yandex([to_addr[0]], alert, alert)
            logging.info(send_mail)
            send_telegram(tg_id_g, alert)
            vk_message.send_message(vk_id_d, alert)
            break

        if time_now.day > check_day and time_now.hour >= check_time:
            check_day = time_now.day
            list_s = "\n".join([site[1] for site in list_sites])
            alert = f"Check the websites by yourself (server {server_name}):\n{list_s}"
            logging.info(alert)
            send_telegram(tg_id_v, alert)
            send_telegram(tg_id_d, alert)
            vk_message.send_message(vk_id_v, alert)
            vk_message.send_message(vk_id_d, alert)
            # send logs for last day on email-address
            log = "Logs was not read!"
            alert = f"Logs for {time_now.isoformat()[:10]}"
            with open("debug.log") as f:
                log = f.read()
            send_mail = send_from_yandex([to_addr[0]], alert, log)
            logging.info(send_mail)
            with open("debug_old.log", "a") as f:
                f.write(f"\n{time_now.isoformat()[:10]}\n{log}")
            with open("debug.log", "w") as f:
                f.write(f"{alert}\n")

        if time_now > time_work:
            alert = f"Working on server {server_name} at {time_now.time().isoformat()[:5]}              "
            logging.info(alert)
            if add_alert:
                alert += "\n".join(add_alert)
            send_telegram(tg_id_g, alert)
            vk_message.send_message(vk_id_d, alert)
            time_work += timedelta(minutes=send_time)
            send_mail = send_from_yandex([to_addr[0]], alert[:40], alert)
            logging.info(send_mail)

        time.sleep(per)  # waiting for next request


if __name__ == "__main__":
    check_sites(per=period_sec, send_time=send_time_min, work_time=work_time_days)
