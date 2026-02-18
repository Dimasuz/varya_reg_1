from datetime import datetime, timedelta
import time
import logging
from request_1 import request_all
from request_2 import request_mhatschool
from send_mail import send_from_yandex, to_addr
from send_tel import send_telegram

per = 11 # sek период повторения запросов
send_time = 1 # min как часто отправлять сообщение о работе
work_days = 30 # day сколько всего работает программа

logging.basicConfig(
level=logging.INFO,
format='%(asctime)s [%(levelname)s] %(message)s',
handlers=[
logging.FileHandler("debug.log"),
logging.StreamHandler()
]
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    with open('debug.log', 'w'):
        pass
    start = datetime.now()
    time_work = start + timedelta(minutes=send_time)
    alert = f"Start the program at {start}"
    logging.info(alert)
    send_from_yandex(to_addr, alert, alert)
    send_telegram(alert)

    while True:
        time_now = datetime.now()
        logging.info(f"Request the websites at {time_now}")
        time.sleep(1)
        request_all()
        # request_mhatschool()
        time.sleep(per)

        if (start + timedelta(days=work_days)) < time_now:
            alert = f"Stop the program at {time_now}"
            logging.info(alert)
            send_from_yandex(to_addr, alert, alert)
            send_telegram(alert)
            break

        if time_now > time_work:
            alert = f"Working! {time_now}"
            logging.info(alert)
            with open('debug.log', 'w+') as f:
                log = f.read()
                send_from_yandex(to_addr, alert, log)
                send_telegram(alert)
                f.write(alert)
            time_work += timedelta(minutes=send_time)
