

##
##  The packages.
from selenium import webdriver
import pandas, os, time, tqdm
import re
import time


##
##  Introduce the script.
'''
Define the scroll number, get the title and link of DCARD.
'''


##
##  The arguments.
platform = 'dcard'
board = 'mood'
site = "https://www.dcard.tw/f/mood"
number = 20
folder = "LOG/IV"
confirmation = False


##
##  Initial process.
os.makedirs(folder) if not os.path.isdir(folder) else None
option = webdriver.chrome.options.Options()
option.binary_location = "/usr/bin/google-chrome"
driver = webdriver.Chrome(options=option, executable_path='driver/chrome')
driver.set_window_size(1920/5, 1080/2)
driver.get(site)
driver.find_element_by_css_selector(".btn-big").click() if confirmation else None
document = {
    "platform":platform,
    "board":board,
    "title":[],
    "link":[],
    "author":[],
    "date":[],
    "content":[],
    "comment":[]
}

##  Relax a second.
time.sleep(1)


##
##  Get title and link.
for n in range(1, number+1):
    
    document['title'] += [re.sub("#", "", i.text) for i in driver.find_elements_by_css_selector('.cUGTXH')]
    document['link'] += [i.get_attribute('href') for i in driver.find_elements_by_xpath('//h2[@class="tgn9uw-2 jWUdzO"]/a')]
    driver.execute_script("var q=document.documentElement.scrollTop={}".format(n * 10000))
    time.sleep(1)
    pass


##
##  Get other information base on link.
for l in tqdm.tqdm(document['link']):

    driver.get(l)
    time.sleep(5)
    try:

        document['date'] += [driver.find_element_by_css_selector(".boQZzA+ .boQZzA").text]
        document['author'] += [driver.find_element_by_xpath("//div[@class='s3d701-2 kBmYXB']").text]
        document['content'] += [driver.find_element_by_xpath("//div[@class='phqjxq-0 fQNVmg']").text]
        document['comment'] += ['\n\n'.join([i.text for i in driver.find_elements_by_xpath("//div[@class='sc-71lpws-1 hcbtbx-0 kxmuAN cCOVWi']")])]
        pass

    except:

        document['date'] += [None]
        document['author'] += [None]
        document['content'] += [None]
        document['comment'] += [None]
        pass

    pass

driver.close()


##
##  Convert to table.
table = {
    "data":pandas.DataFrame(document),
    "location":os.path.join(folder, "{} {} {}.csv".format(platform, board, re.sub(" ", "-", time.ctime())))
}
table['data'].to_csv(table['location'], index=False, encoding="utf_8_sig")
pass

 