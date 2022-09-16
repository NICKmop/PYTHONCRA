import re
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
import common.common_fnc  as com

class Nowon_notice:
    def mainCra(cnt,numberCnt):
        url = 'https://www.nowon.kr/www/user/bbs/BD_selectBbsList.do?q_bbsCode=1001&q_estnColumn1=11';
        soupData = com.pageconnect(cnt, url, "opMovePage({});return false;".format(cnt));
        
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
                print("Nowon_notice Next Page : {}".format(cnt));
                return Nowon_notice.mainCra(cnt, numberCnt),
            else:
                if numberCnt == commonConstant_NAME.STOPCUOUNT:
                    break;
            # linkSp = re.sub(r'[^0-9]','',link[i + 1].attrs.get('onclick'));
            linkAttr = link[i].attrs.get('onclick');
            # print(linkAttr);
            
            linkSub = linkAttr.split("(")[1];
            linkSubNt = linkSub.split(")")[0];
            linkSubts = linkSubNt.split(",");
            
            linkresult = [];
            for i in range(len(linkSubts)):
                linkSubtsrep = linkSubts[i].replace("'", '')
                linkresult.append(linkSubtsrep);
                
            # print(linkresult[0]);
            # print(linkresult[1]);

            firebase_con.updateModel( commonConstant_NAME.GWANAK_BOROUGH_NOTICE,numberCnt,
                datasModel.toJson(
                    "https://www.gwanak.go.kr/site/gwanak/ex/bbs/View.do?cbIdx={}&bcIdx={}&parentSeq={}".format(linkresult[0], linkresult[1], linkresult[1]),
                    numberCnt,
                    "",
                    title[i].text.strip(),
                    "",
                    registrationdate[i].text,
                    "노원구_공지사항"
                )
            )
            