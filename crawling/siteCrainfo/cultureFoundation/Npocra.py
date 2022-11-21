import requests
from bs4 import BeautifulSoup
from common.common_fnc import fnCompareTitle
from common.common_fnc import fnChnagetype
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel

class Npocra:
    def mainCra(cnt,numberCnt):
        requests.packages.urllib3.disable_warnings()
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
        cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.SEOUL_NAME);
        maxCntNumber = max(cntNumber);

        url = 'https://www.snpo.kr/bbs/board.php?bo_table=bbs_npo&page={}'.format(cnt);
        
        response = requests.get(url);
        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser');

            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('.title');
            title = soup.select('.title');
            registrationdate = soup.select('.date');
            checkValue = soup.select('td:nth-child(3)')
            linkCount = len(link) - 1;

            for i in range(len(link)):
                numberCnt += 1;
                
                if linkCount == i:
                    cnt += 1;

                    print("Npocra Next Page : {}".format(cnt));
                    return Npocra.mainCra(cnt, numberCnt);
                else:
                    # if numberCnt == commonConstant_NAME.SEOUL_STOP_COUNT_THREE:
                    #     break;

                    if(fnCompareTitle(commonConstant_NAME.SEOUL_NAME, title[i].text.strip()) == 1):
                        break;
                    else:
                        maxCntNumber += 1;

                        changeText= str(registrationdate[i+1].text.replace('.','-'));
                        if(checkValue[i].text.strip() == 'NPO지원센터'):
                            numberCnt -= 1;
                        
                        if(checkValue[i].text.strip() != 'NPO지원센터'):
                            firebase_con.updateModel(commonConstant_NAME.SEOUL_NAME,maxCntNumber,
                                datasModel.toJson(
                                    link[i].attrs.get('href'),
                                    maxCntNumber,
                                    "",
                                    title[i].text.strip(),
                                    "",
                                    fnChnagetype(changeText.strip()),
                                    "서울NPO지원센터",
                                )
                            );  
        else : 
            print(response.status_code)