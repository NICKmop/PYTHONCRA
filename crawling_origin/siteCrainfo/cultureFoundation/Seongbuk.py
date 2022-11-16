import requests
from bs4 import BeautifulSoup
from common.common_fnc import fnCompareTitle
from common.common_fnc import fnChnagetype
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel

class Seongbuk:
    def mainCra(cnt,numberCnt):
        requests.packages.urllib3.disable_warnings()
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
        # cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.SEONGBUK_NAME);
        # maxCntNumber = max(cntNumber);

        url = 'https://www.sbculture.or.kr/culture/bbs/BMSR00021/list.do?pageIndex={}&menuNo=500049&fDate=&tDate=&searchCondition=3&searchKeyword='.format(cnt);
        response = requests.get(url);

        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser');

            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('tbody > tr > td.text-left > a');
            title = soup.select('tbody > tr > td.text-left > a');
            registrationdate = soup.select('tbody > tr > td:nth-child(5)');

            linkCount = len(link) - 1;

            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print("Seongbuk Next Page : {}".format(cnt));
                    return Seongbuk.mainCra(cnt, numberCnt);
                else:
                    if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT:
                        break;
                    # if(fnCompareTitle(commonConstant_NAME.SEONGBUK_NAME, title[i].text.strip()) == 1):
                    #         break;
                    # else:
                    #     maxCntNumber += 1;
                    changeText= str(registrationdate[i].text);
                    firebase_con.updateModel(commonConstant_NAME.SEONGBUK_NAME,numberCnt,
                        datasModel.toJson(
                            "https://www.sbculture.or.kr/culture/bbs/BMSR00021/{}".format(link[i].attrs.get('href')),
                            numberCnt,
                            "",
                            title[i].text.strip(),
                            "",
                            fnChnagetype(changeText.strip()),
                            "성북문화재단",
                        )
                    );
        else : 
            print(response.status_code)