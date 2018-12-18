import os
import json
from collections import defaultdict

from CDNdomains import cdn_domains, cdn_names
from count_objects import fetch_homepage_url_count
import parse_whois


def find_cdn_by_site(site):
    """
    input site and cdn_domains dict
    search site in cdn_domains top down
    return cdn_name
    """
    for cdn_url in cdn_domains.keys():
        if site in cdn_url:
            # for short sites like t.co that are in all cdn_domains
            check_prefix, check_suffix = cdn_url.split(site, 1)  # split only once starting from left, atleast . prefix
            if (check_prefix[-1] == ".") or (check_prefix[-4:] == '.cdn'):
                # only if site was complete, last char of prefix will be a '.' from cdn_domains
                # print("\t\t\t\t\t"+site+" in "+cdn_url)
                return cdn_domains[cdn_url]
            # print("\t\t\t\t\tError checking "+site+" in "+cdn_url)
    return False


def find_cdn_by_url(url):
    """
    input url from site and cdn_domains dict {cdn_url: cdn_name}
    for cdn_name in cdn_domains search cdn_name in url (not url in cdn_name)
    return cdn_name
    """
    for cdn_url in cdn_domains.keys():
        # add leading '.' to url if there is none
        if url[0] != '.':
            url = '.' + url

        if cdn_url in url:
            return cdn_domains[cdn_url]
    return False


def find_cdn_by_counting_url(site):
    """finds probable cdn based on most count of url static resources"""
    cnt = fetch_homepage_url_count(site)
    cdn_cnt = defaultdict(int)

    """save data"""
    temp_data = {}
    temp_data['site'] = site
    temp_data['cdn_cnt'] = cnt
    """end save"""

    if cnt:
        # print(site+":", end="")
        # print(cnt[:4])

        for url, url_cnt in cnt:

            if url == '':
                cdn_name = ''
            else:
                cdn_name = find_cdn_by_url(url)

                if not (cdn_name):
                    # if '.cdn' in url:
                    #    #split at first occurance of 'cdn' and print everything after
                    #    cdn_name = ''.join(url.partition('.cdn')[1:])  # unknown CDN to be resolved later
                    # elif 'cdn.' in url:
                    #    #split at last '.' before cdn (regex is better for this)
                    #    url_r = url[::-1]
                    #    cdn_name = ''.join(url.partition('.ndc')[1:])
                    if 'cdn' in url:
                        parts = url.split('.')
                        for i in range(len(parts)):
                            if 'cdn' in parts[i]:
                                break
                        cdn_name = '.'.join(parts[i:])
                    elif site in url:
                        cdn_name = ''  # local site resources and links
                    else:
                        cdn_name = '?'  # unknown external links

            cdn_cnt[cdn_name] += url_cnt

        # print(cdn_cnt)
        # sort by value into list [('cdn1': n1), ('cdn2': n2), ('?': n3), ...]
        cdn_cnt_sorted = sorted(cdn_cnt.items(), key=lambda x: x[1], reverse=True)

        """save data"""
        temp_data['url_cnt'] = cdn_cnt_sorted
        """end save"""

        # remove "?" as option
        cdn_cnt_filtered = [i for i in cdn_cnt_sorted if i[0] != '?']

        if len(cdn_cnt_filtered) > 0:
            # for c,n in cdn_cnt_filtered:
            #    if (site in c):
            #        return c

            sum_cdn_links = sum([i[1] for i in cdn_cnt_filtered])

            i = 0
            probable_cdn = cdn_cnt_filtered[i][0]
            # enter loop only if first choice is '' else return first choice
            while (probable_cdn == ''):
                i += 1
                if i < len(cdn_cnt_filtered):
                    probable_cdn = cdn_cnt_filtered[i][0]

                    if (cdn_cnt_filtered[i][1] <= 2):
                        # if num url is too low
                        i = 0
                        probable_cdn = cdn_cnt_filtered[i][0]
                        break

                    if probable_cdn in ['Google', 'Facebook', 'Twitter', 'Amazon CloudFront']:
                        # if num famous url is high but can't compare with other links
                        if (cdn_cnt_filtered[i][1] >= sum_cdn_links / 5):
                            # 1/10 was arbitarily decided but surprisingly was the threshold for deciding whatsapp, stackoverflow
                            break
                        else:
                            # if links to Google etc much less than sum then set back to first element regardless of ''
                            i = 0
                            probable_cdn = cdn_cnt_filtered[i][0]
                            break
                            # problem only if unknown cdn follows Google (ex: 9gag, whatsapp)

                else:
                    # if i>len set back to first element regardless of '' or [Google, fb, twitter] or whatever
                    i = 0
                    probable_cdn = cdn_cnt_filtered[i][0]
                    break

            print('\t' + site + ': ' + probable_cdn + ' | ' + str(sum_cdn_links) + ': ', end="")
            print(cdn_cnt_filtered)

            """save data"""
            temp_data['sum_cdn_links'] = sum_cdn_links
            temp_data['probable_cdn'] = probable_cdn

            # _save_cdn_counter_detection(temp_data)
            """end save"""

            return probable_cdn

    return False


