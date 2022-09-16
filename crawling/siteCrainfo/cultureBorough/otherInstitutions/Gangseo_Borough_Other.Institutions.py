import requests
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Gangbuk_Institutions:
    def mainCra(cnt,numberCnt):
        url = '';
        response = requests.get(url);
        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser')
            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('tr');
            title = soup.select('tr > td > a');
            registrationdate = soup.select('td:nth-child(5)');
            
            # linkCount = len(link) - 1;
            print(soup);

        #     for i in range(len(link)):
        #         numberCnt += 1;
        #         if linkCount == i:
        #             cnt += 1;
        #             print(commonConstant_NAME.GANGBUK_BOROUGH_NOTICE," Next Page : {}".format(cnt));
        #             return Gangbuk_notice.mainCra(cnt, numberCnt);
        #         else:
        #             if numberCnt == commonConstant_NAME.STOPCUOUNT:
        #                 break;
                    
        #             firebase_con.updateModel(commonConstant_NAME.GANGBUK_BOROUGH_NOTICE,numberCnt,
        #                 datasModel.toJson(
        #                     "https://www.gangbuk.go.kr{}".format(link[i].attrs.get('href')),
        #                     numberCnt,
        #                     "",
        #                     title[i].text.strip(),
        #                     "",
        #                     registrationdate[i].text,
        #                     "강북구_공지사항",
        #                 )
        #             );
        # else : 
        #     print(response.status_code)
            