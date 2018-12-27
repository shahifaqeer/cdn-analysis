from __future__ import division
import urllib.parse
from bs4 import BeautifulSoup
from collections import defaultdict, Counter
import os, re
import pickle as pkl
import pandas as pd

from utils import parse_whois
from utils.CDNdomains import cdn_domains, cdn_names


def split_before(pattern, text):
    prev = 0
    for m in re.finditer(pattern,text):
        yield text[prev:m.start()]
        prev = m.start()
    yield text[prev:]


class CDN:
    def __init__(self, rank, site):
        self.rank = rank
        self.site = site
        self.url = "https://www." + site
        self.object_netlocs = []
        self.num_links = 0
        self.object_cdn = defaultdict(int)
        self.object_unknown = defaultdict(int)

        self.cdn_by_site = self._find_cdn_by_site(self.site)
        self.cdn_by_whois = self._find_cdn_by_whois_org(self.site)
        self.cdn_by_cname = None  # TODO find if dns.cname points to a CDN url
        self.cdn_by_xcache = None  # TODO find 'x-cache: HIT or MISS in headers and match to CDN name

        self.cdn_by_parse = None
        self.cdn_score = {}
        self.most_linked_url = None

        self.cdn = None

    def estimate_cdn(self):
        """
        final_cdn priority is by:
        - xcache: if objects on page were on cdn, xcache shows hit or miss and also cdn name.
            - Can also be used to populate url list on the fly as analysis progresses
            - #TODO NOT IMPLEMENTED YET
        - site: compare site name against "list of well known cdn urls".
        - cname: returned cname is cdn url then original site is getting redirected to "list of well known cdn urls"
            -#TODO
        - parse: compare object links on page to "list of well known cdn urls"

        - whois: not too reliable, returns information on owner of IP range rather than CDN directly.
            - Works for most CDN providers, but requires maintaining list of famous CDN names
            - Fails if provider sells hosting services and CDN (eg Amazon AWS and Cloudfront are both on same ASN)
        """
        return self.cdn_by_xcache or self.cdn_by_site or self.cdn_by_cname or self.cdn_by_parse

    @staticmethod
    def _get_parsed_info(loc):
        """netloc is base url"""
        if loc is None or loc is "":  # empty src or link instead of local src or link
            return None, None
        parsed = urllib.parse.urlparse(loc)
        fname, fextension = os.path.splitext(parsed.path)
        return fextension, parsed.netloc

    @staticmethod
    def _find_cdn_by_site(site):
        """
        input site and cdn_domains dict
        search site in cdn_domains top down
        return cdn_name
        """
        for cdn_url in cdn_domains.keys():

            url = "." + site
            if cdn_url in url:
                #print("\t\t\t\t\t" + cdn_url + " in " + site)
                return cdn_domains[cdn_url]

            if site in cdn_url:
                # for short sites like t.co that are in all cdn_domains
                check_prefix, check_suffix = cdn_url.split(site,
                                                           1)  # split only once starting from left, atleast . prefix
                if (check_prefix[-1] == ".") or (check_prefix[-4:] == '.cdn'):
                    # only if site was complete, last char of prefix will be a '.' from cdn_domains
                    #print("\t\t\t\t\t"+site+" in "+cdn_url)
                    return cdn_domains[cdn_url]
                # print("\t\t\t\t\tError checking "+site+" in "+cdn_url)
        return None

    @staticmethod
    def _find_cdn_by_url(url):
        """
        input url from site and cdn_domains dict {cdn_url: cdn_name}
        for cdn_name in cdn_domains search cdn_name in url (not url in cdn_name)
        return first complete matching cdn_name

        TODO: add partial CDN name match using difflib.SequenceMatcher() and select best match above a threshold
        """
        for cdn_url in cdn_domains.keys():
            # add leading '.' to url if there is none
            if url[0] != '.':
                url = '.' + url

            if cdn_url in url:
                return cdn_domains[cdn_url]
        return False

    @staticmethod
    def _find_cdn_by_whois_org(site):
        # TODO use difflib.SequenceMatcher to select best match instead of exact string matches

        whois = parse_whois.loadwhoisIP(site)
        Org = parse_whois.searchOrg(whois)

        for org in Org:
            for cdn in cdn_names:
                if (org.lower() in cdn.lower()) or (cdn.lower() in org.lower()):
                    return cdn
            for cdn in cdn_domains.values():
                if (org.lower() in cdn.lower()) or (cdn.lower() in org.lower()):
                    return cdn
        return None

    @staticmethod
    def _get_cdn_url(url):
        if "cdn" in url:
            x = list(split_before("cdn", url))
            if x[0] == "":
                cdn_url = ''.join(x)
            else:
                cdn_url = x[0].split(".")[-1] + ''.join(x[1:])
            return cdn_url
        else:
            return url

    def get_cdn_score(self, cdn):
        if cdn is None:
            return 0
        return self.cdn_score[cdn]

    def get_total_links(self):
        return self.num_links

    def set_cdn_by_site(self):
        self.cdn_by_site = self._find_cdn_by_site(self.site)
        return

    def set_cdn_by_whois(self):
        self.cdn_by_whois = self._find_cdn_by_whois_org(self.site)
        return

    def count_netlocs(self, data):
        """find static resources on a webpage data and urls they are served from"""
        soup = BeautifulSoup(data, features="lxml")
        tags_to_search = ["script src", "img src", "source srcset", "source data-srcset",
                          "link href", ]  # "meta content", "a href", ]
        # extensions_to_count = [".js", ".css", ".jsp",
        #                       ".png", ".jpeg", ".jpg", ".gif", ".img",
        #                       ".ico",".woff",".woff2",".svg",]    # ".xml",".json", ".rss"
        for tag in tags_to_search:
            html_tag, html_src = tag.split(" ")
            html_elem = soup.findAll(html_tag)
            for elem in html_elem:
                obj_type, obj_loc = self._get_parsed_info(elem.get(html_src))
                if obj_type is not None and obj_type is not "":
                    # netlocs[obj_type].append(obj_loc)
                    # print(obj_type, obj_loc, tag, obj, sep="|")
                    self.object_netlocs.append(obj_loc.strip())
        return Counter(self.object_netlocs)

    def get_homepage_url_count(self):
        """counts url static resources in homepage
        input: site
        output: {url:count} in order where url is the base url from resources on homepage"""

        file = 'output/homepage/' + self.site
        altfile = 'output/homepage/' + self.site + '.html'

        if os.path.exists(file):
            with open(file, 'r') as f:
                data = f.read()
        elif os.path.exists(altfile):
            with open(altfile, 'r', encoding="utf8", errors='ignore') as f:
                data = f.read()
        else:
            # bad_sites.append(site)
            return False
        cnt = self.count_netlocs(data)
        del cnt[None]  # remove empty src NOT local src

        return cnt

    def object_url_to_cdn(self):
        """list of object on webpage to list of CDNs from CDNdomains.cdn_domains"""

        self.num_links = len(self.object_netlocs)

        if self.num_links > 0:
            for url in self.object_netlocs:
                #print("url", url)
                if url == "":
                    # not an external object at all
                    # self.object_unknown[url] += 1
                    # self.object_cdn[url] += 1
                    pass
                else:
                    cdn = self._find_cdn_by_url(url)
                    if cdn:
                        self.object_cdn[cdn] += 1
                    elif "cdn" in url:
                        cdn_url = self._get_cdn_url(url)
                        self.object_cdn[cdn_url] += 1
                    else:
                        self.object_cdn["unknown"] += 1
                        self.object_unknown[url] += 1
        return

    def estimate_cdn_by_parse(self):
        """
        sort object_cdn by their count and relative ratio
        if there are at least 5 total external links, and link with highest ratio has majority
        set it as cdn_by_parse name
        """
        sorted_cdn_count = sorted(self.object_cdn.items(), key=lambda value: value[1], reverse=True)
        self.cdn_score = {tup[0]:tup[1]/self.get_total_links() for tup in sorted_cdn_count}

        if len(sorted_cdn_count) == 0:
            self.cdn_by_parse = None
            return

        likely_cdn_name = sorted_cdn_count[0][0]

        if (likely_cdn_name is not None) and (likely_cdn_name != "unknown"):
            if self.get_total_links() > 4:      # at least 5 external urls
                cdn_score = self.get_cdn_score(likely_cdn_name)
                if cdn_score >= 0.5:
                    self.cdn_by_parse = likely_cdn_name

        if likely_cdn_name == "unknown":
            sorted_url_count = sorted(self.object_unknown.items(), key=lambda value: value[1], reverse=True)
            if self.get_total_links() > 4:
                url_score = sorted_url_count[0][1]/self.get_total_links()
                if url_score >= 0.5:
                    self.most_linked_url = sorted_url_count[0][0]
        return

    def process(self):
        cnt = self.get_homepage_url_count()
        self.object_url_to_cdn()
        self.estimate_cdn_by_parse()
        self.cdn = self.estimate_cdn()
        return


