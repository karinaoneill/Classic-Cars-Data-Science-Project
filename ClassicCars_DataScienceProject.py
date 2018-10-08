#import needed libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
%matplotlib inline
from urllib.request import urlopen   #to extract data from html files
from bs4 import BeautifulSoup   #bs4 = Beautiful Soup v4

url = "https://www.classiccarratings.com/auction-results?field_makecar_tid=All&field_yearcar_value%5Bmin%5D%5Byear%5D=1880&field_yearcar_value%5Bmax%5D%5Byear%5D=2001&field_modelcar_value=&field_date%5Bvalue%5D%5Bdate%5D=&sort_by=field_date_value"
html = urlopen(url)
soup = BeautifulSoup(html, 'lxml')

"""
next step is to access results table, which is not in a HTML table...
rows variable is first step to getting results table into Pandas dataframe:
using *= selector because div class names are named differently,
    e.g. <div class="views-row views-row-1 views-row-odd views-row-first">
         <div class="views-row views-row-2 views-row-even">     etc.
"""
rows=[]
for EachPart in soup.select('div[class*="views-row views-row-"]'):
    rows.append(EachPart.get_text())

rowssplit=[]

for i in rows:
    i=i.split(' \n')
    rowssplit.append(i)
    
for i in range(0,len(rowssplit)):
    del rowssplit[i][0], rowssplit[i][-1], rowssplit[i][-1], rowssplit[i][-2]   #remove fields that i won't use
    rowssplit[i][-1] = re.sub('\n', '', rowssplit[i][-1])   #take \n off price
    for j in range(0,4):   #to delete the field name info (i.e. 'Make:  ' etc). https://stackoverflow.com/questions/25045373/use-regex-re-sub-to-remove-everything-before-and-including-a-specified-word
        if ":  " in rowssplit[i][j]:
            rowssplit[i][j] = re.sub('^(.*:  )','',rowssplit[i][j])

df = pd.DataFrame(rowssplit)
df.columns = ['Make', 'Model', 'Year', 'Date', 'Price']
