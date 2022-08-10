import requests
from bs4 import BeautifulSoup
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel

class Gnagbuk:
    def mainCra(cnt,numberCnt):
        numberCnt = numberCnt;
        cnt  = cnt; # 1
        url = 'http://www.gbcf.or.kr/load.asp?subPage=510&searchValue=&searchType=&cate=&page={}&board_md=list'.format(cnt);
        response = requests.get(url);

        if response.status_code == 200:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser')
            # 타이틀 ,기관, 링크, 등록일, 번호
            title = soup.select('div.bbs_normal_list > ul > li > div.subject > div.subject_inner > div.subject_box > a');
            link = soup.select('div.bbs_normal_list > ul > li > div.subject > div.subject_inner > div.subject_box > a');
            registrationdate = soup.select('div.bbs_normal_list > ul > li > div.subject > div.subject_inner > span');

            linkCount = len(link) - 1;
            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print("Next Page : {}".format(cnt));
                    return Gnagbuk.mainCra(cnt, numberCnt);
                else:
                    if numberCnt == commonConstant_NAME.STOPCUOUNT:
                        break;
                    
                    firebase_con.updateModel(commonConstant_NAME.GANGBUK_NAME,numberCnt,
                        datasModel.toJson(
                            "https://www.gbcf.or.kr/{}".format(link[i].attrs.get('href')),
                            numberCnt,
                            "",
                            title[i].text.strip(),
                            "",
                            registrationdate[i].text,
                            "강북문화재단",
                        )
                    );
        else : 
            print(response.status_code)