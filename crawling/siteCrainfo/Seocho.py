import requests
from bs4 import BeautifulSoup
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel

class Seocho:
    def mainCra(cnt,numberCnt):
        requests.packages.urllib3.disable_warnings()
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

        numberCnt = numberCnt;
        cnt  = cnt; # 1
        url = 'http://www.seochocf.or.kr/site/main/archive/post/category/%EA%B3%B5%EC%A7%80%EC%82%AC%ED%95%AD?cp={}&sortDirection=DESC&catId=7&metaCode1=GENERAL'.format(cnt);
        response = requests.get(url);

        if response.status_code == 200:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser');

            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('tbody > tr > td.left > a.arc_tit');
            title = soup.select('tbody > tr > td.left > a.arc_tit');
            registrationdate = soup.select('tbody > tr > td:nth-child(4)');

            linkCount = len(link) - 1;
            print("linkCount : ", linkCount);

            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print("Next Page : {}".format(cnt));
                    return Seocho.mainCra(cnt, numberCnt);
                else:
                    print("title : ", title[i].text.strip());
                    print(link[i].attrs.get('href'))
                    # print("https://www.gbcf.or.kr/{}".format(link[i].attrs.get('href')));
                    print("registrationdate : ", registrationdate[i].text.strip());
                    
                    if numberCnt == commonConstant_NAME.STOPCUOUNT:
                        break;
                    
                    firebase_con.updateModel(commonConstant_NAME.SEOCHO_NAME,numberCnt,
                        datasModel.toJson(
                            link[i].attrs.get('href'),
                            numberCnt,
                            "",
                            title[i].text.strip(),
                            "",
                            registrationdate[i].text.strip(),
                            "서초문화재단",
                        )
                    );
        else : 
            print(response.status_code)