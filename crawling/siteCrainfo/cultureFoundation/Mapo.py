import re
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
import common.common_fnc  as com

# 보류
class Mapo:
    def mainCra(cnt,numberCnt):
        cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.MAPO_NAME);
        maxCntNumber = max(cntNumber);

        url = 'https://www.mfac.or.kr/communication/notice_all_list.jsp';
        soupData = com.pageconnect(cnt, url, "javascript:submitPage({})".format(cnt));
        
        link = soupData.select('.tit > a');
        title = soupData.select('.btnDetail');
        registrationdate = soupData.select('.date');

        linkCount = len(link) - 1;
        for i in range(len(link)):
            numberCnt += 1;
            if linkCount == i:
                # javascript:pageNum('frm01','200');
                cnt += 10;
                print("Mapo Next Page : {}".format(cnt));
                return Mapo.mainCra(cnt, numberCnt),
            else:
                # if numberCnt == commonConstant_NAME.STOPCUOUNT:
                #     break;

                linkSp = link[i].attrs.get('seq');
                if(registrationdate[i].text != '작성일'):
                    changeText= str(registrationdate[i].text);

                    if(fnCompareTitle(commonConstant_NAME.MAPO_NAME, title[i].text.strip()) == 1):
                        break;
                    else:
                        maxCntNumber += 1;
                        firebase_con.updateModel( commonConstant_NAME.MAPO_NAME,maxCntNumber,
                            datasModel.toJson(
                                "https://www.mfac.or.kr/communication/notice_all_view.jsp?sc_b_code=BOARD_1207683401&sc_type=1&pk_seq={}&sc_cond=b_subject&page=1".format(linkSp),
                                maxCntNumber,
                                "",
                                title[i].text.strip(),
                                "",
                                fnChnagetype(changeText.strip()),
                                "마포문화재단"
                            )
                        )