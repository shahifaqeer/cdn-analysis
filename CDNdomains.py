# https://github.com/Hossein-Doroud/cdn-detector/blob/master/cdnDetector.py
# https://github.com/WPO-Foundation/webpagetest/blob/master/agent/wpthook/cdn.h

# Changes
# added microsoftonline.com is Auth portal but microsoftonline-p.com: Microsoft Office CDN
# remove doubleclick.net: BitGravity as doubleclick.net belongs to Google CDN
# added alicdn.com: Alibaba Cloud service
# added licdn.com: LinkedIn CDN to host images and media
# added nflxvideo.net,.nflxext.com : Open-Connect Netflix (https://firebounty.com/104-netflix)
# added msocdn.com, cdn.office.net: Akamai CDN for microsoft office 365 services (https://www.dns-as.org/support/dns-as-cloud-apps/)
# added ssl-images-amazon.com: Amazon CloudFront
# redditstatic.com is currently hosted by Fastly, but was previously Cloudfront, and even earlier Akamai. Use whois.
# added .atlassian.com: Amazon CloudFront, belongs to AS16509 Amazon AWS
# added .pstatic.net: Akamai, belongs to AS16625 to serve content
# added .sfdcstatic: Akamai for Salesforce
# added .cdn.sohucs.com: Sohu CS Media currently hosted by Beijing Media
# added .office365.com: Akamai although it is auth portal for microsoft office
# replaced all Akamai Microsoft resources with Microsoft
# add .media-amazon.com:"Amazon CloudFront"
# TO ADD .twitchcdn.net: Fastly
# remove KT, SKY from cdn_names as comparison was causing errors due to partial matches
# replace Instartlogic by Instart Logic for better matches on whois
# remove/comment out ".pix-cdn.org":"Advanced Hosters CDN" - txxx.com should be cloudfront based on whois IP
# replace ".tl88.net":"Akamai China CDN" with just Akamai to avoid confusion
# add ytimg.com:Google for youtubeimage cdn

#cdn_domain = cdnFinder + github_cdn_List

