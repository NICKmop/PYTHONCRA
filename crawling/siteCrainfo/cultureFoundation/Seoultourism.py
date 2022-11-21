import re
from common.common_fnc import fnCompareTitle
from common.common_fnc import fnChnagetype
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
import common.common_fnc  as com

class Seoultourism:
    def mainCra(cnt):
        cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.SEOUL_NAME);
        numberCnt = max(cntNumber);

        url = 'https://www.seoul.go.kr/realmnews/in/list.do';
        soupData = com.pageconnect(cnt, url, "javascript:fnPagingMove({});".format(cnt));
        
        link = soupData.select('.item > a');
        title = soupData.select('.tbx > .subject');
        registrationdate = soupData.select('.tbx > .date');

        linkCount = len(link) - 1;

        for i in range(len(link)):
            numberCnt += 1;
            changeText= str(registrationdate[i].text.split(' ')[0]);
            if linkCount == i:
                cnt += 1;

                firebase_con.updateModel( commonConstant_NAME.SEOUL_NAME,numberCnt,
                datasModel.toJson(
                    link[i].attrs.get('href'),
                    numberCnt,
                    "",
                    title[i].text.strip(),
                    "",
                    fnChnagetype(changeText.strip()),
                    "서울관광재단"
                    )
                )
                print("Seoultourism Next Page : {}".format(cnt));
                return Seoultourism.mainCra(cnt),
            else:
                # if numberCnt == commonConstant_NAME.SEOUL_STOP_COUNT_EIGHT:
                #     break;
                
                if(fnCompareTitle(commonConstant_NAME.SEOUL_NAME, title[i].text.strip()) == 1):
                    break;

                firebase_con.updateModel( commonConstant_NAME.SEOUL_NAME,numberCnt,
                    datasModel.toJson(
                        link[i].attrs.get('href'),
                        numberCnt,
                        "",
                        title[i].text.strip(),
                        "",
                        fnChnagetype(changeText.strip()),
                        "서울관광재단"
                    )
                )