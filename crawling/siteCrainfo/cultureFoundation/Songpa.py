import re
from common.common_fnc import fnCompareTitle
from common.common_fnc import fnChnagetype
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
import common.common_fnc  as com

class Songpa:
    def mainCra(cnt,numberCnt):
        cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.SONGPA_NAME);
        maxCntNumber = max(cntNumber);

        url = 'https://www.songpafac.or.kr/notice_list.do';
        soupData = com.pageconnect(cnt, url, "fn_paging('{}')".format(cnt));
        
        link = soupData.select('tr > .title > a');
        title = soupData.select('tr > .title > a');
        registrationdate = soupData.select('td:nth-child(3)');

        linkCount = len(link) - 1;
        for i in range(len(link)):
            numberCnt += 1;
            if linkCount == i:
                # javascript:pageNum('frm01','200');
                cnt += 10;
                print("Songpa Next Page : {}".format(cnt));
                return Songpa.mainCra(cnt, numberCnt),
            else:
                # if numberCnt == commonConstant_NAME.STOPCUOUNT:
                #     break;
                if(fnCompareTitle(commonConstant_NAME.SONGPA_NAME, title[i].text.strip()) == 1):
                    break;
                else:
                    maxCntNumber += 1;
                    linkSp = link[i].attrs.get('href').split('Page');
                    linkSub = re.sub(r'[^0-9]','',linkSp[0]);
                    
                    changeText= str(registrationdate[i].text);
                    firebase_con.updateModel( commonConstant_NAME.SONGPA_NAME,maxCntNumber,
                        datasModel.toJson(
                            "https://www.songpafac.or.kr/notice_view.do?brd_seq={}&curPage=&searchtype=&keyword=".format(cnt , linkSub),
                            maxCntNumber,
                            "",
                            title[i].text.strip(),
                            "",
                            fnChnagetype(changeText.strip()),
                            "송파문화재단"
                        )
                    )