cdn_domains = {
  ".microsoftonline-p.com":"Microsoft",
  ".microsoftonline-p.net":"Microsoft",
  ".microsoftonline.com":"Microsoft",
  ".alicdn.com":"Alibaba",
  ".licdn.com":"LinkedIn CDN",
  ".nflxvideo.net":"Open-Connect (Netflix)",
  ".msocdn.com":"Microsoft",
  ".cdn.office.net":"Microsoft",
  ".ssl-images-amazon.com":"Amazon CloudFront",
  ".atlassian.com":"Amazon CloudFront",
  ".pstatic.net":"Akamai",
  ".sfdcstatic.com":"Akamai",
  ".cdn.sohucs.com":"Sohu",
  ".office365.com":"Microsoft Azure",
  ".nflxext.com":"Open-Connect (Netflix)",
  ".media-amazon.com":"Amazon CloudFront",
  ".ytimg.com":"Google",
  ".clients.turbobytes.net":"TurboBytes",
  ".turbobytes-cdn.com":"TurboBytes",
  ".afxcdn.net":"afxcdn.net",
  ".akamai.net":"Akamai",
  ".akamaiedge.net":"Akamai",
  ".akadns.net":"Akamai",
  ".akamaitechnologies.com":"Akamai",
  ".gslb.tbcache.com":"Alimama",
  ".cloudfront.net":"Amazon CloudFront",
  ".anankecdn.com.br":"Ananke",
  ".att-dsa.net":"AT&T",
  ".azioncdn.net":"Azion",
  ".belugacdn.com":"BelugaCDN",
  ".bluehatnetwork.com":"Blue Hat Network",
  ".systemcdn.net":"EdgeCast",
  ".cachefly.net":"Cachefly",
  ".cdn77.net":"CDN77",
  ".cdn77.org":"CDN77",
  ".panthercdn.com":"CDNetworks",
  ".cdngc.net":"CDNetworks",
  ".gccdn.net":"CDNetworks",
  ".gccdn.cn":"CDNetworks",
  ".cdnify.io":"CDNify",
  ".ccgslb.com":"ChinaCache",
  ".ccgslb.net":"ChinaCache",
  ".c3cache.net":"ChinaCache",
  ".chinacache.net":"ChinaCache",
  ".c3cdn.net":"ChinaCache",
  ".lxdns.com":"ChinaNetCenter",
  ".speedcdns.com":"QUANTIL/ChinaNetCenter",
  ".cloudflare.com":"Cloudflare",
  ".cloudflare.net":"Cloudflare",
  ".edgecastcdn.net":"EdgeCast",
  ".adn.":"EdgeCast",
  ".wac.":"EdgeCast",
  ".wpc.":"EdgeCast",
  ".fastly.net":"Fastly",
  ".fastlylb.net":"Fastly",
  ".google.":"Google",
  ".googlesyndication.":"Google",
  ".youtube.":"Google",
  ".googleusercontent.com":"Google",
  ".l.doubleclick.net":"Google",
  ".hiberniacdn.com":"HiberniaCDN",
  ".hwcdn.net":"Highwinds",
  ".incapdns.net":"Incapsula",
  ".inscname.net":"Instart Logic",
  ".insnw.net":"Instart Logic",
  ".internapcdn.net":"Internap",
  ".kxcdn.com":"KeyCDN",
  ".lswcdn.net":"LeaseWeb CDN",
  ".footprint.net":"Level3",
  ".llnwd.net":"Limelight",
  ".lldns.net":"Limelight",
  ".netdna-cdn.com":"MaxCDN",
  ".netdna-ssl.com":"MaxCDN",
  ".netdna.com":"MaxCDN",
  ".mncdn.com":"Medianova",
  ".instacontent.net":"Mirror Image",
  ".mirror-image.net":"Mirror Image",
  ".cap-mii.net":"Mirror Image",
  ".rncdn1.com":"Reflected Networks",
  ".simplecdn.net":"Simple CDN",
  ".swiftcdn1.com":"SwiftCDN",
  ".swiftserve.com":"SwiftServe",
  ".gslb.taobao.com":"Taobao",
  ".cdn.bitgravity.com":"Tata communications",
  ".cdn.telefonica.com":"Telefonica",
  ".vo.msecnd.net":"Microsoft Azure",
  ".ay1.b.yahoo.com":"Yahoo",
  ".yimg.":"Yahoo",
  ".zenedge.net":"Zenedge",

  ".akamai.net":"Akamai",
  ".akamaized.net":"Akamai",
  ".akamaiedge.net":"Akamai",
  ".akamaihd.net":"Akamai",
  ".edgesuite.net":"Akamai",
  ".edgekey.net":"Akamai",
  ".srip.net":"Akamai",
  ".akamaitechnologies.com":"Akamai",
  ".akamaitechnologies.fr":"Akamai",
  ".tl88.net":"Akamai",
  ".llnwd.net":"Limelight",
  ".edgecastcdn.net":"EdgeCast",
  ".systemcdn.net":"EdgeCast",
  ".transactcdn.net":"Edgecast",
  ".v1cdn.net":"Edgecast",
  ".v2cdn.net":"Edgecast",
  ".v3cdn.net":"Edgecast",
  ".v4cdn.net":"Edgecast",
  ".v5cdn.net":"Edgecast",
  ".hwcdn.net":"Highwinds",
  ".simplecdn.net":"Simple CDN",
  ".instacontent.net":"Mirror Image",
  ".footprint.net":"Level3",
  ".fpbns.net":"Level 3",
  ".ay1.b.yahoo.com":"Yahoo",
  ".yimg.":"Yahoo",
  ".yahooapis.com":"Yahoo",
  ".google.":"Google",
  ".googlesyndication.":"Google",
  ".youtube.":"Google",
  ".googleusercontent.com":"Google",
  ".googlehosted.com":"Google",
  ".gstatic.com":"Google",
  ".insnw.net":"Instart Logic",
  ".inscname.net":"Instart Logic",
  ".internapcdn.net":"Internap",
  ".cloudfront.net":"Amazon CloudFront",
  ".netdna-cdn.com":"MaxCDN",
  ".netdna-ssl.com":"MaxCDN",
  ".kxcdn.com":"KeyCDN",
  ".cotcdn.net":"Cotendo CDN",
  ".cachefly.net":"Cachefly",
  ".bo.lt":"BO.LT",
  ".cloudflare.com":"Cloudflare",
  ".afxcdn.net":"afxcdn.net",
  ".lxdns.com":"ChinaNetCenter",
  ".wscdns.com":"ChinaNetCenter",
  ".wscloudcdn.com":"ChinaNetCenter",
  ".ourwebpic.com":"ChinaNetCenter",
  ".att-dsa.net":"AT&T",
  ".vo.msecnd.net":"Microsoft Azure",
  ".azureedge.net":"Microsoft Azure",
  ".voxcdn.net":"VoxCDN",
  ".bluehatnetwork.com":"Blue Hat Network",
  ".swiftcdn1.com":"SwiftCDN",
  ".cdngc.net":"CDNetworks",
  ".gccdn.net":"CDNetworks",
  ".panthercdn.com":"CDNetworks",
  ".fastly.net":"Fastly",
  ".fastlylb.net":"Fastly",
  ".nocookie.net":"Fastly",
  ".gslb.taobao.com":"Taobao",
  ".gslb.tbcache.com":"Alimama",
  ".mirror-image.net":"Mirror Image",
  ".yottaa.net":"Yottaa",
  ".cubecdn.net":"cubeCDN",
  ".cdn77.net":"CDN77",
  ".cdn77.org":"CDN77",
  ".incapdns.net":"Incapsula",
  ".r.worldcdn.net":"OnApp",
  ".r.worldssl.net":"OnApp",
  ".tbcdn.cn":"Taobao",
  ".taobaocdn.com":"Taobao",
  ".ngenix.net":"NGENIX",
  ".pagerain.net":"PageRain",
  ".ccgslb.com":"ChinaCache",
  ".cdn.sfr.net":"SFR",
  ".azioncdn.net":"Azion",
  ".azioncdn.com":"Azion",
  ".azion.net":"Azion",
  ".cdncloud.net.au":"MediaCloud",
  ".rncdn1.com":"Reflected Networks",
  ".cdnsun.net":"CDNsun",
  ".mncdn.com":"Medianova",
  ".mncdn.net":"Medianova",
  ".mncdn.org":"Medianova",
  ".cdn.jsdelivr.net":"jsDelivr",
  ".nyiftw.net":"NYI FTW",
  ".nyiftw.com":"NYI FTW",
  ".resrc.it":"ReSRC.it",
  ".zenedge.net":"Zenedge",
  ".lswcdn.net":"LeaseWeb CDN",
  ".lswcdn.eu":"LeaseWeb CDN",
  ".revcn.net":"Rev Software",
  ".revdn.net":"Rev Software",
  ".caspowa.com":"Caspowa",
  ".twimg.com":"Twitter",
  ".facebook.com":"Facebook",
  ".facebook.net":"Facebook",
  ".fbcdn.net":"Facebook",
  ".cdninstagram.com":"Facebook",
  ".rlcdn.com":"Reapleaf",
  ".wp.com":"WordPress",
  ".aads1.net":"Aryaka",
  ".aads-cn.net":"Aryaka",
  ".aads-cng.net":"Aryaka",
  ".squixa.net":"section.io",
  ".bisongrid.net":"Bison Grid",
  ".cdn.gocache.net":"GoCache",
  ".hiberniacdn.com":"HiberniaCDN",
  ".cdntel.net":"Telenor",
  ".raxcdn.com":"Rackspace",
  ".unicorncdn.net":"UnicornCDN",
  ".optimalcdn.com":"Optimal CDN",
  ".kinxcdn.com":"KINX CDN",
  ".kinxcdn.net":"KINX CDN",
  ".stackpathdns.com":"StackPath",
  ".hosting4cdn.com":"Hosting4CDN",
  ".netlify.com":"Netlify",
  ".b-cdn.net":"BunnyCDN",
  #".pix-cdn.org":"Advanced Hosters CDN"
}

