import os
from dotenv import find_dotenv, load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# to_addr = ["5845889@mail.ru", "dluzanov@mail.com"]
to_addr = ["5845889@mail.ru", "varyaluz@gmail.com"]

def send_from_yandex(to_addr, subj, text):

    from_addr = "daluzanov@yandex.ru"
    mypass = os.environ.get("EMAIL_PASS", "")

    msg = MIMEMultipart()
    msg['From'] = from_addr
    # msg['To'] = to_addr
    msg['Subject'] = subj

    body = text
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.login(from_addr, mypass)
    text_1 = msg.as_string()
    for addr in to_addr:
        try:
            server.sendmail(from_addr, addr, text_1)
        except:
            print(f"Error send massage to {addr}")
    server.quit()

    return None

# if __name__ == "__main__":
#     alert = "test"
#     send_from_yandex(to_addr, alert, alert)
#     alert = "test1"
#     send_from_yandex(to_addr[0:1], alert, alert)