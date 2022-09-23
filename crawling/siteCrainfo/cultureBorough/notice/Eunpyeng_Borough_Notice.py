import requests
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Eunpyeng_notice:
    def mainCra(cnt,numberCnt):
        url = 'https://www.ep.go.kr/www/selectBbsNttList.do?key=744&bbsNo=42&searchCtgry=&searchCnd=all&searchKrwd=&integrDeptCode=&pageIndex={}'.format(cnt);
        response = requests.get(url);
        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser')
            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('.p-subject > a');
            title = soup.select('.p-subject > a');
            registrationdate = soup.select('td:nth-child(4)');

            # print(registrationdate);
            linkCount = len(link) - 1;

            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print(commonConstant_NAME.EUNPYENG_BOROUGH_NOTICE," Next Page : {}".format(cnt));
                    return Eunpyeng_notice.mainCra(cnt, numberCnt);
                else:
                    if numberCnt == commonConstant_NAME.STOPCUOUNT:
                        break;

                    # print(title[i].text.strip());
                    print(registrationdate);
                    
                    # firebase_con.selectModel(commonConstant_NAME.SEOCHO_BOROUGH_NOTICE);

                    firebase_con.updateModel(commonConstant_NAME.EUNPYENG_BOROUGH_NOTICE,numberCnt,
                        datasModel.toJson(
                            "https://www.ep.go.kr/www{}".format(link[i].attrs.get('href').removeprefix('.')),
                            numberCnt,
                            "",
                            title[i].text.strip(),
                            "",
                            registrationdate[i].text,
                            "은평구_공지사항",
                        )
                    );
        else : 
            print(response.status_code)
            