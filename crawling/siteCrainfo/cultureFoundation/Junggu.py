import requests
from bs4 import BeautifulSoup
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from models.datasModel import datasModel

# 현재 달 날짜 찾는지 아직 미정. 

class Junggu:
    def mainCra(cnt,numberCnt):
        try:
            requests.packages.urllib3.disable_warnings()
            requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.JUNGGU_NAME);
            maxCntNumber = max(cntNumber);

            numberCnt = numberCnt;
            cnt  = cnt; # 1
            url = 'https://www.caci.or.kr/caci/bbs/BMSR00040/list.do?pageIndex={}&menuNo=200016&searchGubunCd=&searchCondition=&searchKeyword='.format(cnt);
            response = requests.get(url);

            if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
                html = response.text;
                soup = BeautifulSoup(html, 'html.parser');
                # 타이틀 ,기관, 링크, 등록일, 번호
                link = soup.select('tbody > tr > td.text-left > a');
                title = soup.select('tbody > tr > td.text-left > a');
                registrationdate = soup.select('tbody > tr > td:nth-child(4)');
                checkValue = soup.select('.onlyPc > a');


                linkCount = len(link) - 1;

                for i in range(len(link)):
                    numberCnt += 1;
                    if(checkValue[i].text.strip() != '공지'):
                        if linkCount == i:
                            cnt += 1;
                            print("Junggu Next Page : {}".format(cnt));
                            return Junggu.mainCra(cnt, numberCnt);
                        else:
                            # if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT:
                            #     break; 
                            changeText = str(registrationdate[i].text);
                            if(fnCompareTitle(commonConstant_NAME.JUNGGU_NAME, title[i].text.strip()) == 1):
                                break;
                            else:
                                maxCntNumber += 1;
                                firebase_con.updateModel(commonConstant_NAME.JUNGGU_NAME,maxCntNumber,
                                    datasModel.toJson(
                                        "https://www.caci.or.kr/caci/bbs/BMSR00040/{}".format(link[i].attrs.get('href')),
                                        maxCntNumber,
                                        "",
                                        title[i].text.strip(),
                                        "",
                                        fnChnagetype(changeText.strip()),
                                        "중구문화재단",
                                    )
                                );
                            # else:
                            #     numberCnt = 0;
            else : 
                print(response.status_code)
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
            raise ValueError("Argument에 잘못된 값이 전달되었습니다.")