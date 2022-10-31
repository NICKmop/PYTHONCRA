import requests
from common.common_fnc import fnChnagetype
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Dongdaemun_notice:
    def mainCra(cnt):
        cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.DONGDAEMUN_NAME);
        numberCnt = max(cntNumber);

        url = 'https://www.ddm.go.kr/www/selectBbsNttList.do?key=198&bbsNo=38&searchCtgry=&searchCnd=all&searchKrwd=&integrDeptCode=&pageIndex={}'.format(cnt);
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
                    print(commonConstant_NAME.DONGDAEMUN_BOROUGH_NOTICE," Next Page : {}".format(cnt));
                    return Dongdaemun_notice.mainCra(cnt);
                else:
                    if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT:
                        break;

                    changeText = str(registrationdate[i].text);
                    firebase_con.updateModel(commonConstant_NAME.DONGDAEMUN_NAME,numberCnt,
                        datasModel.toJson(
                            "https://www.ddm.go.kr/www{}".format(link[i].attrs.get('href').replace(".","",1)),
                            numberCnt,
                            "",
                            title[i].text.strip(),
                            "",
                            fnChnagetype(changeText.strip()),
                            "동대문구청",
                        )
                    );
        else : 
            print(response.status_code)
            