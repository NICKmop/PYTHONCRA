import requests
from bs4 import BeautifulSoup
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel

class Jongro:
    def mainCra(cnt,numberCnt):
        requests.packages.urllib3.disable_warnings()
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
        cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.JONGRO_NAME);
        maxCntNumber = max(cntNumber);
        
        url = 'https://www.jfac.or.kr/site/main/archive/post/category/%EA%B3%B5%EC%A7%80%EC%82%AC%ED%95%AD?cp={}&catId=25'.format(cnt);
        response = requests.get(url);

        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser');

            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('tbody > tr > td.align-left > a');
            title = soup.select('tbody > tr > td.align-left > a');
            registrationdate = soup.select('tbody > tr > td:nth-child(5)');

            linkCount = len(link) - 1;

            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print("Jongro Next Page : {}".format(cnt));
                    return Jongro.mainCra(cnt, numberCnt);
                else:
                    # if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT:
                    #     break; 
                    if(fnCompareTitle(commonConstant_NAME.JONGRO_NAME, title[i].text.strip()) == 1):
                        break;
                    else:
                        maxCntNumber += 1;
                        changeText= str(registrationdate[i].text.strip());
                        firebase_con.updateModel(commonConstant_NAME.JONGRO_NAME,maxCntNumber,
                            datasModel.toJson(
                                "https://www.jfac.or.kr{}".format(link[i].attrs.get('href')),
                                maxCntNumber,
                                "",
                                title[i].text.strip(),
                                "",
                                fnChnagetype(changeText),
                                "종로문화재단",
                            )
                        );
        else : 
            print(response.status_code)