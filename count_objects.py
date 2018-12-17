from collections import Counter
from bs4 import BeautifulSoup
import urllib
import os
# import re


def getnetloc(loc):
    """netloc is base url"""
    if loc is None or loc is "":  # empty src or link instead of local src or link
        return None
    return urllib.parse.urlparse(loc).netloc


def count_netlocs(data):
    """find static resources on a webpage and urls they are served from"""
    soup = BeautifulSoup(data, features="lxml")

    netlocs_static = []
    # netlocs_all = []

    # static
    tags = soup.findAll('script')
    for tag in tags:
        loc = tag.get('src')
        netlocs_static.append(getnetloc(loc))

    tags = soup.findAll('img')
    for tag in tags:
        loc = tag.get('src')  # srcset should be counted only once for the src
        netlocs_static.append(getnetloc(loc))

    tags = soup.findAll('source')
    for tag in tags:
        loc = tag.get('data-srcset')  # srcset should be counted only once for the src
        netlocs_static.append(getnetloc(loc))
    for tag in tags:
        loc = tag.get('srcset')  # srcset should be counted only once for the src
        netlocs_static.append(getnetloc(loc))

    tags = soup.findAll('link')
    for tag in tags:
        loc = tag.get('href')
        netlocs_static.append(getnetloc(loc))

    tags = soup.findAll('meta')
    for tag in tags:
        loc = tag.get('content')
        netlocs_static.append(getnetloc(loc))

    tags = soup.findAll('a')
    for tag in tags:
        loc = tag.get('href')
        nloc = getnetloc(loc)
        if not (nloc == ''):  # only counting links having external source
            netlocs_static.append(nloc)

    """
    # all
    tags = soup.findAll('a')
    for tag in tags:
        loc = tag.get('href')
        netlocs_all.append( getnetloc(loc) )
    """
    return Counter(netlocs_static)


def fetch_homepage_url_count(site):
    """counts url static resources in homepage
    input: site
    output: {url:count} in order where url is the base url from resources on homepage"""
    file = 'output/homepage/' + site
    altfile = 'output/homepage/' + site + '.html'

    if os.path.exists(file):
        with open(file, 'r') as f:
            data = f.read()
    elif os.path.exists(altfile):
        with open(altfile, 'r', encoding="utf8", errors='ignore') as f:
            data = f.read()
    else:
        # bad_sites.append(site)
        return False
    cnt = count_netlocs(data)
    del cnt[None]  # remove empty src NOT local src

    return cnt.most_common()
