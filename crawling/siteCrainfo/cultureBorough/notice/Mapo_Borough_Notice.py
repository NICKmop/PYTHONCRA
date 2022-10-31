import requests
from common.common_fnc import fnChnagetype
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Mapo_notice:
    def mainCra(cnt):
        cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.MAPO_NAME);
        numberCnt = max(cntNumber);

        url = 'https://www.mapo.go.kr/site/main/board/notice/list?cp={}&sortOrder=BA_REGDATE&sortDirection=DESC&listType=list&bcId=notice&baNotice=false&baCommSelec=false&baOpenDay=false&baUse=true'.format(cnt);
        response = requests.get(url);
        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser')
            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('.val_m > a');
            title = soup.select('.val_m > a');
            registrationdate = soup.select('td:nth-child(5)');

            # print(registrationdate);
            linkCount = len(link) - 1;

            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print(commonConstant_NAME.MAPO_BOROUGH_NOTICE," Next Page : {}".format(cnt));
                    return Mapo_notice.mainCra(cnt);
                else:
                    if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT:
                        break;
                    
                    changeText = str(registrationdate[i].text.replace('.','-'));
                    firebase_con.updateModel(commonConstant_NAME.MAPO_NAME,numberCnt,
                        datasModel.toJson(
                            "https://www.mapo.go.kr{}".format(link[i].attrs.get('href').replace('.','',1)),
                            numberCnt,
                            "",
                            title[i].text.strip(),
                            "",
                            fnChnagetype(changeText.strip()),
                            "마포구청",
                        )
                    );
        else : 
            print(response.status_code)
            