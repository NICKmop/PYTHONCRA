import requests
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from common.common_fnc import pageconnectLoadUrl
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup
import time

class Gangbuk_notice:
    def mainCra(cnt):
        try:
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.GANGBUK_NAME);
            numberCnt = max(cntNumber);

            url = 'https://www.gangbuk.go.kr/www/boardList.do?page={}&boardSeq=41&key=285&category=&searchType=&searchKeyword=&searchFile=&subContents=&mpart=&part=&item='.format(cnt);
            # response = requests.get(url);
            soup = BeautifulSoup(pageconnectLoadUrl(url), 'html.parser');

            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('.subject > a');
            title = soup.select('.subject > a');
            registrationdate = soup.select('.date');
            
            linkCount = len(link) - 1;

            for i in range(len(link)):
                changeText = str(registrationdate[i].text.replace('.', '-'));
                numberCnt += 1;

                if linkCount == i:
                    cnt += 1;
                    firebase_con.updateModel(commonConstant_NAME.GANGBUK_NAME,numberCnt,
                        datasModel.toJson(
                            "https://www.gangbuk.go.kr/www{}".format(link[i].attrs.get('href').replace('.', '')),
                            numberCnt,
                            "",
                            title[i].text.strip(),
                            "",
                            fnChnagetype(changeText.strip()),
                            "강북구청",
                        )
                    );
                    print(commonConstant_NAME.GANGBUK_BOROUGH_NOTICE," Next Page : {}".format(cnt));
                    return Gangbuk_notice.mainCra(cnt);
                else:
                    # if numberCnt == commonConstant_NAME.SEOUL_STOP_COUNT_FOUR:
                    #     break;

                    if(fnCompareTitle(commonConstant_NAME.GANGBUK_NAME, title[i].text.strip()) == 1):
                        break;

                    firebase_con.updateModel(commonConstant_NAME.GANGBUK_NAME,numberCnt,
                        datasModel.toJson(
                            "https://www.gangbuk.go.kr/www{}".format(link[i].attrs.get('href').replace('.', '')),
                            numberCnt,
                            "",
                            title[i].text.strip(),
                            "",
                            fnChnagetype(changeText.strip()),
                            "강북구청",
                        )
                    );
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
            raise ValueError("Argument에 잘못된 값이 전달되었습니다.")