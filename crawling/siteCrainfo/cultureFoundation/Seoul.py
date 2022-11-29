import re
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
import common.common_fnc  as com

class Seoul:
    def mainCra(cnt,numberCnt):
        url = 'https://www.sfac.or.kr/opensquare/notice/notice_list.do';
        soupData = com.pageconnect(cnt, url, "javascript:doBbsFPag({});return false;".format(cnt));
        print(soupData);
        link = soupData.select('.cell');
        title = soupData.select('.cell');
        registrationdate = soupData.select('td:nth-child(3)');

        print("link : {}".format(link));
        print("title : {}".format(title));
        print("registrationdate : {}".format(registrationdate));

        linkCount = len(link) - 1;

        for i in range(len(link)):
            numberCnt += 1;
            if linkCount == i:
                cnt += 1;
                print("Seoul Next Page : {}".format(cnt));
                return Seoul.mainCra(cnt, numberCnt),
            else:
                if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT:
                    break;

            # firebase_con.updateModel( commonConstant_NAME.SEOUL_NAME,numberCnt,
            #     datasModel.toJson(
            #         "https://www.sfac.or.kr/artspace/artspace/play_notice.do?cbIdx={}&bcIdx={}&type=".format(linkSp,),
            #         numberCnt,
            #         "",
            #         title[i].text.strip(),
            #         "",
            #         registrationdate[i].text,
            #         "서울문화재단"
            #     )
            # )