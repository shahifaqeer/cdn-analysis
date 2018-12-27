"""
required
- cymruwhois
- urllib
- requests
- pandas

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