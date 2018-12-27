import os
import json
import pandas as pd

from utils.curl_timings import parallel_requests, save_curl_timings_data
import CONST


def get_dns_res_time(d):
    return d['time_namelookup'] - d['time_redirect']


def get_tcp_conn_time(d):
    return d['time_connect'] - d['time_namelookup']


def get_ssl_handshake_time(d):
    if d['time_appconnect'] == 0:
        return 0
    return d['time_appconnect'] - d['time_connect']

#def get_ssl_handshake_time(d):
#    t_ssl = d['time_appconnect'] - d['time_connect']
#    if t_ssl <= 0:  # no ssl was used
#        return 0
#    return t_ssl


def get_client_calculation_time(d):
    return d['time_pretransfer'] - d['time_appconnect']


def get_time_to_wait(d):
    return d['time_starttransfer'] - d['time_pretransfer']


def get_time_to_first_byte(d):
    return d['time_starttransfer']  # - d['time_pretransfer']


def get_data_receive_time(d):
    return d['time_total'] - d['time_starttransfer']


def calculate_timings(df):
    """
    :param df: curl timing data frame from curl_timings.py
    :return: df

    From https://ec.haxx.se/usingcurl-verbose.html:
    %{time_appconnect} shows the time, in seconds, it took from the start until the SSL/SSH/etc connect/handshake to the remote host was completed.
    %{time_connect} shows the time, in seconds, it took from the start until the TCP connect to the remote host (or proxy) was completed.
    %{time_namelookup} shows the time, in seconds, it took from the start until the name resolving was completed.
    %{time_pretransfer} shows the time, in seconds, it took from the start until the file transfer was just about to begin. This includes all pre-transfer commands and negotiations that are specific to the particular protocol(s) involved.
    %{time_redirect} shows the time, in seconds, it took for all redirection steps including name lookup, connect, pre-transfer and transfer before the final transaction was started. time_redirect shows the complete execution time for multiple redirections.
    %{time_starttransfer} shows the time, in seconds, it took from the start until the first byte was just about to be transferred. This includes time_pretransfer and also the time the server needed to calculate the result.
    %{time_total} shows the total time, in seconds, that the full operation lasted. The time will be displayed with millisecond resolution.

    Calculations:
    if not using HTTPS/SSL: time_appconnect returned is 0, so set time_appconnect = time_connect
    t_dns = time for DNS resolution (no redirects) = time_namelookup - time_redirect
    t_tcp = time for TCP connection (SYN/SYNACK) = time_connect - time_namelookup
    t_ssl = time for SSL handshake (only if https) = time_appconnect - time_connect
    t_fbyte = time_starttransfer
    t_wait = time between issuing GET request and first byte received (server calculation time) = time_starttransfer - time_pretransfer
    t_rx = time to receive data from first to last byte = time_total - time_starttransfer
    t_calc = waiting time between SSL and GET request = time_pretransfer - time_appconnect
    t_start = waiting time between issuing curl command and issuing first byte of data for DNS lookup
    t_stop = waiting time between receiving last byte and ending the curl command
    """

    df['t_dns'] = df.apply(get_dns_res_time, axis=1)

    df['t_tcp'] = df.apply(get_tcp_conn_time, axis=1)

    df['t_ssl'] = df.apply(lambda r: get_ssl_handshake_time(r), axis=1)

    df['ssl_flag'] = df['t_ssl'] != 0

    df['t_calc'] = df.apply(get_client_calculation_time, axis=1)

    df['t_wait'] = df.apply(get_time_to_wait, axis=1)

    df['t_fbyte'] = df.apply(get_time_to_first_byte, axis=1)
    #df['t_fbyte'] = df['time_starttransfer']

    df['t_rx'] = df.apply(get_data_receive_time, axis=1)

    return df


def calculate_sizes(df):
    """
    size upload and download
    """
    df['size_up'] = df['size_upload'] + df['size_request']
    df['size_dw'] = df['size_download'] + df['size_header']

    return df


def main():

    list_of_websites = CONST.list_of_websites
    nwebsites = CONST.nwebsites
    count = CONST.count
    nthreads = CONST.nthreads

    if os.path.exists(CONST.curl_timing_data_json):
        print("Load curl timing data file %s" % CONST.curl_timing_data_json)
        with open(CONST.curl_timing_data_json) as fin:
            curl_json_data = json.load(fin)
    else:
        print("Run curl requests to %s sites for %s loops" %(nwebsites, count))
        curl_json_data = parallel_requests(list_of_websites, nwebsites, nthreads, count)
        save_curl_timings_data(curl_json_data)

    df_timing = pd.DataFrame(curl_json_data)
    calculate_sizes(df_timing)
    calculate_timings(df_timing)

    print("Saved calculated df_timing for % sites %s threads %s" \
          " loops to %s" % (nwebsites, nthreads, count, CONST.df_timing_filepath))
    print(df_timing.head())
    df_timing.to_pickle(CONST.df_timing_filepath)

    return


if __name__ == '__main__':

    main()
