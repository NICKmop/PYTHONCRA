import re
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
import common.common_fnc  as com

class Seodaemun:
    def mainCra(cnt, numberCnt):
        url = 'https://www.sdm.go.kr/news/news/notice.do';
        soupData = com.pageconnect(cnt, url, "javascript:goPage({})".format(cnt));
        
        link = soupData.select('.aleft');
        title = soupData.select('.aleft');
        registrationdate = soupData.select('tr > td:nth-child(4)');

        linkCount = len(link);

        # print(link);
        # print(title);
        # print(registrationdate);
        for i in range(len(link)):
            numberCnt += 1;
            if linkCount == i:
                cnt += 1;
                print(commonConstant_NAME.SEODAEMUN_NAME,"Next Page : {}".format(cnt));
                return Seodaemun.mainCra(cnt,numberCnt),
            else:
                if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT:
                    break;

            linkAttr = link[i].attrs.get('onclick');
            print("origin Link : {}".format(linkAttr));

            if linkAttr == None:
                pass;
            else:
                linkSub = linkAttr.split("(")[1];
                linkSubNt = linkSub.split(")")[0];
                linkSubts = linkSubNt.split(",");

                print("")
                # firebase_con.updateModel( commonConstant_NAME.SEODAEMUN_NAME,numberCnt,
                #     datasModel.toJson(
                #         "https://www.sba.seoul.kr{}".format(linkSubts[0].replace('"','')),
                #         numberCnt,
                #         "",
                #         title[i].text.strip(),
                #         "",
                #         registrationdate[i].text,
                #         "서대문문화재단"
                #     )
                # )
            