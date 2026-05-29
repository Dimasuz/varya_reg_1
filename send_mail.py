import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

mypass = os.environ.get("EMAIL_PASS", "")

to_addr = [
    "5845889@mail.ru",
    "5845889@mail.ru",
]
# to_addr = ["5845889@mail.ru", "varyaluz@gmail.com"]


def send_from_yandex(to_addr, subj, text, file_path=''):

    if not mypass:
        return "EMAIL is turn off."

    from_addr = "daluzanov@yandex.ru"

    msg = MIMEMultipart()
    msg["From"] = from_addr
    # msg['To'] = to_addr
    msg["Subject"] = subj

    if file_path:
        try:
            with open(file_path, "rb") as f:
                attachment = MIMEApplication(f.read(), Name=file_path)
                attachment['Content-Disposition'] = f'attachment; filename="{file_path}"'
                msg.attach(attachment)
        except FileNotFoundError:
            print("Error! File not found.")

    body = text
    msg.attach(MIMEText(body, "plain"))
    text_1 = msg.as_string()
    alert = "Email "
    try:
        server = smtplib.SMTP_SSL("smtp.yandex.ru", 465)
        server.login(from_addr, mypass)
    except Exception as e:
        alert = f"error - {e}"
        return alert
    for addr in to_addr:
        try:
            # server.sendmail(from_addr, addr, text_1)
            server.send_message(msg, from_addr=from_addr, to_addrs=addr)
        except Exception as e:
            alert += f"error to {addr} - {e}/ "
        else:
            alert += f"sent to {addr}/ "
    server.quit()

    return alert


# if __name__ == "__main__":
#     alert = "test"
#     send_from_yandex(to_addr, alert, alert)
#     alert = "test1"
#     send_from_yandex(to_addr[0:1], alert, alert)

# from email.message import EmailMessage
#
# msg = EmailMessage()
# msg['Subject'] = "Новый способ отправки"
# msg['From'] = "Отправитель"
# msg['To'] = "Получатель"
#
# file_path = "document.pdf"
# with open(file_path, 'rb') as f:
#     file_data = f.read()
#     msg.add_attachment(file_data, maintype='application', subtype='pdf', filename="Отчёт_2025.pdf")