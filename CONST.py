list_of_websites = 'data/top-1m-new.csv'                # location of alexa top websites as RANK,SITE\n
# list_of_websites = 'data/test_bad_sites.csv'
nwebsites = 500                                         # top 500 websites default
count = 100                                             # count loops of curl requests default 100
nthreads = 25                                           # number of parallel threads for same url default 25

# these IPs are returned for block sites. Change this list to empty at another location
ips_blocked_by_ISP = ['49.207.46.6', '49.207.46.24', '49.207.46.34']

# standard filepaths for saving processed data
site_to_ip_json = "output/site_to_ip_%s.json" % (nwebsites)
ip_asn_json = "output/ip_asn_%s.json" % (nwebsites)
curl_timing_data_json = "output/curl_timing_count%s_sites%s.json" % (count, nwebsites)

CDN_data_object_path = "output/CDN_data_object_%s.pkl" % (nwebsites)

# filepaths for saving dataframes and results
df_timing_filepath = "results/df_timing.pkl"
df_ip_asn_filepath = "results/df_ip_asn.pkl"
df_cdn_filepath = "results/df_cdn.pkl"
