import pandas as pd
from find_cdn_methods import *

from CDNdomains import cdn_domains
import urllib.parse
from bs4 import BeautifulSoup
from collections import defaultdict, Counter

site_cdn_method_map = defaultdict(list)


class CDN:
    def __init__(self, rank, site):
        self.rank = rank
        self.site = site
        self.cdn = None

        self.url = "https://www."+site
        self.object_netlocs = []
        self.num_links = 0
        self.object_cdn = defaultdict(int)
        self.object_unknown = defaultdict(int)


    @staticmethod
    def _get_parsed_info(loc):
        """netloc is base url"""
        if loc is None or loc is "":  # empty src or link instead of local src or link
            return None, None
        parsed = urllib.parse.urlparse(loc)
        fname, fextension = os.path.splitext(parsed.path)
        return fextension, parsed.netloc

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
                        self.object_cdn[url] += 1
                    else:
                        self.object_cdn["unknown"] += 1
                        self.object_unknown[url] += 1
        return

    def estimate_cdn(self):
        sorted_cdn_count = sorted(self.object_cdn.items(), key=lambda value: value[1], reverse=True)
        print(self.site, self.num_links, sorted_cdn_count)
        if len(sorted_cdn_count) == 0:
            return None
        return sorted_cdn_count[0]

    def process(self):
        cnt = self.get_homepage_url_count()
        #print(cnt)
        self.object_url_to_cdn()
        self.cdn = self.estimate_cdn()

        return


def cdn_parse_site(site):
    """wrapper func parsing site name and urls on home page"""
    # site in cdn or cdn in site urls
    matching_cdn = find_cdn_by_site(site) or find_cdn_by_url(site) or find_cdn_by_counting_url(site)

    if not matching_cdn:  # False or "" are both returned as False
        return False

    return matching_cdn


def cdn_parse_whois(site):
    """wrapper func calling whois"""
    # whois org is cdn
    matching_cdn = find_cdn_by_whois_org(site)

    if not matching_cdn:  # False or "" are both returned as False
        # matching_cdn = find_cdn_by_whois_site(site)
        return False

    return matching_cdn


def estimate_cdn(site, cdn_parsed, cdn_whois, prioritize_whois=False):
    """logic to decide which CDN finally - prioritizes parsed based detection instead of whois records
    if prioritize_whois is set to True, then if cdn_whois is a famous well known CDN, it is returned"""

    if prioritize_whois and cdn_whois in major_cdns:
        # in case ip has this whois, regardless of static resources return this info
        # usually set to false since we want to prioritize static resources based CDN over whois data
        matching_cdn = cdn_whois

    elif cdn_parsed and cdn_whois:  # confusion case when both exist
        if cdn_parsed in all_cdn_names:
            # known CDN not an unknown url
            matching_cdn = cdn_parsed
        else:
            matching_cdn = cdn_whois
            # note association between cdn_parsed of url type and cdn_whois
            global site_cdn_method_map
            site_cdn_method_map['site'].append(site)
            site_cdn_method_map['cdn_parsed'].append(cdn_parsed)
            site_cdn_method_map['cdn_whois'].append(cdn_whois)

    else:
        # assume cdn_whois has higher priority if cdn_parsed is an unknown cdn url - most will be amazon aws
        matching_cdn = cdn_whois or cdn_parsed

    """
    global i
    if cdn_parsed and cdn_whois:
        if cdn_parsed != cdn_whois:
            i += 1
            print(i, ". ", site, ":", matching_cdn, "<", cdn_parsed, "|", cdn_whois, ">")
    """

    return matching_cdn


def main():

    print("Reading file: 'output/df_data.json'\n")
    df_data = pd.read_json('output/df_data.json')
    df_valid = df_data[df_data['ip']!=False].copy()

    print("Number of sites loaded: %s" % (len(df_data)))
    print("Number of valid sites for further analysis: %s\n" % (len(df_valid)))
    print("List of blocked sites: %s" % list(df_data[df_data['ip']==False]['site']))

    df_valid['cdn_parsed'] = df_valid['site'].apply(cdn_parse_site)
    df_valid['cdn_whois'] = df_valid['site'].apply(cdn_parse_whois)
    df_valid['cdn'] = False

    df_valid['cdn'] = df_valid.apply(lambda row:
                                     estimate_cdn(row['site'], row['cdn_parsed'], row['cdn_whois'], False),
                                     axis=1)

    df_url_cdn_whois_map = pd.DataFrame(site_cdn_method_map)
    df_url_cdn_whois_map.to_pickle('output/df_url_cdn_whois_map.pkl')

    df_valid.to_pickle('output/df_ip_asn_cdn.pkl')

    print("\n\nCreating pandas dataframe file: 'output/df_url_cdn_whois_map.pkl")
    print("Creating pandas dataframe file: 'output/df_ip_asn_cdn.pkl")

    return


def main2():
    from fetch_site_info import load_sites
    rank_to_site = load_sites("data/top-1m-new.csv", 10)
    cdn = {}

    for rank, site in rank_to_site.items():
        #print(rank, site)
        c = CDN(rank, site)
        c.process()
        cdn[rank] = c
        print(c.object_unknown)

    return


if __name__ == '__main__':

    main2()


