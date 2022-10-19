import requests
from bs4 import BeautifulSoup
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel

class Youthseoul:
    def mainCra(cnt):
        cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.SEOUL_NAME);
        numberCnt = max(cntNumber);
        url = 'https://youth.seoul.go.kr/site/main/board/notice/list?cp={}&pageSize=15&sortOrder=BA_REGDATE&sortDirection=DESC&bcId=notice&baCategory1=basic&baNotice=false&baCommSelec=true&baOpenDay=true&baUse=true'.format(cnt);
        
        response = requests.get(url);
        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser');

            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('.tlt > a');
            title = soup.select('.tlt');
            registrationdate = soup.select('td:nth-child(3)');
            
            linkCount = len(link);

            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print(commonConstant_NAME.DOBONG_BOROUGH_NOTICE, "Next Page : {}".format(cnt));
                    return Youthseoul.mainCra(cnt);
                else:
                    if numberCnt == commonConstant_NAME.SEOUL_STOP_COUNT_TWO:
                        break;
                
                firebase_con.updateModel(commonConstant_NAME.SEOUL_NAME,numberCnt,
                    datasModel.toJson(
                        'https://youth.seoul.go.kr{}'.format(link[i].attrs.get('href')),
                        numberCnt,
                        "",
                        title[i].text.strip(),
                        "",
                        registrationdate[i].text.strip(),
                        "청년몽땅정보통",
                    )
                );
        else : 
            print(response.status_code)