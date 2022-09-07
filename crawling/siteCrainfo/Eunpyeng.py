import re
from bs4 import BeautifulSoup
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from selenium import webdriver


def driver1(driver):
    driver.get('https://www.efac.or.kr/sub06/sub01.php');
    html = driver.page_source;
    return html;

def pageconnect():
    driver = webdriver.Chrome('D:/pythoncra/crawling/chromedriver.exe');
    driver.implicitly_wait(15);
    driver.get('https://www.efac.or.kr/sub06/sub01.php');

    soup = BeautifulSoup(driver1(driver), 'html.parser');
    return soup;

class Eunpyeng:
    def mainCra():
        soupData = pageconnect();
        link = soupData.select('.b-text-s > a');
        title = soupData.select('.board1');
        registrationdate = soupData.select('td:nth-child(5)');

        linkCount = len(link) - 1;
        for i in range(len(link)):
            # if linkCount == i:
            #     javascript:pageNum('frm01','200');
            #     cnt += 1;
            #     print("Eunpyeng Next Page : {}".format(cnt));
            #     return Eunpyeng.mainCra(cnt, numberCnt);
            # else:
            #     if numberCnt == commonConstant_NAME.STOPCUOUNT:
            #         break;
            # linkSp = re.sub(r'[^0-9]','',link[i].attrs.get('href'));
            # firebase_con.updateModel(commonConstant_NAME.EUNPYENG_NAME,
            #     datasModel.toJson(
            #         "https://www.efac.or.kr/sub06/sub01.php?type=view&uid={}".format(linkSp),
            #         numberCnt,
            #         ""
            #         title[i].text.strip(),
            #         "",
            #         registrationdate[i + 1].text,
            #         "은평문화재단"
            #     )
            # )

        #             firebase_con.updateModel(commonConstant_NAME.GANGBUK_NAME,numberCnt,
        #                 datasModel.toJson(
        #                     "https://www.gbcf.or.kr/{}".format(link[i].attrs.get('href')),
        #                     numberCnt,
        #                     "",
        #                     title[i].text.strip(),
        #                     "",
        #                     registrationdate[i].text,
        #                     "강북문화재단",
        #                 )
        #             );
        # else : 
        #     print(response.status_code)