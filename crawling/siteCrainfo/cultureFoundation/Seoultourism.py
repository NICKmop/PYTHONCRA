import requests
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Seoultourism:
    def mainCra(cnt):
        try:
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.SEOUL_NAME);
            numberCnt = max(cntNumber);

            url = 'https://www.sto.or.kr/unitrcrit?curPage={}'.format(cnt);
            response = requests.get(url);

            if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
                html = response.text;
                soup = BeautifulSoup(html, 'html.parser')

                link = soup.select('.od-row > a');
                title = soup.select('.od-row > a');
                registrationdate = soup.select('.col4');

                linkCount = len(link) - 1;

                for i in range(len(link)):
                    numberCnt += 1;
                    changeText= str(registrationdate[i].text.strip());
                    if linkCount == i:
                        cnt += 1;

                        firebase_con.updateModel( commonConstant_NAME.SEOUL_NAME,numberCnt,
                            datasModel.toJson(
                                "https://www.sto.or.kr{}".format(link[i].attrs.get('href')),
                                numberCnt,
                                "",
                                title[i].text.strip(),
                                "",
                                fnChnagetype(changeText),
                                "서울관광재단"
                            )
                        )
                        print("Seoultourism Next Page : {}".format(cnt));
                        return Seoultourism.mainCra(cnt),
                    else:
                        # if numberCnt == commonConstant_NAME.SEOUL_STOP_COUNT_EIGHT:
                        #     break;
                        if(fnCompareTitle(commonConstant_NAME.SEOUL_NAME, title[i].text.strip()) == 1):
                            break;
                        
                        if(changeText == '작성일'):
                            numberCnt -= 1;
                        if(changeText != '작성일'):
                            firebase_con.updateModel( commonConstant_NAME.SEOUL_NAME,numberCnt,
                                datasModel.toJson(
                                    "https://www.sto.or.kr{}".format(link[i].attrs.get('href')),
                                    numberCnt,
                                    "",
                                    title[i].text.strip(),
                                    "",
                                    fnChnagetype(changeText),
                                    "서울관광재단"
                                )
                            )
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
            raise ValueError("Argument에 잘못된 값이 전달되었습니다.")