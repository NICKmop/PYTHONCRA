from bs4 import BeautifulSoup
from selenium import webdriver
import time

def pageReload(driver, pageNumber, script):
    time.sleep(2);
    driver.execute_script(script)
    # javascript:pagingUtil.pageSubmit('2') -> 금천
def driver1(driver, pageNumber, url, script):
    driver.get(url);
    pageReload(driver,pageNumber, script);
    html = driver.page_source;
    return html;

def pageconnect(pageNumber, url, script):
    if pageNumber is None:
        pageNumber = 0;
        
    driver = webdriver.Chrome('D:/pythoncra/crawling/chromedriver.exe');
    driver.implicitly_wait(15);
    driver.get(url);

    soup = BeautifulSoup(driver1(driver,pageNumber, url, script), 'html.parser');
    return soup;