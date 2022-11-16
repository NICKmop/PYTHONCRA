import requests
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup


class Dobong_notice:
    def mainCra(cnt):
        cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.DOBONG_NAME);
        numberCnt = max(cntNumber);

        url = 'https://www.dobong.go.kr/bbs.asp?intPage={}&code=10004124&'.format(cnt);
        response = requests.get(url);

        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser')
            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('.al > a');
            title = soup.select('.al > a');
            registrationdate = soup.select('td:nth-child(3)');

            linkCount = len(link) - 1;
        
            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print(commonConstant_NAME.DOBONG_BOROUGH_NOTICE," Next Page : {}".format(cnt));
                    return Dobong_notice.mainCra(cnt);
                else:
                    # if numberCnt == commonConstant_NAME.SEOUL_STOP_COUNT_FOUR:
                    #     break;
                    
                    if(fnCompareTitle(commonConstant_NAME.DOBONG_NAME, title[i].text.strip()) == 1):
                        break;
                    
                    linkrep = link[i].attrs.get('href').replace("'", "");

                    changeText = str(registrationdate[i].text.replace('.','-'));
                    firebase_con.updateModel(commonConstant_NAME.DOBONG_NAME,numberCnt,
                        datasModel.toJson(
                            "https://www.dobong.go.kr{}".format(linkrep.replace(".","",1)),
                            numberCnt,
                            "",
                            title[i].text.strip(),
                            "",
                            fnChnagetype(changeText.strip()),
                            "도봉구청",
                        )
                    );
        else : 
            print(response.status_code)
            