def find_cdn_by_whois_org(site):
    all_cdn_names = list(set(cdn_names + list(cdn_domains.values())))

    whois1 = parse_whois.loadwhoisIP(site)
    Org1 = parse_whois.searchOrg(whois1)
    # Email = parse_whois.searchEmail(whois1)

    """save data"""
    temp_data = {}
    temp_data['site'] = site
    temp_data['organization'] = Org1
    """end save"""

    print("\twhois " + site + " | ", end="")
    print(Org1, end=" | ")
    # print("\t" + Org2)

    for org in Org1:  # list( set(Org1+Org2) ):
        for cdn in all_cdn_names:
            if (org.lower() in cdn.lower()) or (cdn.lower() in org.lower()):
                print(" cdn " + cdn)

                """save data"""
                temp_data['probable_cdn'] = cdn
                # _save_cdn_whois_detection(temp_data)
                """end save"""
                return cdn
    print()
    return False


def find_cdn_by_whois_site(site):
    all_cdn_names = list(set(cdn_names + list(cdn_domains.values())))

    whois2 = parse_whois.loadwhoissite(site)
    Org2 = parse_whois.searchOrg(whois2)

    print("\twhois " + site + " | ", end="")
    print(Org2, end=" | ")

    for org in Org2:  # list( set(Org1+Org2) ):
        for cdn in all_cdn_names:
            if (org.lower() in cdn.lower()) or (cdn.lower() in org.lower()):
                print(" cdn " + cdn)
                return cdn
    print()
    return False


def _save_cdn_counter_detection(temp):
    if not os.path.exists('output/cdn_counter'):
        os.makedirs('output/cdn_counter')

    site = temp['site']
    with open('output/cdn_counter/' + site + '.json', 'w') as fout:
        json.dump(temp, fout)
    # read using temp = json.load(open(site.json))
    return


def _save_cdn_whois_detection(temp):
    if not os.path.exists('output/cdn_whois'):
        os.makedirs('output/cdn_whois')

    site = temp['site']
    with open('output/cdn_whois/' + site + '.json', 'w') as fout:
        json.dump(temp, fout)
    # read using temp = json.load(open(site.json))
    return


def main():
    """Test function"""

    def find_cdn2(site):
        """wrapper func and logic to decide which cdn should be final"""
        # site in cdn or cdn in site urls
        matching_cdn = find_cdn_by_site(site) or find_cdn_by_url(site)

        if not matching_cdn:
            # by counting objects
            cdn_parsed = find_cdn_by_counting_url(site)
            # by matching whois organization
            cdn_whois = find_cdn_by_whois_org(site)

            if cdn_whois in ['Fastly', 'Cloudflare', 'Akamai', 'Alibaba', 'Google LLC']:
                # google cloud customers have 'Google LLC' in whois
                matching_cdn = cdn_whois
            else:
                matching_cdn = cdn_parsed or cdn_whois  # prioritize parsed based matching except when above case

            if not matching_cdn:
                return False
                # maybe do not need whois by site
                # matching_cdn = find_cdn_by_whois_site(site)

                # if not matching_cdn:
                #    return False
        return matching_cdn

    site_to_IP = json.load(open('output/site_to_IP.json', 'r'))
    for site_name, IP in site_to_IP.items():
        probable_cdn = find_cdn2(site_name)
        print(site_name, IP, probable_cdn)

    return


if __name__ == '__main__':

    main()
