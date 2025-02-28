import re
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
import common.common_fnc  as com

class Nowon_notice:
    def mainCra(cnt):
        try:
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.NOWON_NAME);
            numberCnt = max(cntNumber);

            url = 'https://www.nowon.kr/www/user/bbs/BD_selectBbsList.do?q_bbsCode=1001&q_estnColumn1=11';
            soupData = com.pageconnect(cnt, url, "opMovePage({});return false;".format(cnt));
            
            link = soupData.select('.cell-subject > a');
            title = soupData.select('.cell-subject > a');
            registrationdate = soupData.select('tr > td:nth-child(4)');

            linkCount = len(link) - 1;

            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print("Nowon_notice Next Page : {}".format(cnt));
                    return Nowon_notice.mainCra(cnt),
                else:
                    # if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT:
                    #     break; 
                    linkAttr = link[i].attrs.get('onclick');
                    linkSub = linkAttr.split("('")[1];
                    linkSubNt = linkSub.split("')")[0];

                    changeText= str(registrationdate[i].text);
                    
                    if(fnCompareTitle(commonConstant_NAME.NOWON_NAME, title[i].text.strip(), changeText) == 1):
                        break;
                    else:
                        firebase_con.updateModel( commonConstant_NAME.NOWON_NAME,numberCnt,
                            datasModel.toJson(
                                "https://www.nowon.kr/www/user/bbs/BD_selectBbs.do?q_bbsCode=1001&q_bbscttSn={}&q_estnColumn1=11&q_rowPerPage=10&q_currPage={}&q_sortName=&q_sortOrder=&q_searchKeyTy=sj___1002&q_searchVal=&".format(linkSubNt,cnt),
                                numberCnt,
                                "",
                                title[i].text.strip(),
                                "",
                                fnChnagetype(changeText.strip()),
                                "노원구청"
                            )
                        )
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
            raise ValueError("Argument에 잘못된 값이 전달되었습니다.")
            