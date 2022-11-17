from bs4 import BeautifulSoup
from selenium import webdriver
import time, logging
from  datetime import date
from firebase_admin import firestore
from common.common_constant import commonConstant_NAME
from dbbox.firebases import firebase_con
from datetime import datetime

def loggingdata(data):
    today = date.today();

    logger = logging.getLogger();
    logger.setLevel(logging.INFO);
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    stream_handler = logging.StreamHandler();
    stream_handler.setFormatter(formatter);
    logger.addHandler(stream_handler);

    file_handler = logging.FileHandler('/Users/yeon/StudioProjects/pythoncra/crawling/siteLog/{}.log'.format(today.strftime('%Y-%m-%d')));
    file_handler.setFormatter(formatter);
    logger.addHandler(file_handler);

    logger.info(data);

def pageReload(driver, pageNumber, script):
    time.sleep(2);
    driver.execute_script(script)
def driver1(driver, pageNumber, url, script):
    driver.get(url);
    pageReload(driver,pageNumber, script);
    html = driver.page_source;
    return html;

def fnChnagetype(text):
    dt_obj = datetime.strptime(text,'%Y-%m-%d')
    return dt_obj;
    
def pageconnect(pageNumber, url, script):
    if pageNumber is None:
        pageNumber = 0;
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    browser = webdriver.Chrome('/Users/yeon/StudioProjects/pythoncra/crawling/chromedriver', options=options);
    browser.implicitly_wait(15);
    browser.get(url);

    soup = BeautifulSoup(driver1(browser,pageNumber, url, script), 'html.parser');
    return soup;

def fnCompareTitle(name, title):
    # changeDate = fnChnagetype(date);
    dupltitleList = [];
    cntTitle = firebase_con.selectModelValueNumber(name);
    # cntData = firebase_con.selectModelValueNumber(name)[1];

    for i in cntTitle:
        if(i == title):
            print("{} Firebase title : {}".format(name,i));
            print("{} webCra title : {}".format(name,title));
            dupltitleList.append(title);
            return 1;

    # for i in zip(cntTitle , cntData):
    #     print(i[0]);
    #     if(i[0] == title):
        #     print("{} Firebase title : {}".format(name,i));
        #     print("{} webCra title : {}".format(name,title));
        #     dupltitleList.append(title);
        #     return 1;


  