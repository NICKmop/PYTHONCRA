import re
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
import common.common_fnc  as com

class Gangnam_Institutions:
    def mainCra(cnt,numberCnt):
        url = 'https://www.gangnam.go.kr/board/B_000046/list.do?mid=ID05_0410';
        soupData = com.pageconnect(cnt, url, "selectPage_func({})".format(cnt));
        
        link = soupData.select('.grid-item > td > a');
        title = soupData.select('.grid-item > td > a');
        registrationdate = soupData.select('.grid-item > td:nth-child(5)');

        # print("link : ", link);

        linkCount = len(link) - 1;
        for i in range(len(link)):
            numberCnt += 1;
            if linkCount == i:
                # javascript:pageNum('frm01','200');
                cnt += 1;
                print("Gangnam_Institutions Next Page : {}".format(cnt));
                return Gangnam_Institutions.mainCra(cnt, numberCnt),
            else:
                if numberCnt == commonConstant_NAME.STOPCUOUNT:
                    break;
            linkSp = link[i].attrs.get('href');
           
            firebase_con.updateModel( commonConstant_NAME.GANGNAM_BOROUGH_OTHER_INSTITUTIONS,numberCnt,
                datasModel.toJson(
                    "https://www.gangnam.go.kr{}".format(linkSp),
                    numberCnt,
                    "",
                    title[i].text.strip(),
                    "",
                    registrationdate[i].text,
                    "강남구_타기관공시송달"
                )
            )
            