import requests
from bs4 import BeautifulSoup
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel

class Dongjak:
    def mainCra(cnt,numberCnt):
        requests.packages.urllib3.disable_warnings()
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

        numberCnt = numberCnt;
        cnt  = cnt; # 1
        url = 'https://www.idfac.or.kr/bbs/board.php?bo_table=notice&page={}'.format(cnt);
        response = requests.get(url);

        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser');

            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('tbody > tr > td.title > div > a');
            title = soup.select('tbody > tr > td.title > div > a');
            registrationdate = soup.select('tbody > tr > td.date');

            linkCount = len(link) - 1;

            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print("Dongjak Next Page : {}".format(cnt));
                    return Dongjak.mainCra(cnt, numberCnt);
                else:
                    if numberCnt == commonConstant_NAME.STOPCUOUNT:
                        break;
                    
                    firebase_con.updateModel(commonConstant_NAME.DONGJAK_NAME,numberCnt,
                        datasModel.toJson(
                            link[i].attrs.get('href'),
                            numberCnt,
                            "",
                            title[i].text.strip(),
                            "",
                            registrationdate[i].text,
                            "동작문화재단",
                        )
                    );
        else : 
            print(response.status_code)