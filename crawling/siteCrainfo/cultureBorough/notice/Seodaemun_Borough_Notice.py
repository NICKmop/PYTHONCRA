import requests
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Seodaemun_notice:
    def mainCra(cnt):
        cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.SEODAEMUN_NAME);
        numberCnt = max(cntNumber);

        url = 'https://www.sscmc.or.kr/info/notice/list.asp?db=BBS_notice&pageno={}&startpage=1&where=&keyfield=&keyword=&catekkk='.format(cnt);
        response = requests.get(url);
        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser')
            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('tr > td:nth-child(2) > a');
            title = soup.select('tr > td:nth-child(2) > a');
            registrationdate = soup.select('tr > td:nth-child(4)');
            checkValue = soup.select("tr > td:nth-child(1)");
            
            linkCount = len(link) - 1;

            for i in range(len(link)):
                if linkCount == i:
                    cnt += 1;
                    print(commonConstant_NAME.SEODAEMUN_NAME," Next Page : {}".format(cnt));
                    return Seodaemun_notice.mainCra(cnt);
                else:
                    # if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT:
                    #     break;
                    
                    if(fnCompareTitle(commonConstant_NAME.SEODAEMUN_NAME, title[i].text.strip()) == 1):
                        break;
                    else:
                        if(checkValue[i].text.strip() != ''):
                            numberCnt += 1;
                            changeText = str(registrationdate[i].text.replace('.','-'));
                            firebase_con.updateModel(commonConstant_NAME.SEODAEMUN_NAME,numberCnt,
                                datasModel.toJson(
                                    "https://www.sscmc.or.kr/info/notice/{}".format(link[i].attrs.get('href')),
                                    numberCnt,
                                    "",
                                    title[i].text.strip(),
                                    "",
                                    fnChnagetype(changeText.strip()),
                                    "서대문공단",
                                )
                            );
        else : 
            print(response.status_code)
            