import requests
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Seodaemun:
    def mainCra(cnt,numberCnt):
        try:
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.SEODAEMUN_NAME);
            maxCntNumber = max(cntNumber);
            url = 'https://www.sscmc.or.kr/info/notice/list.asp?db=BBS_notice&pageno={}&startpage=1&where=&keyfield=&keyword=&catekkk='.format(cnt);
            response = requests.get(url, verify=False);
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
                    numberCnt += 1;
                    if linkCount == i:
                        cnt += 1;
                        print(commonConstant_NAME.SEODAEMUN_NAME," Next Page : {}".format(cnt));
                        return Seodaemun.mainCra(cnt,numberCnt),
                    else:
                        if(checkValue[i].text != ''):
                            # if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT:
                            #     break;
                            if(fnCompareTitle(commonConstant_NAME.SEODAEMUN_NAME, title[i].text.strip()) == 1):
                                break;
                            else:
                                maxCntNumber += 1;
                                changeText = str(registrationdate[i].text.replace('.','-'));
                                firebase_con.updateModel(commonConstant_NAME.SEODAEMUN_NAME,maxCntNumber,
                                    datasModel.toJson(
                                        "https://www.sscmc.or.kr/info/notice/{}".format(link[i].attrs.get('href')),
                                        maxCntNumber,
                                        "",
                                        title[i].text.strip(),
                                        "",
                                        fnChnagetype(changeText.strip()),
                                        "서대문공단",
                                    )
                                );
            else : 
                print(response.status_code)
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
            raise ValueError("Argument에 잘못된 값이 전달되었습니다.") 