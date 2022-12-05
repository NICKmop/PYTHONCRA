import requests
from bs4 import BeautifulSoup
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel

class Gwanak:
    def mainCra(cnt, numberCnt):
        try:
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.GWANAK_NAME);
            maxCntNumber = max(cntNumber);

            url = 'https://www.gfac.or.kr/html/notify/notify11.html?page={}&sub=0'.format(cnt);
            response = requests.get(url);

            if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
                html = response.text;
                soup = BeautifulSoup(html, 'html.parser')

                link = soup.select('td.nor > a');
                title = soup.select('td.nor > a > span.cont2 > em.cont2_2');
                registrationdate = soup.select('td.nor > a > span.cont2 > em.cont2_3 > i.cont2_3_2');
                
                linkCount = len(link) - 1;

                for i in range(len(link)):
                    numberCnt += 1;
                    if linkCount == i:
                        cnt += 1;
                        print("Gwanak Next Page : {}".format(cnt));
                        return Gwanak.mainCra(cnt, numberCnt);
                    else:
                        # if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT:
                        #     break;
                        if(fnCompareTitle(commonConstant_NAME.GWANAK_NAME, title[i].text.strip()) == 1):
                            break;
                        else:
                            maxCntNumber += 1;
                            changeText= str(registrationdate[i].text.strip());
                            
                            firebase_con.updateModel(commonConstant_NAME.GWANAK_NAME,maxCntNumber,
                                datasModel.toJson(
                                    "https://www.gfac.or.kr/html/notify/{}".format(link[i].attrs.get('href')),
                                    maxCntNumber,
                                    "",
                                    title[i].text.strip(),
                                    "",
                                    fnChnagetype(changeText.strip()),
                                    "관악문화재단",
                                )
                            );
            else : 
                print(response.status_code)
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
            raise ValueError("Argument에 잘못된 값이 전달되었습니다.")
