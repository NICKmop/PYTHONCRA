import requests
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Youngsan_notice:
    def mainCra(cnt):
        try:
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.YOUNGSAN_NAME);
            numberCnt = max(cntNumber);

            url = 'https://www.yongsan.go.kr/portal/bbs/B0000041/list.do?menuNo=200228&pageIndex={}'.format(cnt);
            response = requests.get(url);

            if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
                html = response.text;
                soup = BeautifulSoup(html, 'html.parser')
                # 타이틀 ,기관, 링크, 등록일, 번호
                link = soup.select('.title > a');
                title = soup.select('.title > a');
                registrationdate = soup.select('td:nth-child(5)');

                # print(registrationdate);
                linkCount = len(link) - 1;

                for i in range(len(link)):
                    numberCnt += 1;
                    if linkCount == i:
                        cnt += 1;
                        print(commonConstant_NAME.YOUNGSAN_BOROUGH_NOTICE," Next Page : {}".format(cnt));
                        return Youngsan_notice.mainCra(cnt);
                    else:
                        # if numberCnt == commonConstant_NAME.SEOUL_STOP_COUNT_FOUR:
                        #     break;
                        changeText= str(registrationdate[i].text);

                        if(fnCompareTitle(commonConstant_NAME.YOUNGSAN_NAME, title[i].text.strip(), changeText) == 1):
                            break;
                        else:
                            firebase_con.updateModel(commonConstant_NAME.YOUNGSAN_NAME,numberCnt,
                                datasModel.toJson(
                                    "https://www.yongsan.go.kr{}".format(link[i].attrs.get('href')),
                                    numberCnt,
                                    "",
                                    title[i].text.strip(),
                                    "",
                                    fnChnagetype(changeText.strip()),
                                    "용산구청",
                                )
                            );
            else : 
                print(response.status_code)
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
            raise ValueError("Argument에 잘못된 값이 전달되었습니다.")