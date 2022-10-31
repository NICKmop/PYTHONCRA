import re
from common.common_fnc import fnChnagetype
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
import common.common_fnc  as com

class Jongro_notice:
    def mainCra(cnt):
        cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.JONGRO_NAME);
        numberCnt = max(cntNumber);

        url = 'https://www.jongno.go.kr/portal/bbs/selectBoardList.do?bbsId=BBSMSTR_000000000201&menuNo=1752&menuId=1752';
        soupData = com.pageconnect(cnt, url, "javascript:pageMove({});".format(cnt));
        
        link = soupData.select('.sj > a');
        title = soupData.select('.sj > a');
        registrationdate = soupData.select('.date1');

        linkCount = len(link) - 1;

        for i in range(len(link)):
            numberCnt += 1;
            if linkCount == i:
                cnt += 1;
                print("Jongro_notice Next Page : {}".format(cnt));
                return Jongro_notice.mainCra(cnt),
            else:
                if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT:
                    break; 

            linkAttr = link[i].attrs.get('href');
            linkSub = linkAttr.split("('")[1];
            linkSubNt = linkSub.split("')")[0];

            replregistY = registrationdate[i].text.replace("년",'-');
            replregistM = replregistY.replace("월",'-');
            replregistD = replregistM.replace("일",'');
            
            changeText= str(replregistD.strip());

            firebase_con.updateModel( commonConstant_NAME.JONGRO_NAME,numberCnt,
                datasModel.toJson(
                    "https://www.jongno.go.kr/portal/bbs/selectBoardArticle.do?bbsId=BBSMSTR_000000000201&menuNo=1752&menuId=1752&nttId={}".format(linkSubNt),
                    numberCnt,
                    "",
                    title[i].text.strip(),
                    "",
                    fnChnagetype(changeText.strip()),
                    "종로구청"
                )
            )
            