

##  The packages.
from selenium import webdriver
import pandas, os, time
import re
import time


##  The goal.
'''
根據給定的 query 從 91porn 成人網站搜尋，將搜尋的的影片標題以及對應的影片連結擷取出來，輸出成表格。
'''


##  The arguments.
plotform = '91porn'
keyword = '5P'
page = 150
folder = "LOG/II"


##  Initial process.
os.makedirs(folder) if not os.path.isdir(folder) else None
option = webdriver.chrome.options.Options()
option.binary_location = "/usr/bin/google-chrome"
driver = webdriver.Chrome(options=option, executable_path='driver/chrome')
document = {
    'title':[],
    "link":[]
}


##  Get title and link condition the keyword.
for p in range(1, page+1):

    driver.get("https://91porn.com/v.php?category=rf&viewtype=basic&page={}".format(p))
    title = [i.text for i in driver.find_elements_by_xpath('//span[@class="video-title title-truncate m-t-5"]')] 
    link = [i.get_attribute('href') for i in driver.find_elements_by_xpath('//div[@class="well well-sm videos-text-align"]/a')]
    pass

    if(keyword):

        condition = [keyword in i for i in title]
        document['title'] += [t for t, c in zip(title, condition) if c == True]
        document['link'] += [l for l, c in zip(link, condition) if c == True]
        pass

    else:
        
        document['title'] += title
        document['link'] += link
        pass

    time.sleep(1)
    pass


##  Convert to table.
table = {
    "data":pandas.DataFrame(document),
    "location":os.path.join(folder, "{} {} {}.csv".format(plotform, keyword, re.sub(" ", "-", time.ctime())))
}
table['data'].to_csv(table['location'], index=False, encoding="utf_8_sig")
driver.close()


