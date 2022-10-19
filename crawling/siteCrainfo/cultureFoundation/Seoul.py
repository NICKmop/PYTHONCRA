import re
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
import common.common_fnc  as com

class Seoul:
    def mainCra(cnt,numberCnt):
        url = 'https://www.sfac.or.kr/opensquare/notice/notice_list.do';
        soupData = com.pageconnect(cnt, url, "doBbsFPag({});return false;".format(cnt));
        
        link = soupData.select('.cell');
        title = soupData.select('.cell');
        registrationdate = soupData.select('pc_cell');

        print("link : {}".format(link));
        print("title : {}".format(title));
        print("registrationdate : {}".format(registrationdate));

        linkCount = len(link) - 1;

        for i in range(len(link)):
            numberCnt += 1;
            if linkCount == i:
                cnt += 10;
                print("Seoul Next Page : {}".format(cnt));
                return Seoul.mainCra(cnt, numberCnt),
            else:
                if numberCnt == commonConstant_NAME.STOPCUOUNT:
                    break;

            # firebase_con.updateModel( commonConstant_NAME.SEOUL_NAME,numberCnt,
            #     datasModel.toJson(
            #         "http://ddmac.or.kr/sub04/sub01.php?type=view&uid={}".format(linkSp),
            #         numberCnt,
            #         "",
            #         title[i].text.strip(),
            #         "",
            #         registrationdate[i].text,
            #         "서울문화재단"
            #     )
            # )