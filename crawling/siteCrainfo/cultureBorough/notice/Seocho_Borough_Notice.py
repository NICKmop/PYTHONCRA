import requests
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Seocho_notice:
    def mainCra(cnt):
        cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.SEOCHO_NAME);
        numberCnt = max(cntNumber);

        url = 'https://www.seocho.go.kr/site/seocho/ex/bbs/List.do?pageIndex={}&cbIdx=57&searchMedia=&bcIdx=0&searchCondition=subCont&searchKeyword='.format(cnt);
        response = requests.get(url);
        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser')
            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('.title > a');
            title = soup.select('.title > a');
            registrationdate = soup.select('td:nth-child(4)');

            # print(registrationdate);
            linkCount = len(link) - 1;

            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print(commonConstant_NAME.SEOCHO_BOROUGH_NOTICE," Next Page : {}".format(cnt));
                    return Seocho_notice.mainCra(cnt);
                else:
                    if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT:
                        break;

                    # print(link[i].attrs.get('href'));
                    
                    firebase_con.updateModel(commonConstant_NAME.SEOCHO_NAME,numberCnt,
                        datasModel.toJson(
                            "https://www.seocho.go.kr{}".format(link[i].attrs.get('href')),
                            numberCnt,
                            "",
                            title[i].text.strip(),
                            "",
                            registrationdate[i].text,
                            "서초구청",
                        )
                    );
        else : 
            print(response.status_code)
            