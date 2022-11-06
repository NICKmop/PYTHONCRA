import requests
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup


class Gangdong_notice:
    def mainCra(cnt,numberCnt):
        cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.GANGDONG_NAME);
        maxCntNumber = max(cntNumber);
        url = 'https://www.gangdong.go.kr/web/newportal/bbs/b_068?cp={}&pageSize=20&sortOrder=BA_REGDATE&sortDirection=DESC&bcId=b_068&baNotice=false&baCommSelec=false&baOpenDay=true&baUse=true'.format(cnt);
        response = requests.get(url);

        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser')
            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('tr > .tlt > a');
            title = soup.select('tr > .tlt > a');
            registrationdate = soup.select('td:nth-child(4)');

            linkCount = len(link) - 1;
        
            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print(commonConstant_NAME.GANGDONG_BOROUGH_NOTICE," Next Page : {}".format(cnt));
                    return Gangdong_notice.mainCra(cnt, numberCnt);
                else:
                    # if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT:
                    #     break;
                    if(fnCompareTitle(commonConstant_NAME.GANGDONG_NAME, title[i].text.strip()) == 1):
                        break;
                    else:
                        maxCntNumber += 1;
                    
                        changeText = str(registrationdate[i].text);
                        firebase_con.updateModel(commonConstant_NAME.GANGDONG_NAME,maxCntNumber,
                            datasModel.toJson(
                                "https://www.gangdong.go.kr{}".format(link[i].attrs.get('href')),
                                maxCntNumber,
                                "",
                                title[i].text.strip(),
                                "",
                                fnChnagetype(changeText.strip()),
                                "강동구청",
                            )
                        );  
        else : 
            print(response.status_code)
            