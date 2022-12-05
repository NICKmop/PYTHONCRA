import requests
from bs4 import BeautifulSoup
from common.common_fnc import fnCompareTitle
from common.common_fnc import fnChnagetype
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel

class Gangdong:
    def mainCra(cnt,numberCnt):
        try:
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.GANGDONG_NAME);
            maxCntNumber = max(cntNumber);
            url = 'https://www.gdfac.or.kr/web/lay2/bbs/S1T235C370/A/23/list.do?rows=10&cpage={}'.format(cnt);
            response = requests.get(url);

            if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
                html = response.text;
                soup = BeautifulSoup(html, 'html.parser')
                # 타이틀 ,기관, 링크, 등록일, 번호
                title = soup.select('.tit > a');
                link = soup.select('.tit > a');
                registrationdate = soup.select('.tit > ul > li:nth-child(1)');
                checkValue = soup.select('.tit > ul > li:nth-child(2)');

                linkCount = len(link) - 1;

                for i in range(len(link)):
                    if linkCount == i:
                        cnt += 1;
                        print("Gangdong Next Page : {}".format(cnt));
                        return Gangdong.mainCra(cnt, numberCnt);
                    else:
                        if('작성일' in registrationdate[i].text.strip() ):
                            registWordSp = registrationdate[i].text.strip().replace('작성일','');
                        if('조회수' in checkValue[i].text.strip()):
                            checkValueSp = checkValue[i].text.strip().replace('조회수','');


                        if(checkValueSp != '공지'):
                            numberCnt += 1;
                            # if numberCnt == commonConstant_NAME.STOPCUOUNT + 1:
                            #     break;
                            if(fnCompareTitle(commonConstant_NAME.GANGDONG_NAME, title[i].text.strip()) == 1):
                                break;
                            else:
                                maxCntNumber += 1;
                                changeText= str(registWordSp);
                                firebase_con.updateModel(commonConstant_NAME.GANGDONG_NAME,maxCntNumber,
                                    datasModel.toJson(
                                        "https://www.gdfac.or.kr/web/lay2/bbs/S1T235C370/A/23/{}".format(link[i].attrs.get('href')),
                                        maxCntNumber,
                                        "",
                                        title[i].text.strip(),
                                        "",
                                        fnChnagetype(changeText.strip()),
                                        "강동문화재단",
                                    )
                                );
            else : 
                print(response.status_code);
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
                raise ValueError("Argument에 잘못된 값이 전달되었습니다.")