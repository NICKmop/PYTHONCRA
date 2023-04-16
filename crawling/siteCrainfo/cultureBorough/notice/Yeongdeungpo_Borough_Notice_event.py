import requests
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Yeongdeungpo_notice_event:
    def mainCra(cnt):
        try:
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.YEONGDEUNGPO_NAME);
            numberCnt = max(cntNumber);

            url = 'https://www.ydp.go.kr/www/selectBbsNttList.do?bbsNo=40&&pageUnit=10&key=2848&pageIndex={}'.format(cnt);
            response = requests.get(url);
            if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
                html = response.text;
                soup = BeautifulSoup(html, 'html.parser')
                # 타이틀 ,기관, 링크, 등록일, 번호
                link = soup.select('.p-subject > a');
                title = soup.select('.p-subject > a');
                registrationdate = soup.select('td:nth-child(4)');
                checkValue = soup.select('td:nth-child(1)');
                linkCount = len(link) - 1;

                for i in range(len(link)):
                    numberCnt += 1;

                    if linkCount == i:
                        cnt += 1;
                        print(commonConstant_NAME.YEONGDEUNGPO_BOROUGH_NOTICE," Next Page : {}".format(cnt));
                        return Yeongdeungpo_notice_event.mainCra(cnt);
                    else:
                        # if numberCnt == commonConstant_NAME.SEOUL_STOP_COUNT_FOUR:
                        #     break;

                        if('NEW' in title[i].text.strip()):
                            replaceString = title[i].text.strip().replace('NEW', '').strip();
                        else:
                            replaceString = title[i].text.strip();
                        changeText= str(registrationdate[i].text.replace('.','-'));

                        if(fnCompareTitle(commonConstant_NAME.YEONGDEUNGPO_NAME, replaceString, changeText) == 1):
                            break;


                        if(checkValue[i].text != '공지'):
                            firebase_con.updateModel(commonConstant_NAME.YEONGDEUNGPO_NAME,numberCnt,
                                datasModel.toJson(
                                    "https://www.ydp.go.kr/www{}".format(link[i].attrs.get('href').replace('.','',1)),
                                    numberCnt,
                                    "",
                                    replaceString,
                                    "",
                                    fnChnagetype(changeText.strip()),
                                    "영등포구청",
                                )
                            );
                            
            else : 
                print(response.status_code)
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
            raise ValueError("Argument에 잘못된 값이 전달되었습니다.")
            