import numpy as np
import re
import requests
import HTMLParser
import pandas
from BeautifulSoup import BeautifulSoup
import pickle

def attempt(s):
    try:
        return float(s.replace(',','').replace('%',''))
    except:
        pass
    return s

def gatherStats():
    h = HTMLParser.HTMLParser()
    dict_of_df = {}
    for pos, pos_id in [('QB', 10), ('RB', 20), ('WR', 30), ('TE', 40), ('K', 80), ('DEF', 99)]:
        print pos, pos_id
        pos_id = str(pos_id)
        cleaned_rows = []
        for page_id in range(2):
            page_id = str(page_id)
            p = BeautifulSoup(h.unescape(requests.get('http://fftoday.com/stats/playerstats.php?Season=2014&PosID='+pos_id+'&cur_page='+page_id).text))        
            if pos != 'DEF':
                cols = ['Name', 'Pos'] + [re.search('.*order_by=(\w+)', a['href']).group(1) for a in p.findAll('tr')[19].findChildren('a')[4::2]]        
            else:
                cols = ['Name', 'Pos'] + [re.search('.*order_by=(\w+)', a['href']).group(1) for a in p.findAll('tr')[19].findChildren('a')[2::2]]                    
            rows = p.findAll('tr')[20:-1]
            for row in rows:
                cleaned_rows.append([row.findChild('td').findChild('a').text, pos]+[attempt(a.text) for a in row.findChildren('td')[1:]])
        dict_of_df[pos] = pandas.DataFrame(cleaned_rows, columns=cols)
    with open('nfl_model.pkl', 'wb') as f:
        pickle.dump(dict_of_df, f)
    return dict_of_df
      
# data_frame = gatherStats()

def calculateImportances(dict_of_df):
    for pos, pos_id in [('QB', 10), ('RB', 20), ('WR', 30), ('TE', 40), ('K', 80), ('DEF', 99)]:  
        numeric_cols = list(dict_of_df[pos].columns[4:])
        def difference_from_centroid(r):
            return round(np.mean((r[numeric_cols] - dict_of_df[pos][numeric_cols].mean()) / dict_of_df[pos][numeric_cols].std()), 2)
        dict_of_df[pos]['distance'] = dict_of_df[pos].apply(difference_from_centroid, axis = 1)
    return dict_of_df
    
# data_frame = gatherStats(data_frame)
# adds an importance columns

# dict_of_df['QB'].sort_index(by = 'distance', ascending = False).head(10)

def removePlayerFromPos(dict_of_df, name, pos):
    name = name.lower()
    pos = pos.upper()
    try:
        dict_of_df[pos] = dict_of_df[pos][dict_of_df[pos].Name.str.lower() != name]
    except:
        pass

# removePlayerFromPos(data_frame, 'Russell Wilson', 'qb')








