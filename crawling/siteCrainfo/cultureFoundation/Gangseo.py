import requests
from bs4 import BeautifulSoup
from common.common_fnc import fnCompareTitle
from common.common_fnc import fnChnagetype
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from common.common_fnc import pageClickEvent
from common.common_fnc import pageconnectLoadUrl
from models.datasModel import datasModel

class Gangseo:
    def mainCra(numberCnt):
        try:
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.GANGSEO_NAME);
            maxCntNumber = max(cntNumber);

            url = 'https://kcc2000.modoo.at/?link=2glkcxv4'
            soup = BeautifulSoup(pageconnectLoadUrl(url), 'html.parser');
            
            # 타이틀 ,기관, 링크, 등록일, 번호
            title = soup.select('.tit');
            link = soup.select('span[data-message-no]')
            registrationdate = soup.select('.info > .date');

            linkCount = len(link) - 1;
            for i in range(len(link)):
                numberCnt += 1;

                if linkCount == i:
                    print("GANGSEO_NAME Next Page");
                else:
                    # if numberCnt == commonConstant_NAME.STOPCUOUNT + 1:
                    #     break;
                    changeText = str(registrationdate[i].text.replace('.','-'));
                    if(fnCompareTitle(commonConstant_NAME.GANGSEO_NAME, title[i].text.strip(), changeText) == 1):
                        break;
                    else:
                        maxCntNumber += 1;
                        if('새글' in title[i].text.strip()):
                            replaceString = title[i].text.strip().replace('새글', '').strip();
                        else:
                            replaceString = title[i].text.strip();
                            
                        if('시간 전' not in registrationdate[i].text):
                            print(" True : {}".format(registrationdate[i].text));

                            firebase_con.updateModel(commonConstant_NAME.GANGSEO_NAME,maxCntNumber,
                                datasModel.toJson(
                                    "https://kcc2000.modoo.at/?link=2glkcxv4&messageNo={}&mode=view&query=&queryType=0&myList=0&page=1".format(link[i].attrs.get('data-message-no')),
                                    maxCntNumber,
                                    # numberCnt,
                                    "",
                                    replaceString,
                                    "",
                                    fnChnagetype(changeText.strip()),
                                    "강서문화원",
                                )
                            );
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
            raise ValueError("Argument에 잘못된 값이 전달되었습니다.")
                    