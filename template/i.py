

##  The packages.
from selenium import webdriver
import pandas, os, time
import re


##  The goal.
'''
根據給定的 query 從 google 搜尋，將搜尋的網頁標題以及對應的網頁連結擷取出來，輸出成表格。
'''


##  The arguments.
platform = 'google'
keyword = 'dog'
page = 10
folder = "LOG/I"


##  Initial process.
os.makedirs(folder) if not os.path.isdir(folder) else None
option = webdriver.chrome.options.Options()
option.binary_location = "/usr/bin/google-chrome"
driver = webdriver.Chrome(options=option, executable_path='driver/chrome')
driver.get("https://www.google.com/search?q={}".format(keyword))
document = {
    "title" :[],
    "link" : []
}


##  Get title and link.
for p in range(1, page+1):

    document['title'] += [i.text for i in driver.find_elements_by_xpath('//h3[@class="LC20lb DKV0Md"]')]
    document['link'] += [i.get_attribute("href") for i in driver.find_elements_by_xpath('//div[@class="yuRUbf"]/a')]
    driver.find_elements_by_css_selector('.NVbCr+ span')[-1].click()
    time.sleep(1)
    pass


##  Convert to table.
table = {
    "data":pandas.DataFrame(document),
    "location":os.path.join(folder, "{} {} {}.csv".format(platform, keyword, re.sub(" ", "-", time.ctime())))
}
table['data'].to_csv(table['location'], index=False, encoding="utf_8_sig")
driver.close()




