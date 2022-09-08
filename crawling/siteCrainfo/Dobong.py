import re
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
import common.common_fnc  as com

class Dobong:
    def mainCra(cnt,numberCnt):
        url = 'http://www.dbfac.or.kr/front/board/boardContentsListPage.do?board_id=1';
        soupData = com.pageconnect(cnt, url, "javascript:go_Page({})".format(cnt));
        
        link = soupData.select('tr');
        # title = soupData.select('.title > a');
        # registrationdate = soupData.select('.title > .mVer > p:nth-child(2)');

        print("link : ", link);
        # # print("registrationdate : ", registrationdate);

        # linkCount = len(link) - 1;
        # for i in range(len(link)):
        #     numberCnt += 1;
        #     if linkCount == i:
        #         # javascript:pageNum('frm01','200');
        #         cnt += 1;
        #         print("Geuamcheoun Next Page : {}".format(cnt));
        #         return Geuamcheoun.mainCra(cnt, numberCnt),
        #     else:
        #         if numberCnt == commonConstant_NAME.STOPCUOUNT:
        #             break;
        #     linkSp = re.sub(r'[^0-9]','',link[i + 1].attrs.get('onclick'));
        #     # print(title[i].text.strip());
        #     print(registrationdate[i].text);

        #     firebase_con.updateModel( commonConstant_NAME.D,i,
        #         datasModel.toJson(
        #             "https://gcfac.or.kr/board/freeDetail?notice_gb=&board_seq={}&gcfac_menu_cd=&currRow=1&scType=all&srch_input=".format(linkSp),
        #             i,
        #             "",
        #             title[i].text.strip(),
        #             "",
        #             registrationdate[i].text,
        #             "도봉문화재단"
        #         )
        #     )