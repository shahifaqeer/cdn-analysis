import pandas as pd
from find_cdn_methods import *

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


if __name__ == '__main__':

    main()


