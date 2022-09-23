import re
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
import common.common_fnc  as com

class Jongro_notice:
    def mainCra(cnt,numberCnt):
        url = 'https://www.jongno.go.kr/portal/bbs/selectBoardList.do?bbsId=BBSMSTR_000000000201&menuNo=1752&menuId=1752';
        soupData = com.pageconnect(cnt, url, "javascript:pageMove({});".format(cnt));
        
        link = soupData.select('.sj > a');
        title = soupData.select('.sj > a');
        registrationdate = soupData.select('tr > td:nth-child(4)');

        linkCount = len(link) - 1;

        for i in range(len(link)):
            numberCnt += 1;
            if linkCount == i:
                cnt += 1;
                print("Jongro_notice Next Page : {}".format(cnt));
                return Jongro_notice.mainCra(cnt, numberCnt),
            else:
                if numberCnt == commonConstant_NAME.STOPCUOUNT:
                    break; 
            # linkSp = re.sub(r'[^0-9]','',link[i + 1].attrs.get('onclick'));
            linkAttr = link[i].attrs.get('href');
            linkSub = linkAttr.split("('")[1];
            linkSubNt = linkSub.split("')")[0];
            print(linkSubNt);
            # linkSubts = linkSubNt.split(",");
            
            firebase_con.updateModel( commonConstant_NAME.JONGRO_BOROUGH_NOTICE,numberCnt,
                datasModel.toJson(
                    "https://www.jongno.go.kr/portal/bbs/selectBoardArticle.do?bbsId=BBSMSTR_000000000201&menuNo=1752&menuId=1752&nttId={}".format(linkSubNt),
                    numberCnt,
                    "",
                    title[i].text.strip(),
                    "",
                    registrationdate[i].text,
                    "종로구_공지사항"
                )
            )
            