import requests
from bs4 import BeautifulSoup
from common.common_fnc import fnCompareTitle
from common.common_fnc import fnChnagetype
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel

class Gangnam:
    def mainCra(cnt,numberCnt):
        try:
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.GANGNAM_NAME);
            maxCntNumber = max(cntNumber);
            url = 'https://www.gangnam.go.kr/office/gfac/board/gfac_notice/list.do?mid=gfac_notice&pgno={}&keyfield=BDM_MAIN_TITLE&keyword='.format(cnt);
            response = requests.get(url);

            if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
                html = response.text;
                soup = BeautifulSoup(html, 'html.parser')
                # 타이틀 ,기관, 링크, 등록일, 번호
                title = soup.select('td.align-l');
                link = soup.select('td:nth-child(2) > a');
                registrationdate = soup.select('tr > td:nth-child(5)');
                checkValue = soup.select('tr > td:nth-child(1)');

                linkCount = len(link) - 1;

                for i in range(len(link)):
                    if linkCount == i:
                        cnt += 1;
                        print("Gangnam Next Page : {}".format(cnt));
                        return Gangnam.mainCra(cnt, numberCnt);
                    else:
                        if(checkValue[i].text.strip() != '공지'):
                            numberCnt += 1;
                            # if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT + 1:
                            #     break;
                            changeText= str(registrationdate[i].text);

                            if(fnCompareTitle(commonConstant_NAME.GANGNAM_NAME, title[i].text.strip(), changeText) == 1):
                                break;
                            else:
                                maxCntNumber += 1;
                                
                                firebase_con.updateModel(commonConstant_NAME.GANGNAM_NAME,maxCntNumber,
                                    datasModel.toJson(
                                        "https://www.gangnam.go.kr/{}".format(link[i].attrs.get('href')),
                                        maxCntNumber,
                                        "",
                                        title[i].text.strip(),
                                        "",
                                        fnChnagetype(changeText.strip()),
                                        "강남문화재단",
                                    )
                                );
            else : 
                print(response.status_code);
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
                raise ValueError("Argument에 잘못된 값이 전달되었습니다.")