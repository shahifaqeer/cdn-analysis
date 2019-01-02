# ThousandEyes Internet Measurement Challenge

This is the repository for Timing Analysis of top Alexa websites grouped by CDN
and ASN. We use curl for timing analysis, and parse html tags and whois traces
for CDN estimation (details below).

### Execution

`python run.py`
- use `CONST.py` to change runtime variables (temporary)
- creates output/ and results/ folder in code directory
- ensure data/ directory contains path to alexa top sites csv (rank,site)
- uses CDN names and domains from `utils/CDNdomains.py`

### Plotting

To replot results run `jupyter notebook`. The current ipython notebook analysis
requires df_timing.pkl, df_cdn.pkl, and df_asn.pkl in the results/ folder. These
files are generated once you run `python run.py` in the home directory.

To view results and plots of the current dataset, click the following links:

- [Analysis-CDN.ipynb](https://gitlab.com/sgrover/thousandeyeschallenge/blob/master/Analysis-CDN.ipynb)
- [Analysis-ASN.ipynb](https://gitlab.com/sgrover/thousandeyeschallenge/blob/master/Analysis-ASN.ipynb)
- [Analysis-Timing.ipynb](https://gitlab.com/sgrover/thousandeyeschallenge/blob/master/Analysis-Timing.ipynb)


#### Note regarding current results
A backup of the current results is available in results_old/ folder in case
data is overwritten. Some previous results, such as comparison between curl data
without redirects vs with redirects can only be plotted using downloaded 
data output/curl-timing-data-reorder-count100-sites500.json and 
output/curl_timing_count100_sites500.json. These files have been copied to the
results_old/ directory for ease of reproducing the analysis.

## Requirements:

- cymruwhois
- pandas
- bs4 (BeautifulSoup)
- urllib
- requests
- python 3


## Components

The code is basically split into 3 parts: fetching ASN info, estimating CDN for
website, and calculating timings for webpage load.

- `run.py` is the main python file that is launched. It calls `estimate_cdn.py`,
`calculate_timings.py`, and `fetch_site_info.py`.
- `fetch_site_info.py` is used to download whois traces and website homepage for
offline analysis to the output/ directory.
- `curl_time_format.txt` specifies the event timings format to be returned by
curl and saved as a json.
- `CONST.py` contains the runtime variables (number of alexa websites,
link to top alexa csv file, number of threads to use, number of loops, etc.). To
change the link to Alexa file and the number of sites to analyze, make changes
to `CONST.py` before running the code.
- utils/ contains an offline list of CDN names and domains, as well as code
snippets used by `estimate_cdn.py` and `calculate_timings.py`
- `estimate_cdn.py` parses the whois data and the offline web page for HTML tags
with static objects (more details in CDN Estimation Algorithm below)
- `calculate_timings.py` runs multiple CURL requests in parallel with sufficient
random delay to top Alexa websites 

# CDN Estimation Algorithm

Create a `CDN(rank,site)` object and call `CDN.process()`. The aim is to
use multiple techniques to estimate the cdn and finally decide based on 
the following priority
- CDN.cdn_by_xcache: # TODO find 'x-cache': HIT or MISS in HTTP headers and
match to CDN name
- CDN.cdn_by_site: match site to known cdn domains
- CDN.cdn_by_cname: # TODO find if object dns.cname points to a CDN url
- CDN.cdn_by_parse: parse html page and return most popular matched cdn
- CDN.cdn_by_whois: parse whois data and return matched cdn in Organization
field


1. Create the CDN object
    - matches the site domain name to known CDN names. If found, set the 
CDN.cdn_by_site to the matched_cdn
    - parses whois data to its IP address and uses utils.parse_whois
to find if the "Organization" field in whois matches a known CDN name. If found,
set CDN.cdn_by_whois to the matched_cdn
2. `CDN.get_homepage_url_count()`: Use BeatifulSoup to parse the
downloaded homepage for the following tags:
`["script src", "img src", "source srcset", "source data-srcset", "link href"]`
3. `CDN.count_netlocs()`: For each source url to a static object, find the
type and location using `urllib.parse.urlparse()` method
4. `CDN.object_url_to_cdn()`: For list of object locations, find CDN name based
on object URL, and count the number of static objects that location is hosting
in CDN.object_cdn{}
    - TODO: if object is hosted locally: increment CDN.object_cdn["local"]+=1
    - if object is hosted externally, find the cdn_domain of the url
        - match url and cdn_domain from utils/CDNdomains.py
        - if matched_cdn found, increment CDN.object_cdn[matched_cdn]+=1
    - if object is hosted externally, and cdn_domain is not found
        - check if object url is a CDN (contains string ".cdn") and add it to
CDN url list and increment CDN.object_cdn[cdn_url]+=1
        - if url is not a cdn url, add the external link to CDN.object_unknown
and increment CDN.object_cdn["unknown"]+=1
5. `CDN.estimate_cdn_by_parse()`: Sort the CDN.object_cdn{cdn:count} counter
by values and calculate the score for each cdn as cdn_count/total_count
    - assume the most likely_cdn_name is the first cdn in sorted counter
    - if likely_cdn_name is not "unknown" and its score > 0.5 (i.e, more than
half the external objects on webpage are hosted on this url), then assume
CDN.cdn_by_parse is the likely_cdn_name
    - if likely_cdn_name is "unknown" (TODO: or "local"), then count the
external url links stored in CDN.object_unknown, sort by number of links, and
if the url_score (numlinks_to_external_url/total_count) > 0.5, return external
url as CDN.most_linked_url, but keep CDN.cdn_by_parse as None
6. `CDN.estimate_cdn()`: Finally, CDN.cdn is decided based on priority:
CDN.cdn_by_xcache or CDN.cdn_by_site or CDN.cdn_by_cname or CDN.cdn_by_parse
    - optionally, if CDN.cdn is still none, use CDN.cdn_by_whois as final CDN