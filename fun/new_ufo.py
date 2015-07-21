# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 12:14:56 2015

@author: sinanozdemir
"""

import requests
from BeautifulSoup import BeautifulSoup


r = requests.get('http://www.nuforc.org/webreports/ndxe201507.html')

soup = BeautifulSoup(r.text)


rows = soup.findAll('tr', {'valign':'TOP'})

dates = [row.findChildren('td')[0].text for row in rows]
days = [d.split('/')[1] for d in dates]
days

from collections import Counter
import matplotlib.pyplot as plt
plt.plot(Counter(days).items())

rows[0].findChildren('td')[0].text
rows[0].findChildren('td')[1].text
rows[0].findChildren('td')[2].text
rows[0].findChildren('td')[3].text