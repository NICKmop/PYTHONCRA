import requests
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Dongjak_notice_event:
    def mainCra(cnt):
        try:
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.DONGJAK_NAME);
            numberCnt = max(cntNumber);

            print("numberCnt : {}".format(numberCnt));

            url = 'https://www.dongjak.go.kr/portal/bbs/B0000173/list.do?menuNo=201030&pageIndex={}'.format(cnt);
            response = requests.get(url);

            if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
                html = response.text;
                soup = BeautifulSoup(html, 'html.parser');

                # 타이틀 ,기관, 링크, 등록일, 번호
                link = soup.select('.col-sm-12 > dl > df > a');
                title = soup.select('.col-sm-12 > dl > df > a');
                registrationdate = soup.select('ul > li:nth-child(3)');

                # print(registrationdate);
                linkCount = len(link) - 1;

                for i in range(len(link)):
                    numberCnt += 1;
                    if linkCount == i:
                        cnt += 1;
                        print(commonConstant_NAME.DONGJAK_BOROUGH_NOTICE_EVENT," Next Page : {}".format(cnt));
                        return Dongjak_notice_event.mainCra(cnt);
                    else:
                        print(title[i].text.strip());
                        print(link[i].attrs.get('href'));
                        print(registrationdate[i].text.strip());
                        # if numberCnt == commonConstant_NAME.SEOUL_STOP_COUNT_FOUR:
                        #     break;
                        # if(fnCompareTitle(commonConstant_NAME.DONGJAK_NAME, title[i].text.strip()) == 1):
                        #     break;

                        # changeText = str(registrationdate[i].text);
                        # firebase_con.updateModel(commonConstant_NAME.DONGJAK_NAME,numberCnt,
                        #     datasModel.toJson(
                        #         "https://www.dongjak.go.kr{}".format(link[i].attrs.get('href')),
                        #         numberCnt,
                        #         "",
                        #         title[i].text.strip(),
                        #         "",
                        #         fnChnagetype(changeText.strip()),
                        #         "동작구청",
                        #     )
                        # );
            else : 
                print(response.status_code)
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
            raise ValueError("Argument에 잘못된 값이 전달되었습니다.")
            