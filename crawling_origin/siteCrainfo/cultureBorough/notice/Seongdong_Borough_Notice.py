import requests
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Seongdong_notice:
    def mainCra(cnt):
        cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.SEONGDONG_NAME);
        numberCnt = max(cntNumber);

        url = 'https://www.sd.go.kr/main/selectBbsNttList.do?bbsNo=183&&pageUnit=10&key=1472&pageIndex={}'.format(cnt);
        response = requests.get(url);
        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser')
            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('.p-subject > a');
            title = soup.select('.p-subject > a');
            registrationdate = soup.select('td:nth-child(3)');

            # print(registrationdate);
            linkCount = len(link) - 1;

            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print(commonConstant_NAME.SEONGDONG_BOROUGH_NOTICE," Next Page : {}".format(cnt));
                    return Seongdong_notice.mainCra(cnt);
                else:
                    if numberCnt == commonConstant_NAME.SEOUL_STOP_COUNT_FOUR:
                        break;
                    # if(fnCompareTitle(commonConstant_NAME.SEONGDONG_NAME, title[i].text.strip()) == 1):
                    #     break;

                    if('NEW' in title[i].text.strip()):
                        replaceString = title[i].text.strip().replace('NEW', '').strip();
                    else:
                        replaceString = title[i].text.strip();

                    changeText= str(registrationdate[i].text.replace('.', '-'));

                    firebase_con.updateModel(commonConstant_NAME.SEONGDONG_NAME,numberCnt,
                        datasModel.toJson(
                            "https://www.sd.go.kr/main{}".format(link[i].attrs.get('href').replace('.','',1)),
                            numberCnt,
                            "",
                            replaceString,
                            "",
                            fnChnagetype(changeText.strip()),
                            "성동구청",
                        )
                    );
        else : 
            print(response.status_code)
            