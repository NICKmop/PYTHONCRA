import requests
from bs4 import BeautifulSoup
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel

class Jongro:
    def mainCra(cnt,numberCnt):
        print("Jongro Start");
        requests.packages.urllib3.disable_warnings()
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

        numberCnt = numberCnt;
        cnt  = cnt; # 1
        url = 'https://www.jfac.or.kr/site/main/archive/post/category/%EA%B3%B5%EC%A7%80%EC%82%AC%ED%95%AD?cp={}&catId=25'.format(cnt);
        response = requests.get(url);

        if response.status_code == 200:
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
                    if numberCnt == commonConstant_NAME.STOPCUOUNT:
                        break; 
                    
                    firebase_con.updateModel(commonConstant_NAME.JONGRO_NAME,numberCnt,
                        datasModel.toJson(
                            "https://www.jfac.or.kr/{}".format(link[i].attrs.get('href')),
                            numberCnt,
                            "",
                            title[i].text.strip(),
                            "",
                            registrationdate[i].text.strip(),
                            "종로문화재단",
                        )
                    );
        else : 
            print(response.status_code)