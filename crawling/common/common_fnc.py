import os
from bs4 import BeautifulSoup
from selenium import webdriver
import time, logging
from  datetime import date
from firebase_admin import firestore
from common.common_constant import commonConstant_NAME
from dbbox.firebases import firebase_con
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
from requests_toolbelt import MultipartEncoder

current_working_directory = os.getcwd();
ubuntuPath = '/home/ubuntu/Stproject/pythoncra/crawling';

def loggingdata(data):
    try:
        today = date.today();

        logger = logging.getLogger();
        logger.setLevel(logging.INFO);
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        stream_handler = logging.StreamHandler();
        stream_handler.setFormatter(formatter);
        logger.addHandler(stream_handler);

        file_handler = logging.FileHandler(current_working_directory+'/siteLog/{}.log'.format(today.strftime('%Y-%m-%d')));
        # file_handler = logging.FileHandler(ubuntuPath+'/siteLog/{}.log'.format(today.strftime('%Y-%m-%d')));

        file_handler.setFormatter(formatter);
        logger.addHandler(file_handler);
        logger.info(data);
        
    except Exception as header:
        print("pass : {}".format(header));

def pageconnectLoadUrl(url):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(current_working_directory+'/chromedriver', options=options);
    # browser = webdriver.Chrome(executable_path=ubuntuPath+'/chromedriver' , options=options);
    browser.implicitly_wait(15);
    
    browser.get(url);
    
    time.sleep(3);
    
    html = browser.page_source;
    return html;

def pageClickEvent(url):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(current_working_directory+'/chromedriver', options=options);
    # browser = webdriver.Chrome(executable_path=ubuntuPath+'/chromedriver', options=options);
    browser.implicitly_wait(15);
    browser.get(url);

def pageReload(driver, pageNumber, script):
    driver.implicitly_wait(15)
    driver.execute_script(script)
    
def driver1(driver, pageNumber, url, script):
    driver.implicitly_wait(15);
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
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(current_working_directory+'/chromedriver', options=options);
    # browser = webdriver.Chrome(executable_path=ubuntuPath+'/chromedriver', chrome_options=options);
    browser.implicitly_wait(15);
    browser.get(url);

    time.sleep(3);

    soup = BeautifulSoup(driver1(browser,pageNumber, url, script), 'html.parser');
    browser.quit();
    return soup;

def fnCompareTitle(name, title):
    # changeDate = fnChnagetype(date);
    dupltitleList = [];
    cntTitle = firebase_con.selectModelValueNumber(name);
    # cntData = firebase_con.selectModelValueNumber(name)[1];

    for i in cntTitle:
        # print("not same data : {}".format(i));
        if(i == title):
            print("{} Firebase title : {}".format(name,i));
            print("{} webCra title : {}".format(name,title));
            loggingdata(name);
            dupltitleList.append(title);
            return 1;

    # for i in zip(cntTitle , cntData):
    #     print(i[0]);
    #     if(i[0] == title):
        #     print("{} Firebase title : {}".format(name,i));
        #     print("{} webCra title : {}".format(name,title));
        #     dupltitleList.append(title);
        #     return 1;


  