import requests
from bs4 import BeautifulSoup
from common.common_fnc import fnCompareTitle
from common.common_fnc import fnChnagetype
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel

class Seocho:
    def mainCra(cnt,numberCnt):
        try:
            requests.packages.urllib3.disable_warnings()
            requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.SEOCHO_NAME);
            maxCntNumber = max(cntNumber);

            url = 'http://www.seochocf.or.kr/site/main/archive/post/category/%EA%B3%B5%EC%A7%80%EC%82%AC%ED%95%AD?cp={}&sortDirection=DESC&catId=7&metaCode1=GENERAL'.format(cnt);
            response = requests.get(url);

            if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
                html = response.text;
                soup = BeautifulSoup(html, 'html.parser');

                # 타이틀 ,기관, 링크, 등록일, 번호
                link = soup.select('tbody > tr > td.left > a.arc_tit');
                title = soup.select('tbody > tr > td.left > a.arc_tit');
                registrationdate = soup.select('tbody > tr > td:nth-child(4)');

                linkCount = len(link) - 1;

                for i in range(len(link)):
                    numberCnt += 1;
                    if linkCount == i:
                        cnt += 1;
                        print("Seocho Next Page : {}".format(cnt));
                        return Seocho.mainCra(cnt, numberCnt);
                    else:
                        # if numberCnt == commonConstant_NAME.SEOUL_STOP_COUNT_THREE + 1:
                        #     break;
                        changeText= str(registrationdate[i].text);

                        if(fnCompareTitle(commonConstant_NAME.SEOCHO_NAME, title[i].text.strip(), changeText) == 1):
                                break;
                        else:
                            maxCntNumber += 1;
                            firebase_con.updateModel(commonConstant_NAME.SEOCHO_NAME,maxCntNumber,
                                datasModel.toJson(
                                    "http://www.seochocf.or.kr{}".format(link[i].attrs.get('href')),
                                    maxCntNumber,
                                    "",
                                    title[i].text.strip(),
                                    "",
                                    fnChnagetype(changeText.strip()),
                                    "서초문화재단",
                                )
                            );
            else : 
                print(response.status_code)
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
            raise ValueError("Argument에 잘못된 값이 전달되었습니다.")