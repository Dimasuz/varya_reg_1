import logging
import os
import difflib

from dotenv import find_dotenv, load_dotenv

from list_sites import list_sites
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

server_name = os.environ.get("SERVER_NAME", "?")
hd = difflib.HtmlDiff()

def request_list(sites):
    resp = []

    for site in sites:
        req = request_site(site, "check")

        if req[0]:

            with open(f"check_{site[0]}.txt", encoding="utf-8") as f_check, open(
                f"fix_{site[0]}.txt", encoding="utf-8"
            ) as f_fix:
                check_txt = f_check.read()
                fix_txt = f_fix.read()
            if check_txt == fix_txt:
                alert = f"{site[0]} Site is no changed (server {server_name})."
                resp.append([site[0], site[1], alert])
                print(alert)
            else:
                alert = f"{site[0]} Site has changed (server {server_name})!\n{site[1]}"
                logging.info(alert)
                # проверка что именно поменялось
                fix_list = fix_txt.splitlines()
                check_list = check_txt.splitlines()
                # запись изменений в файл html
                html_diff = hd.make_file(fix_list, check_list)
                with open(f"diff_{site[0]}.html", "w", encoding="utf-8") as f:
                    f.write(html_diff)
                # запись изменененной строки и +-3 строк рядом
                diff = '\n'.join(difflib.unified_diff(fix_list, check_list))
                resp.append([site[0], site[1], alert, diff])
                print(alert)

        else:
            alert = (
                f"{site[0]} - Error request the site (server {server_name})!/n{req[1]}"
            )
            logging.info(alert)
            resp.append([site[0], site[1], alert])

    return resp


def request_all():
    return request_list(list_sites)
