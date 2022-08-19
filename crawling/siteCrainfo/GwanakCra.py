import requests
from bs4 import BeautifulSoup
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel

class Gwanak:
    print("Gwanak Start");

    def mainCra(cnt, numberCnt):
        numberCnt = numberCnt;
        cnt = cnt;
        url = 'https://www.gfac.or.kr/html/notify/notify11.html?page={}&sub=0'.format(cnt);
        response = requests.get(url);

        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser')

            link = soup.select('td.nor > a');
            number = soup.select('td.nor > a > span.cont1 > i');
            title = soup.select('td.nor > a > span.cont2 > em.cont2_2');
            registrationdate = soup.select('td.nor > a > span.cont2 > em.cont2_3 > i.cont2_3_2');
            
            linkCount = len(link) - 1;

            for i in range(len(link)):
                numberCnt +=1;
                if linkCount == i:
                    cnt += 1;
                    print("Gwanak Next Page : {}".format(cnt));
                    return Gwanak.mainCra(cnt, numberCnt);
                else:
                    if numberCnt == commonConstant_NAME.STOPCUOUNT:
                        break;
                     
                    firebase_con.updateModel(commonConstant_NAME.GWANAK_NAME,number[i].text,
                        datasModel.toJson(
                            "https://www.gfac.or.kr/html/notify/{}".format(link[i].attrs.get('href')),
                            number[i].text,
                            "",
                            title[i].text.strip(),
                            "",
                            registrationdate[i].text.strip(),
                            "관악문화재단",
                        )
                    );
        else : 
            print(response.status_code)
