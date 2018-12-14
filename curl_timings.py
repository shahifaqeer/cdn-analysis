from __future__ import division
import subprocess
import json
from collections import defaultdict
import multiprocessing
import time
import os
#import numpy as np


def fetch_url(url):
    """fetch url using curl
    --connect-timeout 5.0s optional, max timeout -m 10.0s, follow redirects using -L flag
    result is ( dict {url_effective, response_code, time_namelookup, time_connect, time_appconnect,
    time_pretransfer, time_redirect, time_starttransfer, time_total}, exception )
    variable explanations: https://ec.haxx.se/usingcurl-verbose.html
    """
    try:
        p = subprocess.Popen(['curl', '-L', '--connect-timeout', '5.0', '-m', '10.0', '-o', '/dev/null',
                              '-w', '@curl_time_format.txt', '-s', url], stdout=subprocess.PIPE)
        out, err = p.communicate()
        result = json.loads(out.decode('UTF-8'))
        #print("%r (%r) fetched with response code %r in %ss"
        #      % (url, result['url_effective'], result['response_code'], result['time_total']))
    except Exception as e:
        print("Error fetching %r: Exception %s" % (url, e))
        result = None
    return result


def load_urls(websites, nwebsites=500):
    """get top 500 of alexa websites csv <RANK, SITE> and append with 'https://www.' for curl request"""
    urls = defaultdict(int)
    from itertools import islice
    with open(websites) as f:
        for line in islice(f, nwebsites):
            rank, site = line.strip().split(',')
            url = 'https://www.' + site + '/'
            urls[rank] = url
    return urls


def main():

    # check for output directory to save files
    outdir = 'output/'
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    list_of_websites = 'top-1m-new.csv'  # location of alexa top websites as RANK,SITE\n
    count = 100      # average timings over count loops of curl requests
    nthreads = 20   # number of parallel threads for same url default 20

    data = defaultdict(list)    # save result as json and load in pandas for averaging and analysis
    urls = load_urls(list_of_websites, 500)
    #inv_urls = {v: k for k, v in urls.items()}  # reverse dictionary to retrieve rank given url

    #url_counter = 0
    #for rank, url in urls.items():
    for i in range(count):

        #url_counter += 1
        #urls_parallel = [url for i in range(count)]
        urls_parallel = urls.values()
        #print("Rank: %s, Start time: %s, URL: %r" % (rank, time.time(), url))
        print("Loop: %s, Start time: %s" % (i, time.time()))

        pool = multiprocessing.Pool(processes=nthreads)
        pool_outputs = pool.map(fetch_url, urls_parallel)  # pool_output is a list of results

        pool.close()
        pool.join()

        for res in pool_outputs:
            if res is not None:
                [data[key].append(res[key]) for key in res.keys()]
                #data['rank'].append(inv_urls[res['url_effective']])    # can't use just in case url_effective != url

    with open('output/curl-timing-data-reorder-count100-sites500.json', 'w') as outfile:
        json.dump(data, outfile)

    return


if __name__ == '__main__':

    main()
