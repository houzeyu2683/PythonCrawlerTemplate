

##
##  The packages.
from selenium import webdriver
import pandas, os, time, tqdm
import re
import time


##
##  Introduce the script.
'''
Define the search number, get the title and link of PTT.
'''


##
##  The arguments.
platform = "ptt"
board = 'stock'
site = "https://www.ptt.cc/bbs/Stock/index.html"
number = 20
folder = "LOG/III"
confirmation = False


##
##  Initial process.
os.makedirs(folder) if not os.path.isdir(folder) else None
option = webdriver.chrome.options.Options()
option.binary_location = "/usr/bin/google-chrome"
driver = webdriver.Chrome(options=option, executable_path='driver/chrome')
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
    "comment":[],
    "push":[],
    "message":[],
    "boo":[]
}


##
##  Get title and link.
for n in range(number):
    
    document['title'] += [i.text for i in driver.find_elements_by_css_selector('.title a')]
    document['link'] += [i.get_attribute('href') for i in driver.find_elements_by_xpath("//div[@class='title']/a")]
    driver.find_element_by_css_selector('.wide:nth-child(2) , .f2').click()
    time.sleep(1)
    pass


##
##  Get other information base on link.
for l in tqdm.tqdm(document['link']):

    driver.get(l)
    pass

    try:

        document['author'] += [driver.find_element_by_css_selector(".article-metaline:nth-child(1) .article-meta-value").text]
        document['date'] += [driver.find_element_by_css_selector('.article-metaline+ .article-metaline .article-meta-value').text]
        document['content'] += [driver.find_element_by_css_selector('#main-content').text]
        document['comment'] += ['\n\n'.join([i.text for i in driver.find_elements_by_css_selector('.push')])]
        style = [re.sub(" ", "", i.text) for i in driver.find_elements_by_css_selector('.push-tag')]
        document['push'] += [sum(['推' in i for i in style])]
        document['message'] += [sum(['→' in i for i in style])]
        document['boo'] += [sum(['噓' in i for i in style])]
        pass

    except:

        document['author'] += [None]
        document['date'] += [None]
        document['content'] += [None]
        document['comment'] += [None]
        document['push'] += [None]
        document['message'] += [None]
        document['boo'] += [None]
        pass

    time.sleep(1)
    pass

driver.close()


##
##  Convert to table.
table = {
    "data":pandas.DataFrame(document),
    "location":os.path.join(folder, "{} {} {}.csv".format(platform, board, re.sub(" ", "-", time.ctime())))
}
selection = ['platform', 'board', 'link', 'title', 'author', 'date', 'content', 'comment']
table['data'][selection].to_csv(table['location'], index=False, encoding="utf_8_sig")
