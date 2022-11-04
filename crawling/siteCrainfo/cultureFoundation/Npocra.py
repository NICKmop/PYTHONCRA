import requests
from bs4 import BeautifulSoup
from common.common_fnc import fnChnagetype
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel

class Npocra:
    def mainCra(cnt,numberCnt):
        requests.packages.urllib3.disable_warnings()
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
        url = 'https://www.snpo.kr/bbs/board.php?bo_table=bbs_npo&amp;page={}'.format(cnt);
        
        response = requests.get(url);
        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser');

            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('.title');
            title = soup.select('.title');
            registrationdate = soup.select('.date');
            
            linkCount = len(link) ;

            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print("Npocra Next Page : {}".format(cnt));
                    return Npocra.mainCra(cnt, numberCnt);
                else:
                    if numberCnt == commonConstant_NAME.SEOUL_STOP_COUNT_ONE:
                        break;
                
                changeText= str(registrationdate[i].text.replace('.','-'));
                if(changeText != '날짜'):
                    firebase_con.updateModel(commonConstant_NAME.SEOUL_NAME,numberCnt,
                        datasModel.toJson(
                            link[i].attrs.get('href'),
                            numberCnt,
                            "",
                            title[i].text.strip(),
                            "",
                            fnChnagetype(changeText.strip()),
                            "서울NPO지원센터",
                        )
                    );
                else:
                    numberCnt = 0;
        else : 
            print(response.status_code)