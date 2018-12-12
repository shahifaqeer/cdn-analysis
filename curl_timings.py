from __future__ import division
import subprocess
import json
from collections import defaultdict
import time
#from multiprocessing.pool import ThreadPool
#import numpy as np


def fetch_url(url):
    """fetch url using curl
    --connect-timeout 5.0s optional, max timeout -m 10.0s, follow redirects using -L flag
    result is ( dict {url_effective, response_code, time_namelookup, time_connect, time_appconnect,
    time_pretransfer, time_redirect, time_starttransfer, time_total}, exception )
    """
    try:
        p = subprocess.Popen(['curl', '-L', '--connect-timeout', '5.0', '-m', '10.0', '-o', '/dev/null',
                              '-w', '@curl_time_format.txt', '-s', url], stdout=subprocess.PIPE)
        out, err = p.communicate()
        result = json.loads(out.decode('UTF-8'))
        return result, None
    except Exception as e:
        return None, e


def load_url_list(websites, nwebsites=500):
    """get top 500 of alexa websites csv <RANK, SITE> and append with 'https://www.' for curl request"""
    urls = []
    from itertools import islice
    with open(websites) as f:
        for line in islice(f, nwebsites):
            rank, site = line.strip().split(',')
            url = 'https://www.' + site + '/'
            urls.append(url)
    return urls


def main():

    list_of_websites = 'top-1m-new.csv'  # location of alexa top websites as RANK,SITE\n
    count = 100  # average timings over count loops of curl requests
    # nthreads = 20 # number of parallel threads for same url

    data = defaultdict(list)    # save result as json and load in pandas for averaging and analysis
    urls = load_url_list(list_of_websites, 500)
    url_counter = 0

    for url in urls:

        url_counter += 1
        # can do threading here using gevents or multiprocessing to parallelize curl requests
        for i in range(count):
            result, error = fetch_url(url)
            if error is None:

                # if result['response_code'] == '000':
                #     # try reaching website without www
                #     url = url.replace("www.", "")
                #     result, error = fetch_url(url)
                # elif result['response_code'] == '301' or result['response_code'] == '302':
                #     # try fetching effective url after redirects instead
                #     url = result['url_effective']
                #     result, error = fetch_url(url)

                [data[key].append(value) for key, value in result.items()]
                data['rank'].append(url_counter)    # rank of alexa website is same as counter
                data['url'].append(url)     # original url fetched (before redirect)

                print("%s %r (%r) fetched with response code %r in %ss on iteration %s "
                      % (url_counter, url, result['url_effective'], result['response_code'], result['time_total'], i))
            else:
                print("Error fetching %s %r (%r): Exception %s on iteration %s"
                      % (url_counter, url, result['url_effective'], error, i))
        print()

    with open('curl-timing-data-100.json', 'w') as outfile:
        json.dump(data, outfile)

    return


if __name__ == '__main__':

    main()
