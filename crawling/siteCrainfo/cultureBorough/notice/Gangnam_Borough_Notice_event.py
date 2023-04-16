import requests
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup


class Gangnam_notice_event:
    def mainCra(cnt):
        try:
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.GANGNAM_NAME);
            numberCnt = max(cntNumber);
            url = 'https://www.gangnam.go.kr/board/B_000045/list.do?mid=ID05_040103&pgno={}&deptField=BDM_DEPT_ID&deptId=&keyfield=bdm_main_title&keyword='.format(cnt);
            response = requests.get(url);

            print("numberCnt : {}".format(numberCnt));

            if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
                html = response.text;
                soup = BeautifulSoup(html, 'html.parser')
                # 타이틀 ,기관, 링크, 등록일, 번호
                link = soup.select('.align-l > a');
                title = soup.select('.align-l > a');
                registrationdate = soup.select('td:nth-child(5)');

                linkCount = len(link) - 1;
            
                for i in range(len(link)):
                    numberCnt += 1;
                    if linkCount == i:
                        cnt += 1;
                        print(commonConstant_NAME.GANGNAM_BOROUGH_NOTICE_EVENT," Next Page : {}".format(cnt));
                        return Gangnam_notice_event.mainCra(cnt);
                    else:  
                        # print(title[i].text.strip());
                        # if numberCnt == 193:
                        #     break;
                        changeText = str(registrationdate[i].text);
                        if(fnCompareTitle(commonConstant_NAME.GANGDONG_NAME, title[i].text.strip(), changeText) == 1):
                            break;
                        
                        firebase_con.updateModel(commonConstant_NAME.GANGNAM_NAME,numberCnt,
                            datasModel.toJson(
                                "https://www.gangnam.go.kr{}".format(link[i].attrs.get('href')),
                                numberCnt,
                                "",
                                title[i].text.strip(),
                                "",
                                fnChnagetype(changeText.strip()),
                                "강남구청",
                            )
                        );
            else : 
                print(response.status_code)
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
            raise ValueError("Argument에 잘못된 값이 전달되었습니다.")