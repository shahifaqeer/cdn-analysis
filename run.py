#!/usr/bin/python

"""
required
- cymruwhois
- urllib
- requests
- pandas
- bs4

%run fetch_site_info.py
- top-1m.csv, location, nwebsites
- get ip and asn/asname
- saves site_to_ip_500.json, ip_asn_500.json
- FINAL saves df_ip_asn.pkl

%run estimate_cdn.py
- a CDN() object class
- parse site and get urls of objects and counts
- parse whois (done), xcache (todo), cname (todo)
- saves CDN_data_object.pkl
- FINAL saves df_cdn.pkl

%run calculate_timings.py
- runs curl_timing_data.py if no curl_timing_count100_sites500.json file
- convert to pandas df and calculate sizes and timings
- FINAL saves df_timing.pkl

# Plot using ipython notebooks
%run plotter.ipynb <-- calculate_timings, estimate_cdn, fetch_site_info
- Input df_ip_asn.pkl, df_cdn.pkl, df_timings.pkl
- output: results/

"""

import os
import sys

import CONST
import fetch_site_info
import estimate_cdn
import calculate_timings


def create_folders():
    if not os.path.exists("results/"):
        os.makedirs("results/")
    if not os.path.exists("output/"):
        os.makedirs("output/")
    return


def check_for_input_vars():
    # TODO: temporary fix instead of argparse; fix exception handling and neat exits.

    if not os.path.exists(CONST.list_of_websites):
        print("Error. Check CONST.py. Wrong path to list of top alexa websites: %s" %CONST.list_of_websites)
        sys.exit(0)

    if CONST.nwebsites<1:
        print("Error. Check CONST.py. Number of websites is invalid: %s" % CONST.nwebsites)
        sys.exit(0)

    if CONST.count<1:
        print("Error. Check CONST.py. Number of loops must be at least 1: %s" % CONST.count)
        sys.exit(0)

    if CONST.nthreads < 1:
        print("Error. Check CONST.py. Number of threads must be at least 1: %s" % CONST.count)
        sys.exit(0)

    print("Assuming CONST.ips_blocked_by_ISP are:", CONST.ips_blocked_by_ISP)

    return


def main():
    """
    execute files in order since estimate_cdn and calculate_timings might use offline files downloaded
    by fetch_site_info
    # TODO: instead of CONST to set runtime variables, use sys.argv and argparse
    """
    print("Edit 'CONST.py' to set runtime variables before running this file.")

    print("Creating output/ and results/ folders to store working data and final results")
    create_folders()
    check_for_input_vars()

    print("\nRunning fetch_site_info.py with:\nlist_of_websites=%s\nnwebsites=%s" %(CONST.list_of_websites,
                                                                                    CONST.nwebsites))
    fetch_site_info.main()

    print("\nRunning estimate_cdn.py with:\nlist_of_websites=%s\nnwebsites=%s"
          "\ncount=%s\nnthreads=%s" % (CONST.list_of_websites, CONST.nwebsites, CONST.count, CONST.nthreads))
    calculate_timings.main()

    print("\nRunning estimate_cdn.py with:\nlist_of_websites=%s\nnwebsites=%s" % (CONST.list_of_websites,
                                                                                  CONST.nwebsites))
    estimate_cdn.main()

    return


if __name__=='__main__':

    main()
