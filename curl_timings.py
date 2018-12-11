from __future__ import division
import numpy as np
import subprocess
import json



# csv read top 500 rows of websites
count = 100     # average timings over count loops of curl requests
# for each website COUNT time queries (in parallel)?
# for each result.response_code == '200' -> add to dict and find avg timings per website





site = 'wikipedia.org'
url = 'https://www.'+site+'/'


p = subprocess.Popen(['curl', '--connect-timeout', '3.0', '-o', '/dev/null',  '-w', '@curl_time_format.txt',
                      '-s', url], stdout=subprocess.PIPE)
out, err = p.communicate()


print(out)

result = json.loads(out.decode('UTF-8'))

print(result)
