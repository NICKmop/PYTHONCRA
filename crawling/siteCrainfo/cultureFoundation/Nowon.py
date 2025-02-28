import requests
from bs4 import BeautifulSoup
from common.common_fnc import fnCompareTitle
from common.common_fnc import fnChnagetype
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel

class Nowon:
    def mainCra(cnt,numberCnt):
        try:
            requests.packages.urllib3.disable_warnings()
            requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.NOWON_NAME);
            maxCntNumber = max(cntNumber);

            url = 'https://nowonarts.kr/html/openspace/notice.php';
            response = requests.get(url, verify=False);

            if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
                html = response.text;
                soup = BeautifulSoup(html, 'html.parser');

                # 타이틀 ,기관, 링크, 등록일, 번호
                link = soup.select('.tb_subject > a');
                title = soup.select('.tb_subject > a');
                registrationdate = soup.select('.tb_date');

                linkCount = len(link) - 1;
                
                for i in range(len(link)):
                    if linkCount == i:
                        numberCnt += 1;
                        cnt += 1;
                        firebase_con.updateModel(commonConstant_NAME.NOWON_NAME,maxCntNumber,
                                datasModel.toJson(
                                    "https://nowonarts.kr{}".format(link[i].attrs.get('href')),
                                    numberCnt,
                                    "",
                                    title[i].text.strip(),
                                    "",
                                    fnChnagetype(changeText.strip()),
                                    "노원문화재단",
                                )
                            );

                        print("Nowon Next Page : {}".format(cnt));
                        # return Nowon.mainCra(cnt, numberCnt);
                    else:
                        # if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT:
                        #     break;
                        changeText= str(registrationdate[i].text);

                        if(fnCompareTitle(commonConstant_NAME.NOWON_NAME, title[i].text.strip(), changeText) == 1):
                                break;
                        else:
                            maxCntNumber += 1;
                            if(changeText != '등록일'):
                                numberCnt += 1;
                                firebase_con.updateModel(commonConstant_NAME.NOWON_NAME,maxCntNumber,
                                # firebase_con.updateModel(commonConstant_NAME.NOWON_NAME,numberCnt,
                                    datasModel.toJson(
                                        "https://nowonarts.kr{}".format(link[i].attrs.get('href')),
                                        maxCntNumber,
                                        "",
                                        title[i].text.strip(),
                                        "",
                                        fnChnagetype(changeText.strip()),
                                        "노원문화재단",
                                    )
                                );
            else : 
                print(response.status_code)
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
            raise ValueError("Argument에 잘못된 값이 전달되었습니다.")