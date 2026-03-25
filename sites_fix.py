import requests

from list_sites import list_sites
from request_site import request_url


def request_site(site, file_name='fix'):

    req = request_url(site[1])

    if req[0] == None:
       alert = f"500 {site[0]} - Request was wrong! {req[1]}"
       text_find = alert
       for_return = None

    elif req[0].status_code == 200:
        req_txt = req[0].text
        ind_1 = req_txt.find(site[2])

        if ind_1 == -1:
            alert = f"{req[0].status_code} {site[0]} - Not find the begin of text!"
            text_find = alert
            for_return = False
        else:
            ind_2 = req_txt.find(site[3], ind_1)

            if ind_2 == -1:
                alert = f"{req[0].status_code} {site[0]} - Not find the end of text!"
                text_find = alert
                for_return = False
            else:
                alert = f"{req[0].status_code} {site[0]} - Request is OK."
                text_find = req_txt[ind_1:ind_2]
                for_return = True

    else:
        text_find = f"{req[0].status_code} {site[0]} - Request was wrong. {req[1]}"
        for_return = False

    with open(f"{file_name}_{site[0]}.txt", "w", encoding="utf-8") as f:
        f.write(text_find)

    return for_return, text_find


def request_sites(sites):
    for site in sites:
        request_site(site)
    return None


if __name__ == "__main__":
    request_sites(list_sites)
