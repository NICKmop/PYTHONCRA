import requests
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Songpa_notice:
    def mainCra(cnt):
        cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.SONGPA_NAME);
        numberCnt = max(cntNumber);

        url = 'https://www.songpa.go.kr/www/selectBbsNttList.do?bbsNo=92&&pageUnit=10&key=2775&searchAditfield4=&searchAditfield5=&viewBgnde=&searchAditfield1=&searchAditfield2=&pageIndex={}'.format(cnt);
        response = requests.get(url);
        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser')
            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('.p-subject > a');
            title = soup.select('.p-subject > a');
            registrationdate = soup.select('td:nth-child(4)');

            # print(registrationdate);
            linkCount = len(link) - 1;

            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print(commonConstant_NAME.SONGPA_BOROUGH_NOTICE," Next Page : {}".format(cnt));
                    return Songpa_notice.mainCra(cnt);
                else:
                    if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT:
                        break;

                    firebase_con.updateModel(commonConstant_NAME.SONGPA_NAME,numberCnt,
                        datasModel.toJson(
                            "https://www.songpa.go.kr/www{}".format(link[i].attrs.get('href').replace('.','',1)),
                            numberCnt,
                            "",
                            title[i].text.strip(),
                            "",
                            registrationdate[i].text,
                            "송파구청",
                        )
                    );
        else : 
            print(response.status_code)
            