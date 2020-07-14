import pandas as pd
import wget
import os
import pdb
from conf import *

os.system('rm *export*')
big_df = pd.DataFrame()

for state in LOCATIONS:
    state_url = state.replace(' ', '%20')
    cities = LOCATIONS[state]
    url = 'https://www.repeaterbook.com/api/export.php?state={}'.format(state_url)
    
    filename = wget.download(url)
    f = open(filename)
    data = f.read()
    
    df = pd.DataFrame(list(pd.read_json(data)['results']))
    cols = list(df.columns)
    
    del_cols = list()
    for col in cols:
        if col not in COLUMNS:
            del_cols.append(col)
    
    df = df.drop(columns=del_cols)
   
    df = df.loc[df['State'] == state]            # Remove anything that isn't in the state
    df = df.loc[df['Nearest City'].isin(cities)] # Remove anything that isn't in the city
    
    df = df.sort_values(by=['Nearest City'])
    big_df = pd.concat([big_df, df])

header = open('template.tex', 'r').read()
output = '{} \n {} \n'.format(header, big_df.to_latex(longtable = True, index=False)) + '\end{document}'

open('output.tex', 'w').write(output)
os.system('pdflatex output.tex')      # Compile the document
os.system('open output.pdf')      # Compile the document