# for checking whois Organizations
# add Amazon.com, Inc., Amazon Technologies Inc. for sites on amazon aws (may not be on cloudfront)
# remove Instart only keep Instart Logic for better matches on whois
# remove repeats like Google Cloud, Level 3, etc. for better matches
cdn_names = [
  'AAPT',
  'ARA Networks',
  'AT&T',
  'Akamai',
  'Alibaba',
  'Allot Communications',
  'Amazon Technologies Inc.',
  'Amazon.com, Inc.',
  'Amazon Data Services',
  'CloudFront',
  'Aryaka',
  'Azure CDN',
  'BT',
  'BT Group',
  'BTI Systems',
  ' Bell ',
  'BelugaCDN',
  'Bharti Airtel',
  'BitTorrent',
  'Blue Coat',
  'BootstrapCDN',
  'Broadmedia',
  'Broadpeak',
  'CDN77',
  'CDNetworks',
  'CacheFly',
  'Cedexis',
  'CenterServ',
  'Century Link',
  'China Telecom',
  'ChinaCache',
  'ChinaNetCenter',
  'Cisco',
  'Cloudflare',
  'Comcast',
  'Concentric',
  'Concurrent',
  'Conversant',
  'Conviva',
  'Coral',
  'Cotendo',
  'Deutsche Telekom',
  'EdgeCast',
  'Edgeware',
  'Ericsson',
  'Fastly',
  'Fortinet',
  'Google',
  'HP Cloud Services',
  'HiNet',
  'Hibernia Networks',
  'Highwinds',
  'Hola',
  'Huawei',
  'Incapsula',
  'IneoQuest',
  'Instart Logic',
  'Interferex',
  'Internap',
  'Interoute',
  'JSDelivr',
  'Jetstream',
  'Juniper ',
  'KPN',
  'Korea Telecom',
  'LeaseWeb',
  'Level 3',
  'Limelight Networks',
  'Megafon',
  'MetaCDN',
  'Microsoft Azure',
  'MileWEB',
  'Mirror Image',
  'NACEVI',
  'NTT',
  'NTT Communications',
  'NaviSite',
  'Ngenix',
  'Nice People At Work',
  'Nokia',
  'OVH',
  'OnApp',
  'Ono',
  'Orange',
  'PCCW',
  'Pacnet',
  'Pando Networks',
  'PeerApp',
  'Qualitynet',
  'Qwilt',
  'Rackspace Cloud Files',
  'Radware',
  'Rawflow',
  'Reliance Globalcom',
  'RevAMP',
  'SFR',
  'SK Broadband',
  'SoftLayer',
  'SSIMWave',
  'STC',
  'SingTel',
  'Solbox',
  'Spark New Zealand',
  'Speedera Networks',
  'StackPath',
  'StreamZilla',
  'Swarmify',
  'Swiftserve',
  'Swisscom',
  'Tata Communications',
  'Telcom Italia',
  'Telecom Argentina',
  'Telecom Italia',
  'Telecom Italia Sparkle',
  'Telecom Malaysia',
  'Telefonica',
  'Telenor',
  'TeliaSonera',
  'Telin',
  'Telstra',
  'Telus',
  'Touchstream',
  'Turk Telekom',
  'Varnish',
  'Verizon',
  'Vidscale',
  'Wangsu Science & Technology',
  'Webscale',
  'Yottaa'
]

