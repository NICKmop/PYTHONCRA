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

            url = 'https://www.gfac.or.kr/html/notify/notify1.html?page={}'.format(cnt);
            response = requests.get(url, verify=False);

            if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
                html = response.text;
                soup = BeautifulSoup(html, 'html.parser')

                link = soup.select('td.nor > a');
                title = soup.select('td.nor > a > span.cont2 > em.cont2_2');
                registrationdate = soup.select('td.nor > a > span.cont2 > em.cont2_3 > i.cont2_3_1');
                
                linkCount = len(link) - 1;

                for i in range(len(link)):
                    numberCnt += 1;
                    if linkCount == i:
                        cnt += 1;
                        print("Gwanak Next Page : {}".format(cnt));
                        return Gwanak.mainCra(cnt, numberCnt);
                    else:
                        # print(title[i].text.strip());
                        # print(link[i].attrs.get('href').replace('..',''));
                        # print(registrationdate[i].text.strip());
                        # if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT:
                        #     break;
                        changeText= str(registrationdate[i].text.strip());

                        if(fnCompareTitle(commonConstant_NAME.GWANAK_NAME, title[i].text.strip(), changeText) == 1):
                            break;
                        else:
                            maxCntNumber += 1;
                            
                            firebase_con.updateModel(commonConstant_NAME.GWANAK_NAME,maxCntNumber,
                                datasModel.toJson(
                                    "https://www.gfac.or.kr/html{}".format(link[i].attrs.get('href').replace('..','')),
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
