from multiprocessing.sharedctypes import Value
from exceptiongroup import catch
import requests
from bs4 import BeautifulSoup
from common.common_fnc import fnCompareTitle
from common.common_fnc import fnChnagetype
from siteCrainfo.cultureBorough.notice.Yeongdeungpo_Borough_Notice import Yeongdeungpo_notice
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel

class Yeongdeungpo:
    def mainCra(cnt,numberCnt):
        requests.packages.urllib3.disable_warnings()
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

        # cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.YEONGDEUNGPO_NAME);
        # maxCntNumber = max(cntNumber);

        url = 'https://www.ydpcf.or.kr/board.do?bid=1&p={}'.format(cnt);
        response = requests.get(url);

        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser');

            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('ul.board-list-wrap > li > ul.board-body > li.board-subject > a');
            title = soup.select('ul.board-list-wrap > li > ul.board-body > li.board-subject > a');
            registrationdate = soup.select('ul.board-list-wrap > li > ul.board-body > li.board-date'); # board-date
            checkPassValue = soup.select("ul.board-list-wrap > li > ul.board-body > li.board-cat");

            linkCount = len(link);

            for i in range(linkCount):
                numberCnt += 1;
                if linkCount == i + 1:
                    cnt += 1;

                    print("Yeongdeungpo Next Page : {}".format(cnt));
                    return Yeongdeungpo.mainCra(cnt, numberCnt);
                else:

                    if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT:
                        break; 
                    # 기존 저장되어 있는 제목과 부딫 힐 경우 다음 함수로 이동
                    # if(fnCompareTitle(commonConstant_NAME.YEONGDEUNGPO_NAME, title[i].text.strip()) == 1):
                    #     break;
                    # else:
                    #     maxCntNumber += 1;
                    changeText= str(registrationdate[i].text.strip().split('|')[1].strip().replace('.','-'));
                    firebase_con.updateModel(commonConstant_NAME.YEONGDEUNGPO_NAME,numberCnt,
                        datasModel.toJson(
                            "https://www.ydpcf.or.kr/{}".format(link[i].attrs.get('href')),
                            numberCnt,
                            "",
                            title[i].text.strip(),
                            "",
                            fnChnagetype(changeText.strip()),
                            "영등포문화재단",
                        )
                    );
        else : 
            print(response.status_code)