manual_inspection = {
	"clara.net":{'name': 'clara', 'label': ['cloud']},
	"apsalar.com":{'name':'apsalar', 'label': ['cloud']},
	"sgded.com":{'name': 'sgded', 'label': ['cdn','cloud']},
	"vrvm.com":{'name':'vrvm', 'label': ['cloud']},
	"leaseweb.com":{'name': 'leaseweb', 'label': ['cloud','cdn']},
	"leaseweb.net":{'name': 'leaseweb', 'label': ['cloud','cdn']},
	"psychz.net":{'name':'psychz', 'label': ['cloud','cdn']},
	"rockynet.com":{'name': 'rockynet', 'label': ['cloud']},
	"dslnet.pk":{'name':'dsl', 'label': ['cloud']},
	"nyinternet.net":{'name':'nyinternet', 'label': ['cloud']},
	"purepeak.com":{'name': 'purepeak', 'label': ['cloud']},
	"virtua.com.br":{'name':'virtua', 'label': ['cloud']},
	"inmotionhosting.com":{'name': 'inmotionhosting', 'label': ['cloud']},
	"hostgator.com":{'name':'hostgator', 'label': ['cloud']},
	"dreamhost.com":{'name': 'dreamhost', 'label': ['cloud']},
	"hostingxs.nl":{'name':'hostingxs', 'label': ['cloud','cdn']},
	"xlhost.com":{'name': 'xlhost', 'label': ['cloud']},
	"hosting.com":{'name':'hosting', 'label': ['cloud']},
	"hostnet.nl":{'name': 'hostnet', 'label': ['cloud']},
	"bluehost.com":{'name':'bluehost', 'label': ['cloud']},
	"hosteurope.de":{'name': 'hosteurope', 'label': ['cloud']},
	"hiberniacdn":{'name':'hiberniacdn', 'label': ['cdn']},
	"1e100.net":{'name': 'Google', 'label': ['cdn']},
	"bandwidthx.net":{'name': 'bandwidthx', 'label': ['cloud']},
	"googlevideo.com":{'name':'Google', 'label': ['cdn']},
	"cdngp.net":{'name': 'cdngp', 'label': ['cdn']},
	"dc-msedge.net":{'name':'dc-msedge', 'label': ['cdn']},
	"basefarm.net":{'name': 'basefarm', 'label': ['cloud']},
	"cdnetworks.com":{'name':'cdnetworks', 'label': ['cdn']},
	"yimg.com":{'name': 'Yahoo', 'label': ['cdn']},
	"x2n.com.br":{'name':'x2n', 'label': ['cdn']},
	"amazonaws.com":{'name': 'amazonaws', 'label': ['cloud']},
	"aclst.com":{'name':'aclst', 'label': ['cloud']},
	"emv2.com":{'name': 'emv2', 'label': ['cloud']},
	"open-telekom-cloud.com":{'name': 'Open Telekom', 'label': ['cloud']},
	"hostpoint.ch":{'name': 'hostpoint', 'label': ['cloud']},
	"idealhosting.net.tr":{'name': 'idealhosting', 'label': ['cloud']},
	"aruba.it":{'name': 'aruba', 'label': ['cloud']},
	"quadhost.net":{'name': 'quadhost', 'label': ['cloud']},
	"fasthosts.net.uk":{'name': 'fasthosts', 'label': ['cloud']},
	"xlshosting.net":{'name': 'xlshosting', 'label': ['cloud']},
	"hostforweb.com":{'name': 'hostforweb', 'label': ['cloud']},
	"a2hosting.com":{'name': 'a2hosting', 'label': ['cloud']},
	"nexxea.com":{'name': 'ovh', 'label': ['cloud']},
	"theplanet.com":{'name': 'theplanet', 'label': ['cloud']},
	"cloudn-service.com":{'name': 'ntt', 'label': ['cloud']},
	"myracloud.com":{'name': 'myracloud', 'label': ['cdn']},
	"cloudvps.com":{'name': 'cloudvps', 'label': ['cloud']},
	"cbici.net":{'name': 'cbi', 'label': ['cloud']},
}

