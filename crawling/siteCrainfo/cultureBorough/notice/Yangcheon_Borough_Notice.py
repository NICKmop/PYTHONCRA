import re
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
import common.common_fnc  as com

class Yangcheon_notice:
    def mainCra(cnt):
        cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.YANGCHEON_NAME);
        numberCnt = max(cntNumber);

        url = 'https://www.yangcheon.go.kr/site/yangcheon/ex/bbs/List.do;jsessionid=hQBUNSnObUA1jLlEVux1s4J1SNRDwXu7lZ6YkRLvSztrEKuMbLgVDg7w93anM7oK.YCWEB_servlet_engine3?cbIdx=254#'.format(cnt);
        soupData = com.pageconnect(cnt, url, "doBbsFPag({});return false;".format(cnt));
        # 타이틀 ,기관, 링크, 등록일, 번호
        
        link = soupData.select('.subject > a');
        title = soupData.select('.subject > a');
        registrationdate = soupData.select('tr > td:nth-child(5)');

        linkCount = len(link) - 1;
        for i in range(len(link)):
            numberCnt += 1;
            if linkCount == i:
                cnt += 1;
                print(commonConstant_NAME.YANGCHEON_BOROUGH_NOTICE," Next Page : {}".format(cnt));
                return Yangcheon_notice.mainCra(cnt);
            else:
                # if numberCnt == commonConstant_NAME.SEOUL_STOP_COUNT_FOUR:
                #     break;
                if(fnCompareTitle(commonConstant_NAME.YANGCHEON_NAME, title[i].text.strip()) == 1):
                    break;
                linkAttr = link[i].attrs.get('onclick')
                linkSub = linkAttr.split("(")[1];
                linkSubNt = linkSub.split(")")[0];

                linkSubts = linkSubNt.split(",");
                changeText= str(registrationdate[i].text.replace('.','-'));

                firebase_con.updateModel(commonConstant_NAME.YANGCHEON_NAME,numberCnt,
                    datasModel.toJson(
                        "https://www.yangcheon.go.kr/site/yangcheon/ex/bbs/View.do?cbIdx={}&bcIdx={}&parentSeq={}".format(linkSubts[0].replace("'",""), linkSubts[1].replace("'",""), linkSubts[1].replace("'","")),
                        numberCnt,
                        "",
                        title[i].text.strip(),
                        "",
                        fnChnagetype(changeText.strip()),
                        "양천구청",
                    )
                );
            