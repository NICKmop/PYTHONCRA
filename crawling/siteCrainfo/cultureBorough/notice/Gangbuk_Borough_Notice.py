import requests
from common.common_fnc import fnChnagetype
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Gangbuk_notice:
    def mainCra(cnt):
        cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.GANGBUK_NAME);
        numberCnt = max(cntNumber);
        url = 'https://www.gangbuk.go.kr/www/boardList.do?page={}&boardSeq=41&key=285&category=&searchType=&searchKeyword=&searchFile=&subContents=&mpart=&part=&item='.format(cnt);
        response = requests.get(url);

        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser')
            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('.tb > .subject > a');
            title = soup.select('.tb > .subject > a');
            registrationdate = soup.select('td:nth-child(6)');
            
            linkCount = len(link);
            print("linkCount :  {}".format(linkCount));

            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print(commonConstant_NAME.GANGBUK_BOROUGH_NOTICE," Next Page : {}".format(cnt));
                    return Gangbuk_notice.mainCra(cnt);
                else:
                    if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT:
                        break;
                    changeText = str(registrationdate[i].text);
                    firebase_con.updateModel(commonConstant_NAME.GANGBUK_NAME,numberCnt,
                        datasModel.toJson(
                            "https://www.gangbuk.go.kr/www{}".format(link[i].attrs.get('href')),
                            numberCnt,
                            "",
                            title[i].text.strip(),
                            "",
                            registrationdate[i].text,
                            fnChnagetype(changeText.strip()),
                            "강북구청",
                        )
                    );
        else : 
            print(response.status_code)
            