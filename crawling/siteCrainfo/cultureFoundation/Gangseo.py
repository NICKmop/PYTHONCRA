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
                if(fnCompareTitle(commonConstant_NAME.GANGSEO_NAME, title[i].text.strip()) == 1):
                    break;
                else:
                    maxCntNumber += 1;
                    changeText = str(registrationdate[i].text.replace('.','-'));

                    firebase_con.updateModel(commonConstant_NAME.GANGSEO_NAME,maxCntNumber,
                        datasModel.toJson(
                            "https://kcc2000.modoo.at/?link=2glkcxv4&messageNo={}&mode=view&query=&queryType=0&myList=0&page=1".format(link[i].attrs.get('data-message-no')),
                            maxCntNumber,
                            "",
                            title[i].text.strip(),
                            "",
                            fnChnagetype(changeText.strip()),
                            "강서문화원",
                        )
                    );