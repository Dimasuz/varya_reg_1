import requests
from list_sites import list_sites
from request_site import request_url


def request_site(sites):

    for site in sites:

        print(site[0])

        req = request_url(site[1])
        if req == None:
            continue

        if req.status_code == 200:
            req_txt = req.text

            ind_1 = req_txt.find(site[2])
            if ind_1 == -1:
                alert = f"Site {site[0]}changed!"
            else:
                ind_2 = req_txt.find(site[3], ind_1)
                if ind_2 == -1:
                    alert = f"Problem with site {site[0]}"
                else:
                    print(ind_1, ind_2)
                text_find = req_txt[ind_1:ind_2]
                # print(text_find)
                with open(f"{site[0]}_fix.txt", "w", encoding="utf-8") as f:
                    f.write(text_find)
                alert = f"Request for site {site[0]} is OK."
        else:
            alert = f"Request for site {site[0]} is wrong."

        print(alert)

    return None


if __name__ == "__main__":
    request_site(list_sites)