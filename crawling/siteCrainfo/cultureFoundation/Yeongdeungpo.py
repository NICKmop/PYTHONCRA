import requests
from bs4 import BeautifulSoup
from siteCrainfo.cultureBorough.notice.Yeongdeungpo_Borough_Notice import Yeongdeungpo_notice
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from common.common_fnc import fnCompareTitle
from models.datasModel import datasModel

class Yeongdeungpo:
    def mainCra(cnt,numberCnt):
        requests.packages.urllib3.disable_warnings()
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

        # 최근 숫자 확인후 STOP
        # cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.YEONGDEUNGPO_NAME);
        # print("cntNumber ; {}".format(max(cntNumber)));

        url = 'https://www.ydpcf.or.kr/board.do?bid=1&p={}'.format(cnt);
        response = requests.get(url);

        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser');

            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('ul.board-list-wrap > li > ul.board-body > li.board-subject > a');
            title = soup.select('ul.board-list-wrap > li > ul.board-body > li.board-subject > a');
            registrationdate = soup.select('ul.board-list-wrap > li > ul.board-body > li.board-date'); # board-date
                
            # 카테고리 구분
            checkPassValue = soup.select("ul.board-list-wrap > li > ul.board-body > li.board-cat");
            # 크롤링 하려는 링크 숫자
            linkCount = len(link);
            # 문화재단내의 값중 동인 한게 있는지 체크 
            
            
            # print(len(compareTitle));
            # print(linkCount);

            for i in range(linkCount):
                if(checkPassValue[i].text != '공지사항'):
                    # compareVale = fnCompareTitle(commonConstant_NAME.YEONGDEUNGPO_NAME ,title[i].text.strip(), '영등포문화재단')
                    # print(compareVale);

                    numberCnt += 1;
                    if linkCount == i + 1:
                        cnt += 1;


                        print("Yeongdeungpo Next Page : {}".format(cnt));
                        return Yeongdeungpo.mainCra(cnt, numberCnt);
                    else:
                        if numberCnt == commonConstant_NAME.STOPCUOUNT:
                            break; 
                        
                        print(registrationdate[i].text.strip().split('|')[1].strip().replace('.','-'));

                        firebase_con.updateModel(commonConstant_NAME.YEONGDEUNGPO_NAME,numberCnt,
                            datasModel.toJson(
                                "https://www.ydpcf.or.kr/{}".format(link[i].attrs.get('href')),
                                numberCnt,
                                "",
                                title[i].text.strip(),
                                "",
                                registrationdate[i].text.strip().split('|')[1].strip().replace('.','-'),
                                "영등포문화재단",
                            )
                        );
        else : 
            print(response.status_code)