import requests
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Mapo_Institutions:
    def mainCra(cnt,numberCnt):
        url = 'https://www.mapo.go.kr/site/main/board/othernews/list?cp={}&sortOrder=BA_REGDATE&sortDirection=DESC&listType=list&bcId=othernews&baNotice=false&baCommSelec=false&baOpenDay=false&baUse=true'.format(cnt);
        response = requests.get(url);
        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser')
            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('.val_m > a');
            title = soup.select('.val_m > a');
            registrationdate = soup.select('td:nth-child(5)');

            # print(registrationdate);
            linkCount = len(link) - 1;

            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print(commonConstant_NAME.MAPO_BOROUGH_OTHER_INSTITUTIONS," Next Page : {}".format(cnt));
                    return Mapo_Institutions.mainCra(cnt, numberCnt);
                else:
                    if numberCnt == commonConstant_NAME.STOPCUOUNT:
                        break;

                    # print("linkK:::: ", link[i].attrs.get('href').removeprefix('.'));
                    # print(title);
                    # print(registrationdate);
                    
                    firebase_con.updateModel(commonConstant_NAME.MAPO_BOROUGH_OTHER_INSTITUTIONS,numberCnt,
                        datasModel.toJson(
                            "https://www.mapo.go.kr{}".format(link[i].attrs.get('href').removeprefix('.')),
                            numberCnt,
                            "",
                            title[i].text.strip(),
                            "",
                            registrationdate[i].text,
                            "마포구_타기관공시송달",
                        )
                    );
        else : 
            print(response.status_code)
            