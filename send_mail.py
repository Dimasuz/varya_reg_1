import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# to_addr = ["5845889@mail.ru", "dluzanov@mail.com"]
to_addr = ["5845889@mail.ru", "varyaluz@gmail.com"]

def send_from_yandex(to_addr, subj, text):

    from_addr = "daluzanov@yandex.ru"
    mypass = "ntfebdhkttstxacz"

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
        server.sendmail(from_addr, addr, text_1)
    server.quit()

# if __name__ == "__main__":
#     alert = "test"
#     send_from_yandex(to_addr, alert, alert)
#     alert = "test1"
#     send_from_yandex(to_addr[0:1], alert, alert)