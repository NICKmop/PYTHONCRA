import requests
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Junggu_notice:
    def mainCra(cnt):
        cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.JUNGGU_NAME);
        numberCnt = max(cntNumber);

        url = 'https://www.junggu.seoul.kr/content.do?cmsid=14231&sf_dept=&searchValue=&searchField=all&page={}'.format(cnt);
        response = requests.get(url);
        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser')
            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('.title > a');
            title = soup.select('.title > a');
            registrationdate = soup.select('td:nth-child(5)');

            linkCount = len(link) - 1;

            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print(commonConstant_NAME.JUNGGU_BOROUGH_NOTICE," Next Page : {}".format(cnt));
                    return Junggu_notice.mainCra(cnt);
                else:
                    if numberCnt == commonConstant_NAME.STOPCUOUNT:
                        break;
                    
                    # print("link Data : {}".format(link[i].attrs.get('href')));

                    firebase_con.updateModel(commonConstant_NAME.JUNGGU_NAME,numberCnt,
                        datasModel.toJson(
                            "https://www.junggu.seoul.kr{}".format(link[i].attrs.get('href')),
                            numberCnt,
                            "",
                            title[i].text.strip(),
                            "",
                            registrationdate[i].text,
                            "중구_공지사항",
                        )
                    );
        else : 
            print(response.status_code)
            