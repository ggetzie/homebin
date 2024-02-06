#! /usr/bin/env python
import argparse
import re
import os
import sys
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import requests


def get_subtitle_list_url(url):
    yp = requests.get(url, timeout=10)
    yp_soup = BeautifulSoup(yp.text, "html.parser")
    res = yp_soup.find_all("a", title=re.compile("Download Subtitles"))[0]["href"]
    return res


def parse_tr(tr):
    rating_td = tr.find("td", class_="rating-cell")
    if not rating_td:
        return None
    rating = int(rating_td.text.strip())
    lang_td = tr.find("td", class_="flag-cell")
    lang = lang_td.text.strip()
    title_cell = tr.find_all("td")[2]
    title_a = title_cell.find("a")
    title = title_a.text.strip().replace("\n", " ")
    title = re.sub(r"^subtitle ", "", title, flags=re.IGNORECASE)
    title_url = title_a["href"]
    return rating, lang, title, title_url


def get_subtitle_options(lp_url, lang="English"):
    lp = requests.get(lp_url, timeout=10)
    lp_soup = BeautifulSoup(lp.text, "html.parser")
    trs = lp_soup.find_all("tr")
    res = []
    for tr in trs:
        parsed = parse_tr(tr)
        if parsed and parsed[1].lower() == lang.lower():
            res.append(parsed)
    return sorted(res, key=lambda x: x[0], reverse=True)


def select_subtitle(sub_options):
    count = 0
    print("\tRating\tLanguage\tTitle")
    for rating, lang, title, _ in sub_options:
        print(f"{count}\t   {rating}\t{lang}\t\t{title}")
        count += 1
    print()
    selection = int(input("Select a subtitle by number: "))
    return sub_options[selection][3]


def get_absolute_url(sub_url, relative_url):
    parsed = urlparse(sub_url)
    return f"{parsed.scheme}://{parsed.netloc}{relative_url}"


def get_zip_url(sub_detail_url):
    sd = requests.get(sub_detail_url, timeout=10)
    sd_soup = BeautifulSoup(sd.text, "html.parser")
    links = sd_soup.find_all("a", href=re.compile(r"\.zip$"))
    if not links:
        return None

    return links[0]["href"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get YIFY subtitles")
    parser.add_argument("url", help="URL of the movie")
    args = parser.parse_args()
    sub_url = get_subtitle_list_url(args.url)
    sub_options = get_subtitle_options(sub_url)
    if not sub_options:
        print(f"No subtitles found at {sub_url}")
        sys.exit(0)
    relative_url = select_subtitle(sub_options)
    sub_detail_url = get_absolute_url(sub_url, relative_url)
    zip_url = get_absolute_url(sub_url, get_zip_url(sub_detail_url))
    zip_filename = zip_url.split("/")[-1]
    r = requests.get(zip_url, timeout=10)
    with open(zip_filename, "wb") as f:
        f.write(r.content)
    os.system(f"unzip {zip_filename}")
    os.remove(zip_filename)
