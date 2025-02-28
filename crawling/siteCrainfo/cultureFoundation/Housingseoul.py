import requests
from bs4 import BeautifulSoup
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel

class Housingseoul:
    def mainCra(cnt):
        try:
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.SEOUL_NAME);
            numberCnt = max(cntNumber);
            url = 'https://housing.seoul.go.kr/site/main/board/notice/list?cp={}&sortOrder=BA_REGDATE&sortDirection=DESC&bcId=notice&baNotice=false&baCommSelec=false&baOpenDay=false&baUse=true'.format(cnt);
            
            response = requests.get(url, headers={'User-Agent':'Mozilla/5.0'});
            if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
                html = response.text;
                soup = BeautifulSoup(html, 'html.parser');

                # 타이틀 ,기관, 링크, 등록일, 번호
                link = soup.select('.td-m > a');
                title = soup.select('.td-m');
                registrationdate = soup.select('.td3');
                
                linkCount = len(link);

                for i in range(len(link)):
                    numberCnt += 1;
                    if linkCount == i:
                        cnt += 1;
                        print(commonConstant_NAME.HOUSINGSEOUL_NANE, "Next Page : {}".format(cnt));
                        return Housingseoul.mainCra(cnt);
                    else:
                        # if numberCnt == commonConstant_NAME.SEOUL_STOP_COUNT_FIVE:
                        #     break;
                        changeText= str(registrationdate[i].text.strip());

                        if(fnCompareTitle(commonConstant_NAME.SEOUL_NAME, title[i].text.strip(), changeText) == 1):
                            break;
                        firebase_con.updateModel(commonConstant_NAME.SEOUL_NAME,numberCnt,
                            datasModel.toJson(
                                'https://housing.seoul.go.kr{}'.format(link[i].attrs.get('href')),
                                numberCnt,
                                "",
                                title[i].text.strip(),
                                "",
                                fnChnagetype(changeText),
                                "서울주거포털",
                            )
                        );
            else : 
                print(response.status_code);
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
            raise ValueError("Argument에 잘못된 값이 전달되었습니다.")