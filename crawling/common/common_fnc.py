from bs4 import BeautifulSoup
from selenium import webdriver

def pageReload(driver, pageNumber):
    driver.execute_script("javascript:pageNum('frm01','{}')".format(pageNumber))

def driver1(driver, pageNumber, url):
    driver.get(url);
    pageReload(driver,pageNumber);
    html = driver.page_source;
    return html;

def pageconnect(pageNumber, url):
    if pageNumber is None:
        pageNumber = 0;
        
    driver = webdriver.Chrome('D:/pythoncra/crawling/chromedriver.exe');
    driver.implicitly_wait(15);
    driver.get(url);

    soup = BeautifulSoup(driver1(driver,pageNumber, url), 'html.parser');
    return soup;