def main():
    from fetch_site_info import load_sites
    nwebsites = 500

    rank_to_site = load_sites("data/top-1m-new.csv", )
    cdn = {}
    data = defaultdict(list)

    for rank, site in rank_to_site.items():
        c = CDN(rank, site)
        c.process()
        cdn[rank] = c
        print(rank, site, c.cdn, c.cdn_by_site, c.cdn_by_whois, c.cdn_by_parse, c.get_total_links(),
              c.get_cdn_score(c.cdn_by_parse), c.most_linked_url, sep="|")

        # To store in pandas dataframe
        data['rank'].append(c.rank)
        data['site'].append(c.site)
        data['cdn'].append(c.cdn)
        data['cdn.site'].append(c.cdn_by_site)
        data['cdn.parse'].append(c.cdn_by_parse)
        data['cdn.most_url'].append(c.most_linked_url)
        data['cdn.whois'].append(c.cdn_by_whois)
        data['cdn.xcache'].append(c.cdn_by_xcache)
        data['cdn.cname'].append(c.cdn_by_cname)

    foutpath = "results/CDN_data_object.pkl"
    print("Save CDN class data for top %s sites to %s" %(nwebsites, foutpath))
    pkl.dump(cdn, open(foutpath, "wb"))

    df_cdn = pd.DataFrame(data)
    foutpath2 = "results/df_cdn.pkl"
    print("Save pandas dataframe with site, cdn using all available methods to %s" % (foutpath2))
    df_cdn.to_pickle(foutpath2)

    return


if __name__ == '__main__':

    main()


