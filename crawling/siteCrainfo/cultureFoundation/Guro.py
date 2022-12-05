import requests
from bs4 import BeautifulSoup
from common.common_fnc import fnCompareTitle
from common.common_fnc import fnChnagetype
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel

class Guro:
    def mainCra(cnt,numberCnt):
        try:
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.GURO_NAME);
            maxCntNumber = max(cntNumber);
            url = 'https://www.guroartsvalley.or.kr/user/board/mn011801.do?page={}'.format(cnt);
            response = requests.get(url);

            if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
                html = response.text;
                soup = BeautifulSoup(html, 'html.parser')
                # 타이틀 ,기관, 링크, 등록일, 번호
                title = soup.select('.tit > a');
                link = soup.select('.tit > a');
                registrationdate = soup.select('tr > td:nth-child(4)');

                linkCount = len(link) - 1;

                for i in range(len(link)):
                    numberCnt += 1;
                    if linkCount == i:
                        cnt += 1;
                        print("Guro Next Page : {}".format(cnt));
                        return Guro.mainCra(cnt, numberCnt);
                    else:
                        # if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT + 1:
                        #     break;

                        linkAttr = link[i].attrs.get('href');
                        linkSub = linkAttr.split("(")[1].replace(")", '');
                        linkSubts = linkSub.split(",");

                        linkSubts1 = linkSubts[0].replace("'",'');
                        linkSubts2 = linkSubts[1].replace("'",'');

                        if(fnCompareTitle(commonConstant_NAME.GURO_NAME, title[i].text.strip()) == 1):
                            break;
                        else:
                            maxCntNumber += 1;
                            changeText= str(registrationdate[i].text);
                            firebase_con.updateModel(commonConstant_NAME.GURO_NAME,maxCntNumber,
                                datasModel.toJson(
                                    "https://www.guroartsvalley.or.kr/user/board/boardDefaultView.do?page={}&pageST=&pageSV=&itemCd1=&itemCd2=&menuCode=mn011801&boardId={}&index={}".format(cnt,linkSubts1,linkSubts2.replace(';','')),
                                    maxCntNumber,
                                    "",
                                    title[i].text.strip(),
                                    "",
                                    fnChnagetype(changeText.strip()),
                                    "구로문화재단",
                                )
                            );
            else : 
                print(response.status_code);
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
            raise ValueError("Argument에 잘못된 값이 전달되었습니다.")