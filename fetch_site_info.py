import requests
import os
import subprocess
import json
import socket
from itertools import islice


def load_sites(path_to_alexa_list = 'top-1m-new.csv', nwebsites = 500):
    """"""
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
        print("Error accessing site "+s)
        return False


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

    sites = load_sites()    #top 500 alexa sites as a dictionary {rank: site}

    # load site_to_ip dictionary
    dfile = "output/site_to_IP_.json"    # preloaded dictionary for 480 sites with valid lookups
    if os.path.exists(dfile):
        with open(dfile, 'r') as fin:
            site_to_ip = json.load(fin)
    else:
        site_to_ip = {}
        for rank, site in sites.items():
            ip = get_ip(site)   # use sockets to get IP addresses for sites
            if ip:
                site_to_ip[site] = ip

    for site, IP in site_to_ip.items():
        save_site(site)
        save_whois(site, IP)
        save_whois(site, site)


if __name__ == '__main__':

    main()
