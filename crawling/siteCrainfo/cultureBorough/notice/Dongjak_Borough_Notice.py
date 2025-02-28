import requests
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Dongjak_notice:
    def mainCra(cnt):
        try:
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.DONGJAK_NAME);
            numberCnt = max(cntNumber);
            
            print("numberCnt : " ,cnt);

            url = 'https://www.dongjak.go.kr/portal/bbs/B0000022/list.do?menuNo=200641&pageIndex={}'.format(cnt);
            # page auth header add
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }

            response = requests.get(url, headers=headers);
            # print("response : " , response.text);
            
            if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
                html = response.text;
                soup = BeautifulSoup(html, 'html.parser')
                # 타이틀 ,기관, 링크, 등록일, 번호
                link = soup.select('.title > a');
                title = soup.select('.title > a');
                registrationdate = soup.select('td:nth-child(4)');

                # print(registrationdate);
                linkCount = len(link) - 1;

                for i in range(len(link)):
                    numberCnt += 1;
                    if linkCount == i:
                        cnt += 1;
                        print(commonConstant_NAME.DONGJAK_BOROUGH_NOTICE," Next Page : {}".format(cnt));
                        return Dongjak_notice.mainCra(cnt);
                    else:
                        changeText = str(registrationdate[i].text);
                        # if numberCnt == commonConstant_NAME.SEOUL_STOP_COUNT_FOUR:
                        #     break;
                        
                        if(fnCompareTitle(commonConstant_NAME.DONGJAK_NAME, title[i].text.strip(), changeText) == 1):
                            break;

                        # print("linkK:::: ", link[i].attrs.get('href'));
                        firebase_con.updateModel(commonConstant_NAME.DONGJAK_NAME,numberCnt,
                            datasModel.toJson(
                                "https://www.dongjak.go.kr{}".format(link[i].attrs.get('href')),
                                numberCnt,
                                "",
                                title[i].text.strip(),
                                "",
                                fnChnagetype(changeText.strip()),
                                "동작구청",
                            )
                        );
            else : 
                print("statusCode : " , response.status_code)
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
            raise ValueError("Argument에 잘못된 값이 전달되었습니다.")
            