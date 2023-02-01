import requests
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Nowon_notice_event:
    def mainCra(cnt):
        try:
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.NOWON_NAME);
            numberCnt = max(cntNumber);
            url = 'https://www.nowon.kr/www/user/bbs/BD_selectBbsList.do?q_bbsCode=1002&q_bbscttSn=&q_estnColumn1=11&q_rowPerPage=10&q_currPage={}&q_sortName=&q_sortOrder=&q_searchKeyTy=sj___1002&q_searchVal=&'.format(cnt);
            response = requests.get(url);

            print("numberCnt : {}".format(numberCnt));

            if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
                html = response.text;
                soup = BeautifulSoup(html, 'html.parser')
                # 타이틀 ,기관, 링크, 등록일, 번호
                link = soup.select('.cell-subject > a');
                title = soup.select('.cell-subject > a');
                registrationdate = soup.select('td:nth-child(5)');

                linkCount = len(link) - 1;
            
                for i in range(len(link)):
                    numberCnt += 1;
                    if linkCount == i:
                        cnt += 1;
                        print(commonConstant_NAME.NOWON_BOROUGH_NOTICE_EVENT," Next Page : {}".format(cnt));
                        return Nowon_notice_event.mainCra(cnt);
                    else:  
                        # if numberCnt == 121:
                        #     break;
                        if(fnCompareTitle(commonConstant_NAME.NOWON_NAME, title[i].text.strip()) == 1):
                            break;
                        
                        changeText = str(registrationdate[i].text);
                        firebase_con.updateModel(commonConstant_NAME.NOWON_NAME,numberCnt,
                            datasModel.toJson(
                                "https://www.nowon.kr/www/user/bbs/{}&q_estnColumn1=11&q_deptCode=&q_rowPerPage=10&q_currPage=1&q_sortName=&q_sortOrder=&q_searchKeyTy=sj___1002&q_searchVal=&".format(link[i].attrs.get('href')),
                                numberCnt,
                                "",
                                title[i].text.strip(),
                                "",
                                fnChnagetype(changeText.strip()),
                                "노원구청",
                            )
                        );
            else : 
                print(response.status_code)
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
            raise ValueError("Argument에 잘못된 값이 전달되었습니다.")