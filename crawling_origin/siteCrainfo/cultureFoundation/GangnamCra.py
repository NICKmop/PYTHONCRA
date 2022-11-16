import requests
from bs4 import BeautifulSoup
from common.common_fnc import fnCompareTitle
from common.common_fnc import fnChnagetype
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel

class Gangnam:
    def mainCra(cnt,numberCnt):
        # cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.GANGNAM_NAME);
        # maxCntNumber = max(cntNumber);

        url = 'https://www.gangnam.go.kr/office/gfac/board/gfac_notice/list.do?mid=gfac_notice&pgno={}&keyfield=BDM_MAIN_TITLE&keyword='.format(cnt);
        response = requests.get(url);

        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser')
            # 타이틀 ,기관, 링크, 등록일, 번호
            title = soup.select('td.align-l');
            link = soup.select('td:nth-child(2) > a');
            registrationdate = soup.select('tr > td:nth-child(5)');

            linkCount = len(link) - 1;

            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print("Gangnam Next Page : {}".format(cnt));
                    return Gangnam.mainCra(cnt, numberCnt);
                else:
                    if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT + 1:
                        break;
                    # if(fnCompareTitle(commonConstant_NAME.GANGNAM_NAME, title[i].text.strip()) == 1):
                    #     break;
                    # else:
                    #     maxCntNumber += 1;
                    changeText= str(registrationdate[i].text);
                    
                    firebase_con.updateModel(commonConstant_NAME.GANGNAM_NAME,numberCnt,
                        datasModel.toJson(
                            "https://www.gangnam.go.kr/{}".format(link[i].attrs.get('href')),
                            numberCnt,
                            "",
                            title[i].text.strip(),
                            "",
                            fnChnagetype(changeText.strip()),
                            "강남문화재단",
                        )
                    );
        else : 
            print(response.status_code);