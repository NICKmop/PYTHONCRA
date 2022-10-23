import requests
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Youngsan_notice:
    def mainCra(cnt,numberCnt):
        url = 'https://www.yongsan.go.kr/portal/bbs/B0000041/list.do?menuNo=200228&pageIndex={}'.format(cnt);
        response = requests.get(url);
        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser')
            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('.title > a');
            title = soup.select('.title > a');
            registrationdate = soup.select('td:nth-child(5)');

            # print(registrationdate);
            linkCount = len(link) - 1;

            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print(commonConstant_NAME.YOUNGSAN_BOROUGH_NOTICE," Next Page : {}".format(cnt));
                    return Youngsan_notice.mainCra(cnt, numberCnt);
                else:
                    if numberCnt == commonConstant_NAME.STOPCUOUNT:
                        break;

                    firebase_con.updateModel(commonConstant_NAME.YOUNGSAN_NAME,numberCnt,
                        datasModel.toJson(
                            "https://www.yongsan.go.kr{}".format(link[i].attrs.get('href')),
                            numberCnt,
                            "",
                            title[i].text.strip(),
                            "",
                            registrationdate[i].text,
                            "용산구청",
                        )
                    );
        else : 
            print(response.status_code)
            