# Dictionary of ASs which are dedicated entirely to a given CSP
as_dict = {
393245:{'csp':'Yahoo', 'as_name':'yahoo-swb', 'class':'Enterpise'},
36408:{'csp':'cdngp', 'as_name':'cdnetworksus-02', 'class':'Content'},
10297:{'csp':'xlhost', 'as_name':'enet-2', 'class':'Content'},
25148:{'csp':'basefarm', 'as_name':'basefarm-asn', 'class':'Content'},
19551:{'csp':'Incapsula', 'as_name':'incapsula', 'class':'Content'},
35994:{'csp':'Akamai', 'as_name':'akamai-as', 'class':'Transit/Access'},
14618:{'csp':'amazonaws', 'as_name':'amazon-aes', 'class':'Content'},
32934:{'csp':'Facebook', 'as_name':'facebook', 'class':'Content'},
26347:{'csp':'dreamhost', 'as_name':'dreamhost-as', 'class':'Content'},
16625:{'csp':'Akamai', 'as_name':'akamai-as', 'class':'Content'},
197902:{'csp':'hostnet', 'as_name':'hostnet', 'class':'Content'},
33047:{'csp':'Instartlogic', 'as_name':'instart', 'class':'Content'},
15169:{'csp':'Google', 'as_name':'google', 'class':'Content'},
54641:{'csp':'inmotionhosting', 'as_name':'inmoti-1', 'class':'Content'},
14196:{'csp':'Yahoo', 'as_name':'yahoo-cha', 'class':'Enterpise'},
14776:{'csp':'Yahoo', 'as_name':'inktomi-lawson', 'class':'-'},
34164:{'csp':'Akamai', 'as_name':'akamai-lon', 'class':'Transit/Access'},
20940:{'csp':'Akamai', 'as_name':'akamai-asn1', 'class':'Content'},
20446:{'csp':'Highwinds', 'as_name':'highwinds3', 'class':'Content'},
39905:{'csp':'smartfocus', 'as_name':'emailvision', 'class':'Content'},
38895:{'csp':'amazonaws', 'as_name':'amazon-as-ap', 'class':'Transit/Access'},
60922:{'csp':'HiberniaCDN', 'as_name':'Hibernia-cdn', 'class':'Transit/Access'},
16509:{'csp':'amazonaws', 'as_name':'amazon-02', 'class':'Enterpise'},
30081:{'csp':'Cachefly', 'as_name':'cachenetworks', 'class':'Content'},
8068:{'csp':'dc-msedge', 'as_name':'microsoft-corp-msn-as-block', 'class':'Enterpise'},
22611:{'csp':'inmotionhosting', 'as_name':'imh-west', 'class':'Content'},
34879 : {'as_name': 'CCT-AS NGENIX', 'csp': 'NGENIX', 'class':'Content'},
43428 : {'as_name': 'YAHOO-ULS', 'csp': 'Yahoo', 'class':''},
16265 : {'as_name': 'LEASEWEB-NETWORK Amsterdam', 'csp': 'leaseweb', 'class':'Content'},
29097 : {'as_name': 'hostpoint-as', 'csp': 'hostpoint', 'class':'Content'},
21342 : {'as_name': 'AKAMAI-ASN2', 'csp': 'Akamai', 'class':'Transit/Access'},
8523 : {'as_name': 'BASEFARM-SE-ASN Basefarm AB. Stockholm', 'csp': 'basefarm', 'class':'Enterpise'},
24319 : {'as_name': 'AKAMAI-TYO-AP Akamai Technologies Tokyo ASN', 'csp': 'Akamai', 'class':'Transit/Access'},
29798 : {'as_name': 'HIGHWINDS5', 'csp': 'Highwinds', 'class':'Transit/Access'}
}