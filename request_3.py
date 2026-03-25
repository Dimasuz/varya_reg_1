import logging
import os

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


def request_list(sites):
    resp = []

    for site in sites:
        req = request_site(site, "check")

        if req[0]:

            with open(f"check_{site[0]}.txt", encoding="utf-8") as f_check, open(
                f"fix_{site[0]}.txt", encoding="utf-8"
            ) as f_fix:
                check_text = f_check.read()
                fix_txt = f_fix.read()
            if check_text == fix_txt:
                alert = f"{site[0]} Site is no changed (server {server_name})."
                resp.append([site[0], site[1], alert])
                print(alert)
            else:
                alert = f"{site[0]} Site has changed (server {server_name})!\n{site[1]}"
                logging.info(alert)
                resp.append([site[0], site[1], alert])
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
