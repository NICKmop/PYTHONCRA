import requests
from bs4 import BeautifulSoup
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel

class Seongdong:
    def mainCra(cnt,numberCnt):
        requests.packages.urllib3.disable_warnings()
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

        numberCnt = numberCnt;
        cnt  = cnt; # 1
        url = 'https://www.sdfac.or.kr/kor/sdfac/board/noti_list.do?page={}&b_idx=&bbs_id=&article_category=&searchCnd=3&searchWrd='.format(cnt);
        response = requests.get(url);

        if response.status_code == 200:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser');

            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('div.content > ul.listType > li > a.arc_tit');
            title = soup.select('tbody > tr > td.left > a.arc_tit');
            registrationdate = soup.select('tbody > tr > td:nth-child(4)');

            linkCount = len(link) - 1;
            print("linkCount : ", linkCount);

            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print("Next Page : {}".format(cnt));
                    return Seongdong.mainCra(cnt, numberCnt);
                else:
                    print("title : ", title[i].text.strip());
                    print(link[i].attrs.get('href'))
                    # print("https://www.gbcf.or.kr/{}".format(link[i].attrs.get('href')));
                    print("registrationdate : ", registrationdate[i].text.strip());
                    
                    if numberCnt == commonConstant_NAME.STOPCUOUNT:
                        break;
                    
                    # firebase_con.updateModel(commonConstant_NAME.SEONGDONG_NAME,numberCnt,
                    #     datasModel.toJson(
                    #         link[i].attrs.get('href'),
                    #         numberCnt,
                    #         "",
                    #         title[i].text.strip(),
                    #         "",
                    #         registrationdate[i].text.strip(),
                    #         "성동문화재단",
                    #     )
                    # );
        else : 
            print(response.status_code)