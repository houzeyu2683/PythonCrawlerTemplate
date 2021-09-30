

##  The packages.
import requests
import os 
import pandas
import argparse


##
parser = argparse.ArgumentParser()
parser.add_argument("fold", help="Min fold is 0, max fold is 9.", type=int)
argument = parser.parse_args()


##
table = pandas.read_csv('csv/tgif-v1.0.tsv', sep='\t', header=None)
table.columns = ['link', 'text']
fold = 10
table['fold'] = list(table.index % fold)


##
selection = table.loc[table['fold']==argument.fold]
folder = os.path.join("gif", str(argument.fold))


##
os.makedirs(folder) if not os.path.isdir(folder) else None
for _, item in selection.iterrows():
    
    url = item['link']
    name = str(url).split('/')[-1]
    with open(os.path.join(folder, name), 'wb') as paper:

        content = requests.get(url).content
        paper.write(content)
        pass
    
    print(name)
    pass