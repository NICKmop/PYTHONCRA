import requests
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Seocho_notice_education:
    def mainCra(cnt):
        try:
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.SEOCHO_NAME);
            numberCnt = max(cntNumber);

            print("numberCnt : {}".format(numberCnt));
            
            url = 'https://www.seocho.go.kr/site/seocho/ex/bbs/List.do?pageIndex={}&cbIdx=60&searchMedia=&bcIdx=375757&searchCondition=subCont&searchKeyword='.format(cnt);
            response = requests.get(url);

            if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
                html = response.text;
                soup = BeautifulSoup(html, 'html.parser')
                # 타이틀 ,기관, 링크, 등록일, 번호
                link = soup.select('.title > a');
                title = soup.select('.title > a');
                registrationdate = soup.select('td:nth-child(4)');

                checknotice = soup.select("tr");

                linkCount = len(link) - 1;
                for i in range(len(link)):
                    if(checknotice[i].attrs.get("class") == None):
                        numberCnt += 1;
                        if linkCount == i:
                            cnt += 1;
                            print(commonConstant_NAME.SEOCHO_BOROUGH_NOTICE_EDUCATION," Next Page : {}".format(cnt));
                            return Seocho_notice_education.mainCra(cnt);
                        else:
                            # print(title[i].text.strip());
                            # print(link[i].attrs.get('href'));
                            # print(registrationdate[i].text.strip());
                            # if numberCnt == 182:
                            #     break;

                            if(fnCompareTitle(commonConstant_NAME.SEOCHO_NAME, title[i].text.strip()) == 1):
                                break;

                            changeText= str(registrationdate[i].text.replace('.','-'));
                            firebase_con.updateModel(commonConstant_NAME.SEOCHO_NAME,numberCnt,
                                datasModel.toJson(
                                    "https://www.seocho.go.kr{}".format(link[i].attrs.get('href')),
                                    numberCnt,
                                    "",
                                    title[i].text.strip(),
                                    "",
                                    fnChnagetype(changeText.strip()),
                                    "서초구청",
                                )
                            );
            else : 
                print(response.status_code);
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
            raise ValueError("Argument에 잘못된 값이 전달되었습니다.")
            