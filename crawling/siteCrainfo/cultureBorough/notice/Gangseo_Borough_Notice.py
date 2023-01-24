import requests
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Gangseo_notice:
    def mainCra(cnt):
        try:
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.GANGSEO_NAME);
            numberCnt = max(cntNumber);

            url = 'https://www.gangseo.seoul.kr/gs040101?curPage={}'.format(cnt);
            response = requests.get(url);

            if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
                html = response.text;
                soup = BeautifulSoup(html, 'html.parser')
                # 타이틀 ,기관, 링크, 등록일, 번호
                link = soup.select('tr > td > a');
                title = soup.select('tr > td > a');
                registrationdate = soup.select('td:nth-child(4)');
                noticeCheck = soup.select('td:nth-child(1)');
                
                linkCount = len(link) - 1;

                for i in range(len(link)):
                    numberCnt += 1;
                    if linkCount == i:
                        cnt += 1;
                        print(commonConstant_NAME.GANGSEO_BOROUGH_NOTICE," Next Page : {}".format(cnt));
                        return Gangseo_notice.mainCra(cnt);
                    else:
                        
                        if(noticeCheck[i].text.strip() == ''):
                            numberCnt -= 1;

                        if(noticeCheck[i].text.strip() != ''):
                            # if(fnCompareTitle(commonConstant_NAME.GANGSEO_NAME, title[i].text.strip()) == 1):
                            #     break;
                            if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT:
                                break;
                            changeText = str(registrationdate[i].text);
                            firebase_con.updateModel(commonConstant_NAME.GANGSEO_NAME,numberCnt,
                                datasModel.toJson(
                                    "https://www.gangseo.seoul.kr{}".format(link[i].attrs.get('href')),
                                    numberCnt,
                                    "",
                                    title[i].text.strip(),
                                    "",
                                    fnChnagetype(changeText.strip()),
                                    "강서구청",
                                )
                            );
                        else:
                            print("none blank : {}".format(title[i].text.strip()));
                        
            else : 
                print(response.status_code)
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
            raise ValueError("Argument에 잘못된 값이 전달되었습니다.")
            