import requests
from bs4 import BeautifulSoup
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel

class Gnagbuk:
    def mainCra(cnt,numberCnt):
        try:
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.GANGBUK_NAME);
            maxCntNumber = max(cntNumber);

            url = 'http://www.gbcf.or.kr/load.asp?subPage=510&searchValue=&searchType=&cate=&page={}&board_md=list'.format(cnt);
            response = requests.get(url);

            if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
                html = response.text;
                soup = BeautifulSoup(html, 'html.parser')
                # 타이틀 ,기관, 링크, 등록일, 번호
                title = soup.select('div.bbs_normal_list > ul > li > div.subject > div.subject_inner > div.subject_box > a');
                link = soup.select('div.bbs_normal_list > ul > li > div.subject > div.subject_inner > div.subject_box > a');
                registrationdate = soup.select('div.bbs_normal_list > ul > li > div.subject > div.subject_inner > span');
                checkValue = soup.select('.no');

                linkCount = len(link) - 1;
                for i in range(len(link)):
                    if linkCount == i:
                        cnt += 1;
                        print("Gnagbuk Next Page : {}".format(cnt));
                        return Gnagbuk.mainCra(cnt, numberCnt);
                    else:
                        # if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT:
                        #     break;
                        changeText= str(registrationdate[i].text.split("/")[0].replace(' ',''));
                        if(checkValue[i].text.strip() != '공지'):
                            numberCnt += 1;
                            if(fnCompareTitle(commonConstant_NAME.GANGBUK_NAME, title[i].text.strip()) == 1):
                                    break;
                            else:
                                if title[i].text.strip() == '':
                                    continue;
                                else:
                                    maxCntNumber += 1;
                                    firebase_con.updateModel(commonConstant_NAME.GANGBUK_NAME,maxCntNumber,
                                        datasModel.toJson(
                                            # https://www.gbcf.or.kr/load.asp?subPage=510.view&cate=&idx=773&searchValue=&searchType=&page=3
                                            # http://www.gbcf.or.kr/load.asp?subPage=510.view&cate=&idx=788&searchValue=&searchType=&page=1
                                            "http://www.gbcf.or.kr/{}".format(link[i].attrs.get('href')),
                                            maxCntNumber,
                                            "",
                                            title[i].text.strip(),
                                            "",
                                            fnChnagetype(changeText.strip()),
                                            "강북문화재단",
                                        )
                                    );
            else : 
                print(response.status_code)
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
            raise ValueError("Argument에 잘못된 값이 전달되었습니다.")