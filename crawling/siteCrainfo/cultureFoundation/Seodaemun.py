import re
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
import common.common_fnc  as com

class Seodaemun:
    def mainCra(cnt, numberCnt):
        try:
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.SEODAEMUN_NAME);
            maxCntNumber = max(cntNumber);

            url = 'https://www.sdm.go.kr/news/news/notice.do';
            soupData = com.pageconnect(cnt, url, "javascript:goPage({})".format(cnt));
            
            link = soupData.select('.aleft');
            title = soupData.select('.aleft');
            registrationdate = soupData.select('tr > td:nth-child(4)');
            noticeCheckValue = soupData.select('tr > td:nth-child(1)');
            linkCount = len(link);

            for i in range(len(link)):
                numberCnt += 1;

                if linkCount == i:
                    cnt += 1;
                    print(commonConstant_NAME.SEODAEMUN_NAME,"Next Page : {}".format(cnt));
                    # return Seodaemun.mainCra(cnt,numberCnt),
                else:
                    # if numberCnt == 2:
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
                            maxCntNumber += 1;
                            firebase_con.updateModel( commonConstant_NAME.SEODAEMUN_NAME,maxCntNumber,
                                datasModel.toJson(
                                    # "https://www.sba.seoul.kr{}".format(linkSubts[0].replace('"','')),
                                    'https://www.sdm.go.kr/news/news/notice.do',
                                    maxCntNumber,
                                    "",
                                    title[i].text.strip(),
                                    "",
                                    fnChnagetype(changeText.strip()),
                                    "서대문공단"
                                )
                            )
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
            raise ValueError("Argument에 잘못된 값이 전달되었습니다.")