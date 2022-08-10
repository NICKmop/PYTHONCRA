import requests
from bs4 import BeautifulSoup
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel

class craMain:
    def mainCra(cnt):
        cnt = cnt;
        url = 'https://www.gfac.or.kr/html/notify/notify11.html?page={}&sub=0'.format(cnt);
        response = requests.get(url);

        if response.status_code == 200:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser')

            link = soup.select('td.nor > a');
            number = soup.select('td.nor > a > span.cont1 > i');
            result = soup.select('td.nor > a > span.cont2 > em > i.cont2_pc');
            title = soup.select('td.nor > a > span.cont2 > em.cont2_2');
            apperiod = soup.select('td.nor > a > span.cont2 > em.cont2_3 > i.cont2_3_1');
            registrationdate = soup.select('td.nor > a > span.cont2 > em.cont2_3 > i.cont2_3_2');
            
            linkCount = len(link) - 1;

            for i in range(len(link)):
                if linkCount == i:
                    cnt += 1;
                    print("Next Page : {}".format(cnt));
                    return craMain.mainCra(cnt);
                else:
                    firebase_con.updateModel(commonConstant_NAME.GWANAK_NAME,number[i].text,
                        datasModel.toJson(
                            "https://www.gfac.or.kr/html/notify/{}".format(link[i].attrs.get('href')),
                            number[i].text,
                            result[i].text,
                            title[i].text.strip(),
                            apperiod[i].text.strip(),
                            registrationdate[i].text.strip(),
                            "관악문화재단",
                        )
                    );
        else : 
            print(response.status_code)
