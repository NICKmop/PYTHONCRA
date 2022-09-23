import requests
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Gangseo_notice:
    def mainCra(cnt,numberCnt):
        url = 'https://www.gangseo.seoul.kr/gs040101?curPage={}'.format(cnt);

        response = requests.get(url);
        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser')
            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('tr > td > a');
            title = soup.select('tr > td > a');
            registrationdate = soup.select('td:nth-child(4)');
            
            linkCount = len(link) - 1;

            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print(commonConstant_NAME.GANGSEO_BOROUGH_NOTICE," Next Page : {}".format(cnt));
                    return Gangseo_notice.mainCra(cnt, numberCnt);
                else:
                    if numberCnt == 20:
                        break;

                    # print(link[i].attrs.get('href'));
                    
                    firebase_con.updateModel(commonConstant_NAME.GANGSEO_BOROUGH_NOTICE,numberCnt,
                        datasModel.toJson(
                            "https://www.gangseo.seoul.kr{}".format(link[i].attrs.get('href')),
                            numberCnt,
                            "",
                            title[i].text.strip(),
                            "",
                            registrationdate[i].text,
                            "강서구_공지사항",
                        )
                    );
        else : 
            print(response.status_code)
            