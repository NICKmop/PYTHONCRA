import requests
from bs4 import BeautifulSoup
from common.common_fnc import fnChnagetype
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel

class Gangnam:
    def mainCra(cnt,numberCnt):
        numberCnt = numberCnt;
        cnt  = cnt;
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
                    if numberCnt == commonConstant_NAME.STOPCUOUNT:
                        break;
                    changeText= str(registrationdate[i].text);
                    
                    firebase_con.updateModel(commonConstant_NAME.GANGNAM_NAME,i,
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