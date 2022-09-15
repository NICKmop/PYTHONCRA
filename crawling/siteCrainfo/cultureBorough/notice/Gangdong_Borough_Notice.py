import requests
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup


class Gangdong_notice:
    def mainCra(cnt,numberCnt):
        url = 'https://www.gangdong.go.kr/web/newportal/bbs/b_068';
        response = requests.get(url);

        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser')
            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('tr > .tlt > a');
            title = soup.select('tr > .tlt > a');
            registrationdate = soup.select('td:nth-child(4)');

            linkCount = len(link) - 1;
        
            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print(commonConstant_NAME.GANGDONG_BOROUGH_NOTICE," Next Page : {}".format(cnt));
                    return Gangdong_notice.mainCra(cnt, numberCnt);
                else:
                    if numberCnt == commonConstant_NAME.STOPCUOUNT:
                        break;
                    
                    firebase_con.updateModel(commonConstant_NAME.GANGDONG_BOROUGH_NOTICE,numberCnt,
                        datasModel.toJson(
                            "https://www.gangdong.go.kr{}".format(link[i].attrs.get('href')),
                            numberCnt,
                            "",
                            title[i].text.strip(),
                            "",
                            registrationdate[i].text,
                            "강동구_공지사항",
                        )
                    );
        else : 
            print(response.status_code)
            