

##  The packages.
import requests
import os 
import pandas
import argparse


##
##  Introduce the script.
'''
假設有一張資料表，
其中有某個欄位儲存了某段影片的連結位置，
根據影片連結下載影像資料。
'''
table = pandas.DataFrame(
    {
        "link":[
            "https://38.media.tumblr.com/9f6c25cc350f12aa74a7dc386a5c4985/tumblr_mevmyaKtDf1rgvhr8o1_500.gif",
            "https://38.media.tumblr.com/9ead028ef62004ef6ac2b92e52edd210/tumblr_nok4eeONTv1s2yegdo1_400.gif",
            "https://38.media.tumblr.com/9f43dc410be85b1159d1f42663d811d7/tumblr_mllh01J96X1s9npefo1_250.gif",
            "https://38.media.tumblr.com/9f659499c8754e40cf3f7ac21d08dae6/tumblr_nqlr0rn8ox1r2r0koo1_400.gif"
        ]
    }
)


##
##  The arguments.
title = "V"
folder = "LOG-{}".format(title)


##
##  Initial process.
os.makedirs(folder) if not os.path.isdir(folder) else None
for _, item in table.iterrows():
    
    url = item['link']
    name = str(url).split('/')[-1]
    with open(os.path.join(folder, name), 'wb') as paper:

        content = requests.get(url).content
        _ = paper.write(content)
        pass
    
    print(name)
    pass


# ##
# ##
# parser = argparse.ArgumentParser()
# parser.add_argument("fold", help="Min fold is 0, max fold is 9.", type=int)
# argument = parser.parse_args()


# ##
# ##
# table = pandas.read_csv('csv/tgif-v1.0.tsv', sep='\t', header=None)
# table.columns = ['link', 'text']
# fold = 10
# table['fold'] = list(table.index % fold)


# ##
# ##
# selection = table.loc[table['fold']==argument.fold]
# folder = os.path.join("gif", str(argument.fold))


# ##
# os.makedirs(folder) if not os.path.isdir(folder) else None
# for _, item in selection.iterrows():
    
#     url = item['link']
#     name = str(url).split('/')[-1]
#     with open(os.path.join(folder, name), 'wb') as paper:

#         content = requests.get(url).content
#         paper.write(content)
#         pass
    
#     print(name)
#     pass
