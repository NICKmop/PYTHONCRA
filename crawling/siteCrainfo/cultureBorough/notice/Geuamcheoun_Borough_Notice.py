import requests
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Geuamcheoun_notice:
    def mainCra(cnt,numberCnt):
        url = 'https://www.geumcheon.go.kr/portal/selectBbsNttList.do?key=293&id=&bbsNo=4&searchCtgry=&pageUnit=10&searchCnd=all&searchKrwd=&integrDeptCode=&searchDeptCode=&pageIndex={}'.format(cnt);
        response = requests.get(url);
        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser')
            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('.p-subject > a');
            title = soup.select('.p-subject > a');
            registrationdate = soup.select('td:nth-child(4)');
            
            linkCount = len(link) - 1;

            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print(commonConstant_NAME.GEUAMCHEOUN_BOROUGH_NOTICE," Next Page : {}".format(cnt));
                    return Geuamcheoun_notice.mainCra(cnt, numberCnt);
                else:
                    if numberCnt == commonConstant_NAME.STOPCUOUNT:
                        break;

                    # print(link[i].attrs.get('href').removeprefix('.'));
                    linkrep = link[i].attrs.get('href').removeprefix('.');
                    
                    firebase_con.updateModel(commonConstant_NAME.GEUAMCHEOUN_BOROUGH_NOTICE,numberCnt,
                        datasModel.toJson(
                            "https://www.geumcheon.go.kr/portal{}".format(linkrep),
                            numberCnt,
                            "",
                            title[i].text.strip(),
                            "",
                            registrationdate[i].text,
                            "금천구_공지사항",
                        )
                    );
        else : 
            print(response.status_code);
            