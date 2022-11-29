import re
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
import common.common_fnc  as com

class Youngsan:
    def mainCra(cnt, numberCnt):
        cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.YOUNGSAN_NAME);
        maxCntNumber = max(cntNumber);

        url = 'https://www.ysac.or.kr/page/sub07_01.jsp';
        soupData = com.pageconnect(cnt, url, "javascript:fnListMove({});".format(cnt));

        link = soupData.select('.aleft');
        title = soupData.select('.aleft');
        registrationdate = soupData.select('tr > td:nth-child(4)');
        noticeCheckValue = soupData.select('tr > td:nth-child(1)');
        
        linkCount = len(link);

        for i in range(len(link)):
            numberCnt += 1;

            if linkCount == i:
                cnt += 1;
                print(commonConstant_NAME.YOUNGSAN_NAME,"Next Page : {}".format(cnt));
                return Youngsan.mainCra(cnt,numberCnt),
            else:
                # if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT:
                #     break;

                if(fnCompareTitle(commonConstant_NAME.SEODAEMUN_NAME, title[i].text.strip()) == 1):
                    break;

                linkAttr = link[i].attrs.get('onclick');


                if(noticeCheckValue[i].text.strip() != ''):
                    if linkAttr != None:
                        pass;
                    else:
                        # linkSub = linkAttr.split("(")[1];
                        # linkSubNt = linkSub.split(")")[0];
                        # linkSubts = linkSubNt.split(",");
                        changeText = registrationdate[i].text.strip().replace('.','-');

                        # maxCntNumber += 1;
                        # firebase_con.updateModel( commonConstant_NAME.YOUNGSAN_NAME,maxCntNumber,
                        #     datasModel.toJson(
                        #         # "https://www.sba.seoul.kr{}".format(linkSubts[0].replace('"','')),
                        #         'https://www.sdm.go.kr/news/news/notice.do',
                        #         maxCntNumber,
                        #         "",
                        #         title[i].text.strip(),
                        #         "",
                        #         fnChnagetype(changeText.strip()),
                        #         "용산문화원"
                        #     )
                        # )