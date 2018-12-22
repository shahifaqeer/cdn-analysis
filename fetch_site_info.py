import requests
import os
import subprocess
import json
import socket
from collections import defaultdict
from itertools import islice
from cymruwhois import Client


def load_sites(path_to_alexa_list='data/top-1m-new.csv', nwebsites=500):
    """return rank_to_sites dictionary"""
    sites = {}
    with open(path_to_alexa_list) as f:
        for line in islice(f, nwebsites):
            rank, site = line.strip().split(',')
            sites[rank] = site
    return sites


def get_ip(s):
    """input site and return IP address"""
    try:
        ip = socket.gethostbyname(s)
        # ISP blocked domains return IP 49.207.46.6, 49.207.46.24, 49.207.46.34 from edge routers
        if ip in ['49.207.46.6', '49.207.46.24', '49.207.46.34']:
            print("Blocked site "+s)
            return False
        else:
            return ip
    except Exception as e:
        print("Error getting IP address of site "+s)
        return False


def load_site_to_ip(sites, dfile="output/site_to_ip.json"):
    """load or create site_to_ip dictionary
    preloaded dictionary for 480 sites with valid lookups for 480 sites dfile = output/site_to_ip.json"""
    if os.path.exists(dfile):
        with open(dfile, 'r') as fin:
            site_to_ip = json.load(fin)
    else:
        site_to_ip = {}
        for rank, site in sites.items():
            ip = get_ip(site)   # use sockets to get IP addresses for sites
            if ip:
                site_to_ip[site] = ip
        with open(dfile, 'w') as fout:
            json.dump(site_to_ip, fout)
    return site_to_ip


def get_asn(ip):
    """use cymruwhois by default instead of pyasn
    input ip address as string, return ASN and AS owner"""
    if ip:
        c = Client()
        try:
            r = c.lookup(ip)
            return r.asn, r.owner
        except Exception as e:
            print("Error finding ASN for "+ip)
    return False, False


def save_site(site):
    """use requests module to get and save the site homepage"""

    # url = 'http://'+site
    url = 'https://www.' + site + '/'

    file = 'output/homepage/' + site
    # manually download page to analyze sites that return errors when using non-browser clients
    altfile = 'output/homepage/' + site + '.html'

    if not (os.path.exists(file) or os.path.exists(altfile)):
        try:
            sess = requests.Session()
            sess.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) ' \
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
            # sess.headers['User-Agent'] = 'abc'

            response = sess.get(url, headers={'Accept-Encoding': 'identity'}, timeout=10.0)

            # check if response status code is 200
            if response.ok:
                print("Successfully fetched the homepage of site "+site)
                data = response.text
                fout = open('output/homepage/' + site, 'w')
                fout.write(data)
                fout.close()

            else:
                print("Please fetch site manually. Fetching %s returned response code %r" % (site, response.status_code))

        except Exception as e:
            print("Error fetching %r: Exception %s" % (site, e))
        return False

    return True


def save_whois(site, IP):
    """perform and save whois query for IP or website"""

    file = 'output/whoisIP/' + site
    if not os.path.exists(file):
        try:
            out2 = subprocess.check_output(['whois', IP], stderr=subprocess.STDOUT,
                                               timeout=10.0).decode('UTF-8', 'ignore')
            fout = open('output/whoisIP/'+site, 'w')
            if site == IP:      # in case of downloading whois info on site directly
                fout = open('output/whoissite/'+site, 'w')
            fout.write(out2)
            fout.close()
            print ("Fetched whois for site %s IP %s" % (site, IP))
        except Exception as e:
            print("Error fetching whois for site %s IP %s" % (site, IP))
        return False

    return True


def save_pages_offline(site_to_ip):
    """save whois and homepage offline for analysis"""
    for site, IP in site_to_ip.items():
        save_site(site)
        save_whois(site, IP)
        save_whois(site, site)
        print('.', end="")
    return


def main():

    # check for output directory to save files
    if not os.path.exists('output'):
        os.makedirs('output')
    if not os.path.exists('output/homepage'):
        os.makedirs('output/homepage')
    if not os.path.exists('output/whoisIP'):
        os.makedirs('output/whoisIP')
    if not os.path.exists('output/whoissite'):
        os.makedirs('output/whoissite')

    sites = load_sites()        #top 500 alexa sites as a dictionary {rank: site}
    site_to_ip = load_site_to_ip(sites)

    save_pages_offline(site_to_ip)

    # save dataframe as json for analysis
    df_data = defaultdict(list)
    for rank, site in sites.items():
        df_data['rank'].append(rank)
        df_data['site'].append(site)
        ip = get_ip(site)
        df_data['ip'].append(ip)
        asn, asname = get_asn(ip)
        df_data['asn'].append(asn)
        df_data['asname'].append(asname)

    dfile = 'output/df_data.json'
    with open(dfile, 'w') as fout:
        json.dump(df_data, fout)
    print("Saved IP, ASN info in "+dfile)
    return


if __name__ == '__main__':

    main()
