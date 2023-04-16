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

        print(maxCntNumber);
        
        url = 'https://www.ysac.or.kr/page/sub07_01.jsp';
        soupData = com.pageconnect(cnt, url, "javascript:fnListMove({});".format(cnt));

        link = soupData.select('.bd_title > a');
        title = soupData.select('.bd_title > a');
        registrationdate = soupData.select('.bd_date');
        
        linkCount = len(link);

        for i in range(len(link)):
            numberCnt += 1;

            if linkCount == i:
                cnt += 1;
                print(commonConstant_NAME.YOUNGSAN_NAME,"Next Page : {}".format(cnt));
                return Youngsan.mainCra(cnt,numberCnt),
            else:
                # if numberCnt == 22:
                #     break;
                changeText = registrationdate[i].text.strip();
            
                if(fnCompareTitle(commonConstant_NAME.YOUNGSAN_NAME, title[i].text.split(']', 1)[1].strip(), changeText) == 1):
                    break;
                else:
                    linkAttr = link[i].attrs.get('href');
                    linkSub = linkAttr.split("(")[1];
                    linkSubNt = linkSub.split(")")[0];


                    print("{} : {}".format(i, title[i].text));

                    maxCntNumber += 1;
                    firebase_con.updateModel( commonConstant_NAME.YOUNGSAN_NAME,maxCntNumber,
                        datasModel.toJson(
                            "https://ysac.or.kr/page/sub07_01_v.jsp?p_IDX={}".format((linkSubNt.replace("'",''))),
                            maxCntNumber,
                            "",
                            title[i].text.split(']', 1)[1].strip(),
                            "",
                            fnChnagetype(changeText.strip()),
                            "용산문화원"
                        )
                    )