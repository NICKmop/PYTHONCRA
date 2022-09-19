import re
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
import common.common_fnc  as com

class Seodaemungu_notice:
    def mainCra(cnt,numberCnt):
        url = 'https://www.sdm.go.kr/news/news/notice.do';
        soupData = com.pageconnect(cnt, url, "javascript:goPage({})".format(cnt));
        
        link = soupData.select('.aleft > a');
        title = soupData.select('.aleft > a');
        registrationdate = soupData.select('tr > td:nth-child(4)');

        linkCount = len(link) - 1;

        for i in range(len(link)):
            numberCnt += 1;
            if linkCount == i:
                cnt += 1;
                print("Seodaemungu_notice Next Page : {}".format(cnt));
                return Seodaemungu_notice.mainCra(cnt, numberCnt),
            else:
                if numberCnt == commonConstant_NAME.STOPCUOUNT:
                    break; 
            # linkSp = re.sub(r'[^0-9]','',link[i + 1].attrs.get('onclick'));
            linkAttr = link[i].attrs.get('onclick');
            # linkSubts = linkSubNt.split(",");
            
            firebase_con.updateModel( commonConstant_NAME.SEODAEMUNGU_NOTICE,numberCnt,
                datasModel.toJson(
                    # "".format(linkSubNt,cnt),
                    numberCnt,
                    "",
                    title[i].text.strip(),
                    "",
                    registrationdate[i].text,
                    "서대문구_공지사항"
                )
            )
            