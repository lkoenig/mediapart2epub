#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from xml.etree import ElementTree as etree
import certifi
import urllib3
import mechanize
from bs4 import BeautifulSoup

FEED = 'https://www.mediapart.fr/articles/feed'
PRINT_URI = 'https://www.mediapart.fr/tools/print/{data_nid}'

class ElementWrapper:
    def __init__(self, element):
        self._element = element
    def __getattr__(self, tag):
        if tag.startswith("__"):
            raise AttributeError(tag)
        return self._element.findtext(tag)    


def get_article(browser, url):
    r = browser.open(url)
    content = r.read()

    nid = get_data_nid(content)
    if nid is not None:
        # Use the print version
        article = browser.open(PRINT_URI.format(data_nid=nid))
    else:
        article = format_article(content)
    return article

def get_data_nid(content):
    soup = BeautifulSoup(content, 'html.parser')
    div = soup_article.find_all(lambda x: x.has_attr("data-nid"))
    if len(div) > 0:
        data_nid = div[0]["data-nid"]
        return data_nid
    return None

def format_article(content):
    title = soup.find_all("h1", "title")
    print title.string
    introduction = soup.find_all("div", "introduction")[0]
    author = soup.find_all("div", "author")[0]
    date = soup.find_all("div", "date")[0]

def get_article_list(feed_url):
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where())

    r = http.request('GET', feed_url)
    feed = etree.fromstring(r.data)
    return [ElementWrapper(c) for c in feed.findall("channel/item")]

def hoover():
    browser = mechanize.Browser()
    # browser.open("https://www.mediapart.com/login")

    for item in get_article_list(feed_url=FEED):
        article = get_article(browser, item.link + "?onglet=full")
        format_article(article)
        break

if __name__ == '__main__':
    # hoover()
    content = ""
    with open("out.html") as fid:
        content = fid.read()
    format_article(content)