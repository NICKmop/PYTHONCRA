import requests
from bs4 import BeautifulSoup
from common.common_fnc import fnCompareTitle
from common.common_fnc import fnChnagetype
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel

class Jungnang:
    def mainCra(cnt,numberCnt):
        try:
            requests.packages.urllib3.disable_warnings()
            requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.JUNGNANG_NAME);
            maxCntNumber = max(cntNumber);

            url = 'https://www.jnfac.or.kr/mbbs/index.php?board_id=bbs02&cate=&find=&search=&ltype=&page=2&page={}'.format(cnt);
            
            response = requests.get(url);
            if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
                html = response.text;
                soup = BeautifulSoup(html, 'html.parser');

                # 타이틀 ,기관, 링크, 등록일, 번호
                link = soup.select('.subject');
                title = soup.select('.subject');
                registrationdate = soup.select('td:nth-child(4)');
                checkValue = soup.select('td:nth-child(1)');

                linkCount = len(link) - 1;
                for i in range(len(link)):
                    changeText= str(registrationdate[i].text);
                    numberCnt += 1;

                    if linkCount == i:
                        cnt += 1;
                        firebase_con.updateModel(commonConstant_NAME.JUNGNANG_NAME,numberCnt,
                            datasModel.toJson(
                                'https://www.jnfac.or.kr/{}'.format(link[i].attrs.get('href')),
                                numberCnt,
                                "",
                                title[i].text.strip(),
                                "",
                                fnChnagetype(changeText.strip()),
                                "중랑문화재단",
                            )
                        )

                        print("Jungnang Next Page : {}".format(cnt));
                        return Jungnang.mainCra(cnt, numberCnt);
                    else:
                        if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT:
                            break;  

                        if(fnCompareTitle(commonConstant_NAME.JUNGNANG_NAME, title[i].text.strip()) == 1):
                            break;
                        else:
                            maxCntNumber += 1;
                            firebase_con.updateModel(commonConstant_NAME.JUNGNANG_NAME,maxCntNumber,
                                datasModel.toJson(
                                    'https://www.jnfac.or.kr/{}'.format(link[i].attrs.get('href')),
                                    maxCntNumber,
                                    "",
                                    title[i].text.strip(),
                                    "",
                                    fnChnagetype(changeText.strip()),
                                    "중랑문화재단",
                                )
                            )
                else:
                    print(response.status_code);
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
            raise ValueError("Argument에 잘못된 값이 전달되었습니다.")