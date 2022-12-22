import requests
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Songpa_notice_event:
    def mainCra(cnt):
        try:
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.SONGPA_NAME);
            numberCnt = max(cntNumber);

            print("nubmerCnt : {}".format(numberCnt));

            url = 'https://www.songpa.go.kr/www/selectBbsNttList.do?bbsNo=98&&pageUnit=10&key=2783&searchAditfield4=&searchAditfield5=&viewBgnde=&searchAditfield1=&searchAditfield2=&pageIndex={}'.format(cnt);
            response = requests.get(url);
            if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
                html = response.text;
                soup = BeautifulSoup(html, 'html.parser')
                # 타이틀 ,기관, 링크, 등록일, 번호
                link = soup.select('.p-subject > a');
                title = soup.select('.p-subject > a');
                registrationdate = soup.select('td:nth-child(4)');

                # print(registrationdate);
                linkCount = len(link) - 1;

                for i in range(len(link)):
                    numberCnt += 1;
                    if linkCount == i:
                        cnt += 1;
                        print(commonConstant_NAME.SONGPA_BOROUGH_NOTICE_EVENT," Next Page : {}".format(cnt));
                        return Songpa_notice_event.mainCra(cnt);
                    else:
                        # if numberCnt == 176:
                        #     break;
                        # print(title[i].text.strip());
                        # print(link[i].attrs.get('href'));
                        # print(registrationdate[i].text.strip());
                        if('NEW' in title[i].text.strip()):
                            replaceString = title[i].text.strip().replace('NEW', '').strip();
                        else:
                            replaceString = title[i].text.strip();

                        if(fnCompareTitle(commonConstant_NAME.SONGPA_NAME, replaceString) == 1):
                            break;
                        else:
                            changeText= str(registrationdate[i].text.replace('.','-'));
                            firebase_con.updateModel(commonConstant_NAME.SONGPA_NAME,numberCnt,
                                datasModel.toJson(
                                    "https://www.songpa.go.kr/www{}".format(link[i].attrs.get('href').replace('.','',1)),
                                    numberCnt,
                                    "",
                                    replaceString,
                                    "",
                                    fnChnagetype(changeText.strip()),
                                    "송파구청",
                                )
                            );
            else : 
                print(response.status_code)
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
            raise ValueError("Argument에 잘못된 값이 전달되었습니다.")