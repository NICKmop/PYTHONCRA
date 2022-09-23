import requests
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Jungnang_notice:
    def mainCra(cnt,numberCnt):
        url = 'https://www.jungnang.go.kr/portal/bbs/list/B0000002.do?searchCnd=&searchWrd=&gubun=&delCode=0&useAt=&replyAt=&menuNo=200473&sdate=&edate=&deptId=&deptName=&popupYn=&dept=&dong=&option1=&viewType=&searchCnd2=&pageIndex={}'.format(cnt);
        response = requests.get(url);
        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser')
            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('.tit > a');
            title = soup.select('.tit > a');
            registrationdate = soup.select('td:nth-child(5)');

            # print(registrationdate);
            linkCount = len(link) - 1;

            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print(commonConstant_NAME.JUNGNANG_BOROUGH_NOTICE," Next Page : {}".format(cnt));
                    return Jungnang_notice.mainCra(cnt, numberCnt);
                else:
                    if numberCnt == commonConstant_NAME.STOPCUOUNT:
                        break;

                    # print(title[i].text.strip()); 
                    # print(registrationdate);
                    
                    firebase_con.selectModel(commonConstant_NAME.SEOCHO_BOROUGH_NOTICE);

                    firebase_con.updateModel(commonConstant_NAME.JUNGNANG_BOROUGH_NOTICE,numberCnt,
                        datasModel.toJson(
                            "https://www.jungnang.go.kr{}".format(link[i].attrs.get('href')),
                            numberCnt,
                            "",
                            title[i].text.strip(),
                            "",
                            registrationdate[i].text,
                            "중랑구_공지사항",
                        )
                    );
        else : 
            print(response.status_code)
            