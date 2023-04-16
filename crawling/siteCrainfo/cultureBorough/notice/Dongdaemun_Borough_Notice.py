import requests
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Dongdaemun_notice:
    def mainCra(cnt):
        try:
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.DONGDAEMUN_NAME);
            numberCnt = max(cntNumber);

            url = 'https://www.ddm.go.kr/www/selectBbsNttList.do?key=198&bbsNo=38&searchCtgry=&searchCnd=all&searchKrwd=&integrDeptCode=&pageIndex={}'.format(cnt);
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/605.1.15',
            }
            response = requests.get(url,headers=headers);
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
                        print(commonConstant_NAME.DONGDAEMUN_BOROUGH_NOTICE," Next Page : {}".format(cnt));
                        return Dongdaemun_notice.mainCra(cnt);
                    else:
                        # if numberCnt == commonConstant_NAME.SEOUL_STOP_COUNT_SEVEN:
                        #     break;
                        changeText = str(registrationdate[i].text);
                        if(fnCompareTitle(commonConstant_NAME.DONGDAEMUN_NAME, title[i].text.strip(), changeText) == 1):
                            break;

                        firebase_con.updateModel(commonConstant_NAME.DONGDAEMUN_NAME,numberCnt,
                            datasModel.toJson(
                                "https://www.ddm.go.kr/www{}".format(link[i].attrs.get('href').replace(".","",1)),
                                numberCnt,
                                "",
                                title[i].text.strip(),
                                "",
                                fnChnagetype(changeText.strip()),
                                "동대문구청",
                            )
                        );
            else : 
                print(response.status_code)
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
            raise ValueError("Argument에 잘못된 값이 전달되었습니다.")
            