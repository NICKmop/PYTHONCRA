import requests
from bs4 import BeautifulSoup
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
import datetime


class Gwangzin:
    def mainCra(cnt,numberCnt):
        cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.GWANGZIN_NAME);
        maxCntNumber = max(cntNumber);

        url = 'http://www.naruart.or.kr/bbs/board.php?bo_table=notice&page={}'.format(cnt);
        response = requests.get(url);

        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser')
            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('tbody > tr > td.td_subject > div > a');
            title = soup.select('tbody > tr > td.td_subject');
            registrationdate = soup.select('tbody > tr > td.td_datetime');

            linkCount = len(link) - 1;

            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print(commonConstant_NAME.GWANGZIN_NAME," Next Page : {}".format(cnt));
                    return Gwangzin.mainCra(cnt, numberCnt);
                else:
                    # if numberCnt == commonConstant_NAME.STOPCUOUNT:
                    #     break;

                    if(fnCompareTitle(commonConstant_NAME.GWANGZIN_NAME, title[i].text.strip()) == 1):
                        break;
                    else:
                        maxCntNumber += 1;
                        cngdate = registrationdate[i].text.replace('.','-');
                        firebase_con.updateModel(commonConstant_NAME.GWANGZIN_NAME,maxCntNumber,
                            datasModel.toJson(
                                link[i].attrs.get('href'),
                                maxCntNumber,
                                "",
                                title[i].text.strip(),
                                "",
                                fnChnagetype("20"+cngdate),
                                "광진문화재단",
                            )
                        );
        else : 
            print(response.status_code)