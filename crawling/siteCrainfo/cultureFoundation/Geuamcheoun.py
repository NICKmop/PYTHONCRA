import re
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
import common.common_fnc  as com

class Geuamcheoun:
    def mainCra(cnt,numberCnt):
        try:
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.GEUAMCHEOUN_NAME);
            maxCntNumber = max(cntNumber);

            url = 'https://gcfac.or.kr/board/free';
            soupData = com.pageconnect(cnt, url, "javascript:pagingUtil.pageSubmit('{}')".format(cnt));
            
            link = soupData.select('tr');
            title = soupData.select('.title > a');
            registrationdate = soupData.select('.title > .mVer > p:nth-child(2)');

            linkCount = len(link) - 1;
            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    # javascript:pageNum('frm01','200');
                    cnt += 1;
                    print("Geuamcheoun Next Page : {}".format(cnt));
                    return Geuamcheoun.mainCra(cnt, numberCnt),
                else:
                    # if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT:
                    #     break;
                    changeText= str(registrationdate[i].text.split(":")[1].replace(' ', ''));
                        
                    if(fnCompareTitle(commonConstant_NAME.GEUAMCHEOUN_NAME, title[i].text.strip(), changeText) == 1):
                        break;
                    else:
                        maxCntNumber += 1;
                        linkSp = re.sub(r'[^0-9]','',link[i + 1].attrs.get('onclick'));
                        

                        firebase_con.updateModel( commonConstant_NAME.GEUAMCHEOUN_NAME,maxCntNumber,
                            datasModel.toJson(
                                "https://gcfac.or.kr/board/freeDetail?notice_gb=&board_seq={}&gcfac_menu_cd=&currRow=1&scType=all&srch_input=".format(linkSp),
                                maxCntNumber,
                                "",
                                title[i].text.strip(),
                                "",
                                fnChnagetype(changeText.strip()),
                                "금천문화재단"
                            )
                        )
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
            raise ValueError("Argument에 잘못된 값이 전달되었습니다.")    
        