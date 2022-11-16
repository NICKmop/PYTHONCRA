import requests
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Guro_notice:
    def mainCra(cnt,numberCnt):
        cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.GURO_NAME);
        maxCntNumber = max(cntNumber);

        url = 'https://www.guro.go.kr/www/selectBbsNttList.do?bbsNo=662&&pageUnit=10&key=1790&pageIndex={}'.format(cnt);
        response = requests.get(url);
        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser')
            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('.p-subject > a');
            title = soup.select('.p-subject > a');
            registrationdate = soup.select('td:nth-child(5)');
            
            linkCount = len(link) - 1;

            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print(commonConstant_NAME.GURO_BOROUGH_NOTICE," Next Page : {}".format(cnt));
                    return Guro_notice.mainCra(cnt, numberCnt);
                else:
                    # if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT:
                    #     break;
                    # 기존 저장되어 있는 제목과 부딫 힐 경우 다음 함수로 이동
                    if('NEW' in title[i].text.strip()):
                        replaceString = title[i].text.strip().replace('NEW', '').strip();
                    else:
                        replaceString = title[i].text.strip();

                    if(fnCompareTitle(commonConstant_NAME.GURO_NAME, replaceString) == 1):
                        break;
                    else:
                        maxCntNumber += 1;

                        changeText = str(registrationdate[i].text.replace('.','-'));
                        firebase_con.updateModel(commonConstant_NAME.GURO_NAME,maxCntNumber,
                            datasModel.toJson(
                                "https://www.guro.go.kr/www{}".format(link[i].attrs.get('href').replace(".","",1)),
                                maxCntNumber,
                                "",
                                replaceString,
                                "",
                                fnChnagetype(changeText.strip()),
                                "구로구청",
                            )
                        );
        else : 
            print(response.status_code)
            