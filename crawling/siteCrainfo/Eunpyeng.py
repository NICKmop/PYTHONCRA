import re
from bs4 import BeautifulSoup
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from selenium import webdriver
import common.common_fnc  as com



class Eunpyeng:
    def mainCra(cnt,numberCnt):
        url = 'https://www.efac.or.kr/sub06/sub01.php';
        soupData = com.pageconnect(cnt, url);
        link = soupData.select('.b-text-s > a');
        title = soupData.select('.board1');
        registrationdate = soupData.select('td:nth-child(5)');

        linkCount = len(link) - 1;
        for i in range(len(link)):
            numberCnt += 1;
            if linkCount == i:
                # javascript:pageNum('frm01','200');
                cnt += 10;
                print("Eunpyeng Next Page : {}".format(cnt));
                return Eunpyeng.mainCra(cnt, numberCnt),
            else:
                if numberCnt == commonConstant_NAME.STOPCUOUNT:
                    break;

            linkSp = re.sub(r'[^0-9]','',link[i].attrs.get('href'));
            firebase_con.updateModel( commonConstant_NAME.EUNPYENG_NAME,i,
                datasModel.toJson(
                    "https://www.efac.or.kr/sub06/sub01.php?type=view&uid={}".format(linkSp),
                    i,
                    "",
                    title[i].text.strip(),
                    "",
                    registrationdate[i + 1].text,
                    "은평문화재단"
                )
            )

            