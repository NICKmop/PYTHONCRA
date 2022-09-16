import re
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
import common.common_fnc  as com

class Gwanak_notice:
    def mainCra(cnt,numberCnt):
        url = 'https://www.gwanak.go.kr/site/gwanak/ex/bbs/List.do?cbIdx=239';
        soupData = com.pageconnect(cnt, url, "javascript:doBbsFPag({});return false;".format(cnt));
        
        link = soupData.select('tr > td > a');
        title = soupData.select('tr > td > a');
        registrationdate = soupData.select('tr > td:nth-child(5)');

        # print("registrationdate : ", registrationdate);

        linkCount = len(link) - 1;

        for i in range(len(link)):
            numberCnt += 1;
            if linkCount == i:
                # javascript:pageNum('frm01','200');
                cnt += 1;
                print("Gwanak_notice Next Page : {}".format(cnt));
                return Gwanak_notice.mainCra(cnt, numberCnt),
            else:
                if numberCnt == commonConstant_NAME.STOPCUOUNT:
                    break;
            # linkSp = re.sub(r'[^0-9]','',link[i + 1].attrs.get('onclick'));
            linkAttr = link[i].attrs.get('onclick');
            # print(linkAttr);
            
            linkSub = linkAttr.split("(")[1];
            linkSubNt = linkSub.split(")")[0];

            linkSubts = linkSubNt.split(",");
            
            firebase_con.updateModel( commonConstant_NAME.GWANAK_BOROUGH_NOTICE,numberCnt,
                datasModel.toJson(
                    "https://www.gwanak.go.kr/site/gwanak/ex/bbs/View.do?cbIdx={}&bcIdx={}&parentSeq={}".format(linkSubts[0].replace("'", ""), linkSubts[1].replace("'", ""), linkSubts[1].replace("'", "")),
                    numberCnt,
                    "",
                    title[i].text.strip(),
                    "",
                    registrationdate[i].text,
                    "관악구_공지사항"
                )
            )
            