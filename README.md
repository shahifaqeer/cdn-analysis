This is the repository for Timing Analysis of top Alexa websites grouped by CDN and ASN

The code is basically split into 3 parts: fetching ASN info, estimating CDN for website, and calculating timings for webpage load

- run.py is the main python file that is launched. It calls estimate_cdn.py, calculate_timings.py, and fetch_site_info.py
- fetch_site_info.py is used to download whois traces and website homepage for offline analysis
- curl_time_format.txt specifies the event timings to be returned by curl and saved as json
- CONST.py contains the runtime variables (number of alexa websites, link to top alexa csv file, number of threads to use and number of loops)
- utils/ contains an offline list of CDN names and domains, as well as code snippets used by above files
- estimate_cdn.py parses the whois data and the offline web page for HTML tags with static objects. More details below.
- calculate_timings.py runs multiple CURL requests in parallel with sufficient random delay to top Alexa websites 


CDN estimation algorithm:
# TODO see estimate_cdn_by_parse() in estimate_cdn.py


Requirements:
- cymruwhois
- pandas
- urllib
- requests
- python 3