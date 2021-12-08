

##  The packages.
from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.common.by import By
import pandas, os, tqdm, time


##  The goal.
'''
根據 query 從 PubMed 搜尋引擎下載對應的文章摘要，輸出成表格。
'''


##  The arguments.
keyword = "Athlete's foot"
platform = "pubmed"
site   = "https://pubmed.ncbi.nlm.nih.gov/"
number = 10
folder = "LOG/VI/{}".format(keyword)
os.makedirs(folder) if not os.path.isdir(folder) else None


##
option = webdriver.chrome.options.Options()
option.binary_location = "/usr/bin/google-chrome"
# option.add_argument('--no-sandbox')
service = chrome.service.Service(executable_path='driver/chrome')
driver = webdriver.Chrome(options=option, service=service)
page = range(1, number+1, 1)
group = {
    "link":[],
    "title":[],
    "abstract":[],
    "tag":[],
    "author":[]
}
for p in page:
        
    try:

        driver.get("{}?term={}&filter=simsearch1.fha&page={}".format(site, keyword, p))
        # group['link'] += [i.get_attribute("href") for i in driver.find_elements_by_css_selector(".docsum-title")]
        group['link'] += [i.get_attribute("href") for i in driver.find_elements(By.CSS_SELECTOR, ".docsum-title")]
        pass

    except:

        continue

    pass

link = pandas.DataFrame({"link":group['link']})
link.to_csv(os.path.join(folder, "link.csv"), index=False)

def remove(x, what=""):

    output = []
    for i in x:

        if(i==what):

            continue

        else:

            output += [i]
            pass

        pass
    
    return(output)

for l in tqdm.tqdm(group['link'], total=len(group['link'])):

    try:

        driver.get(l)
        pass

    except:

        group['title'] += [None]
        group['abstract'] += [None]
        group['tag'] += [None]
        group['author'] += [None]            
        continue

    try:
        
        # title = driver.find_element_by_css_selector(".heading-title").text
        title = driver.find_element(By.CSS_SELECTOR, ".heading-title").text        
        pass

    except:

        title = None
        pass

    try:
        
        # abstract = driver.find_element_by_css_selector("#enc-abstract p").text
        abstract = driver.find_element(By.CSS_SELECTOR, "#enc-abstract p").text
        pass

    except:

        abstract = None
        pass

    try:

        # tag = driver.find_element_by_css_selector("#enc-abstract+ p").text.split(": ")[-1]
        tag = driver.find_element(By.CSS_SELECTOR, "#enc-abstract+ p").text.split(": ")[-1]
        pass

    except:

        tag = None
        pass

    try:
        
        # author = ";".join(remove([i.text for i in driver.find_elements_by_css_selector(".full-name")], what=''))
        author = ";".join(remove([i.text for i in driver.find_elements(By.CSS_SELECTOR, ".full-name")], what=''))        
        pass

    except:

        author = None
        pass

    group['title'] += [title]
    group['abstract'] += [abstract]
    group['tag'] += [tag]
    group['author'] += [author]
    time.sleep(1)
    pass

table = pandas.DataFrame(group)
table.to_csv(os.path.join(folder, "data.csv"), index=False)
driver.close()
pass


# ##  The arguments.
# keyword = ["chest cavity"]
# for k in keyword:

#     platform = "pubmed"
#     site   = "https://pubmed.ncbi.nlm.nih.gov/"
#     number = 100
#     folder = "resource/csv/{}".format(k)
#     os.makedirs(folder) if not os.path.isdir(folder) else None


#     ##
#     ##
#     option = webdriver.chrome.options.Options()
#     option.binary_location = "/usr/bin/google-chrome"
#     # option.add_argument('--no-sandbox')
#     driver = webdriver.Chrome(options=option, executable_path='driver/chrome')
#     page = range(1, number+1, 1)
#     group = {
#         "link":[],
#         "title":[],
#         "abstract":[],
#         "tag":[],
#         "author":[]
#     }
#     for p in page:
        
#         try:

#             driver.get("{}?term={}&filter=simsearch1.fha&page={}".format(site, k, p))
#             group['link'] += [i.get_attribute("href") for i in driver.find_elements_by_css_selector(".docsum-title")]
#             pass

#         except:

#             continue

#         pass

#     link = pandas.DataFrame({"link":group['link']})
#     link.to_csv(os.path.join(folder, "link.csv"), index=False)

#     def remove(x, what=""):

#         output = []
#         for i in x:

#             if(i==what):

#                 continue

#             else:

#                 output += [i]
#                 pass

#             pass
        
#         return(output)

#     for l in tqdm.tqdm(group['link'], total=len(group['link'])):

#         try:

#             driver.get(l)
#             pass

#         except:

#             group['title'] += [None]
#             group['abstract'] += [None]
#             group['tag'] += [None]
#             group['author'] += [None]            
#             continue

#         try:
            
#             title = driver.find_element_by_css_selector(".heading-title").text
#             pass

#         except:

#             title = None
#             pass

#         try:
            
#             abstract = driver.find_element_by_css_selector("#enc-abstract p").text
#             pass

#         except:

#             abstract = None
#             pass

#         try:

#             tag = driver.find_element_by_css_selector("#enc-abstract+ p").text.split(": ")[-1]
#             pass

#         except:

#             tag = None
#             pass

#         try:
            
#             author = ";".join(remove([i.text for i in driver.find_elements_by_css_selector(".full-name")], what=''))
#             pass

#         except:

#             author = None
#             pass

#         group['title'] += [title]
#         group['abstract'] += [abstract]
#         group['tag'] += [tag]
#         group['author'] += [author]
#         time.sleep(1)
#         pass

#     table = pandas.DataFrame(group)
#     table.to_csv(os.path.join(folder, "{}.csv".format(k)), index=False)
#     driver.close()
#     pass


# ##  
# ##  Merge all table together.
# path, folder = 'resource/csv', ['asthma', 'Covid-19', "influenza", "Myocardial Infarction", 'Stroke', "chest cavity"]
# group = []
# for f in folder:

#     p = os.path.join(path, f, '{}.csv'.format(f))
#     t = pandas.read_csv(p)
#     t['keyword'] = f
#     t = t.dropna(subset=['title'])
#     group += [t]
#     pass

# data = pandas.concat(group).reset_index(drop=True)
# data.to_csv(os.path.join(path, "data.csv"), index=False)
