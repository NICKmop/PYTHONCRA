import requests
from common.common_fnc import fnCompareTitle
from common.common_fnc import fnChnagetype
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Gwangzin_notice:
    def mainCra(cnt):
        cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.GWANGZIN_NAME);
        numberCnt = max(cntNumber);

        url = 'https://www.gwangjin.go.kr/portal/bbs/B0000001/list.do?menuNo=200190&pSiteId=portal&pageIndex={}'.format(cnt);
        response = requests.get(url);
        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser')
            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('.s > a');
            title = soup.select('.s > a');
            registrationdate = soup.select('.date');
            linkCount = len(link) - 1;

            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print(commonConstant_NAME.GWANGJIN_BOROUGH_NOTICE," Next Page : {}".format(cnt));
                    return Gwangzin_notice.mainCra(cnt);
                else:
                    # if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT:
                    #     break;
                    if(fnCompareTitle(commonConstant_NAME.GWANGZIN_NAME, title[i].text.strip()) == 1):
                        break;
                    changeText= str(registrationdate[i].text);
                    firebase_con.updateModel(commonConstant_NAME.GWANGZIN_NAME,numberCnt,
                        datasModel.toJson(
                            "https://www.gwangjin.go.kr{}".format(link[i].attrs.get('href')),
                            numberCnt,
                            "",
                            title[i].text.strip(),
                            "",
                            fnChnagetype(changeText.strip()),
                            "광진구청",
                        )
                    );
        else : 
            print(response.status_code)
            