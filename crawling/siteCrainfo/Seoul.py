import re
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
import common.common_fnc  as com

class Seoul:
    def mainCra(cnt,numberCnt):
        url = 'https://www.sfac.or.kr/opensquare/notice/notice_list.do';
        soupData = com.pageconnect(cnt, url, "doBbsFPag({});".format(cnt));
        
        print(soupData);
        # link = soupData.select('.cell');
        # title = soupData.select('.cell');
        # registrationdate = soupData.select('td:nth-child(3)');

        # linkCount = len(link) - 1;
        # for i in range(len(link)):
        #     numberCnt += 1;
        #     if linkCount == i:
        #         # javascript:pageNum('frm01','200');
        #         cnt += 10;
        #         print("Seoul Next Page : {}".format(cnt));
        #         return Seoul.mainCra(cnt, numberCnt),
        #     else:
        #         if numberCnt == commonConstant_NAME.STOPCUOUNT:
        #             break;
        #     linkSp = link[i].attrs.get('onclick');
        #     print(linkSp)
            # linkSp = link[i].attrs.get('onclick').split('Page');
            # linkSub = re.sub(r'[^0-9]','',linkSp[0]);
            
            # print(linkSub);
            # print(title[i].text.strip());
            # print(registrationdate[i].text);

            # firebase_con.updateModel( commonConstant_NAME.SEOUL_NAME,numberCnt,
            #     datasModel.toJson(
            #         "".format(cnt , linkSub),
            #         numberCnt,
            #         "",
            #         title[i].text.strip(),
            #         "",
            #         registrationdate[i].text,
            #         "서울문화재단"
            #     )
            # )