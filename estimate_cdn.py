import pandas as pd
from find_cdn_methods import *
from CDNdomains import cdn_domains, cdn_names


all_cdn_names = list(set(cdn_names + list(cdn_domains.values())))
site_cdn_method_map = defaultdict(list)


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


def estimate_cdn(site, cdn_parsed, cdn_whois):
    """logic to decide which CDN finally - prioritizes parsed based detection instead of whois records"""

    # if cdn_whois in ['Fastly', 'Cloudflare', 'CloudFront', 'Akamai', 'Alibaba', 'Google', 'Amazon']:
    #    matching_cdn = cdn_whois
    # if asname in all_valid_cdn_names:
    #    return asname

    global all_cdn_names

    if cdn_parsed and cdn_whois:  # confusion case when both exist
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

    df_data = pd.read_pickle('output/df_data.json')

    df_valid = df_sites[df_sites['IP'] != False].copy()
    df_valid['cdn_parsed'] = df_valid['site'].apply(cdn_parse_site)
    df_valid['cdn_whois'] = df_valid['site'].apply(cdn_parse_whois)
    df_valid['cdn'] = False
