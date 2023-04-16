import requests
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Mapo_notice_event:
    def mainCra(cnt):
        try:
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.MAPO_NAME);
            numberCnt = max(cntNumber);

            print("numberCnt = {}".format(numberCnt));

            url = 'https://www.mapo.go.kr/site/main/board/culturevent/list?cp={}&sortOrder=BA_REGDATE&sortDirection=DESC&listType=list&bcId=culturevent&baNotice=false&baCommSelec=false&baOpenDay=false&baUse=true'.format(cnt);
            response = requests.get(url);
            if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
                html = response.text;
                soup = BeautifulSoup(html, 'html.parser')
                # 타이틀 ,기관, 링크, 등록일, 번호
                checkValue = soup.select('td:nth-child(1)');
                link = soup.select('.tal_l_i > a');
                title = soup.select('.tal_l_i > a');
                registrationdate = soup.select('td:nth-child(4)');

                linkCount = len(link) - 1;
                for i in range(len(link)):
                    numberCnt += 1;
                    if linkCount == i:
                        cnt += 1;
                        print(commonConstant_NAME.MAPO_BOROUGH_NOTICE_EVENT," Next Page : {}".format(cnt));
                        return Mapo_notice_event.mainCra(cnt);
                    else:
                        # if numberCnt == 292:
                        #     break;
                        # print(title[i].text.strip());
                        # # print(link[i].attrs.get('href'));
                        changeText = str(registrationdate[i].text.split(' ')[0]);

                        if(fnCompareTitle(commonConstant_NAME.MAPO_NAME, title[i].text.strip(), changeText) == 1):
                            break;

                        if(title[i].text.strip() == ''):
                            numberCnt -= 1;

                        if(checkValue[i].text.strip() != ''):
                            firebase_con.updateModel(commonConstant_NAME.MAPO_NAME,numberCnt,
                                datasModel.toJson(
                                    "https://www.mapo.go.kr{}".format(link[i].attrs.get('href').replace('.','',1)),
                                    numberCnt,
                                    "",
                                    title[i].text.strip(),
                                    "",
                                    fnChnagetype(changeText.strip()),
                                    "마포구청",
                                )
                            );
            else : 
                print(response.status_code)
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
            raise ValueError("Argument에 잘못된 값이 전달되었습니다.")
            