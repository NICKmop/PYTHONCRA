import re
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
import common.common_fnc  as com

class Gangnam_notice:
    def mainCra(cnt):
        try:
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.GANGNAM_NAME);
            numberCnt = max(cntNumber);

            url = 'https://www.gangnam.go.kr/board/B_000001/list.do?mid=ID05_040101';
            soupData = com.pageconnect(cnt, url, "selectPage_func({})".format(cnt));
            
            link = soupData.select('.grid-item > td > a');
            title = soupData.select('.grid-item > td > a');
            registrationdate = soupData.select('.grid-item > td:nth-child(5)');

            print("firebases Nct : {}".format(cnt));

            linkCount = len(link) - 1;
            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    # javascript:pageNum('frm01','200');
                    cnt += 1;
                    print("Gangnam_notice Next Page : {}".format(cnt));
                    return Gangnam_notice.mainCra(cnt),
                else:
                    # if numberCnt == commonConstant_NAME.SEOUL_STOP_COUNT_FOUR:
                    #     break;
                    if(fnCompareTitle(commonConstant_NAME.GANGNAM_NAME, title[i].text.strip()) == 1):
                        break;
                        
                    linkSp = link[i].attrs.get('href');
                    changeText = str(registrationdate[i].text);
                    firebase_con.updateModel( commonConstant_NAME.GANGNAM_NAME,numberCnt,
                        datasModel.toJson(
                            "https://www.gangnam.go.kr{}".format(linkSp),
                            numberCnt,
                            "",
                            title[i].text.strip(),
                            "",
                            fnChnagetype(changeText.strip()),
                            "강남구청"
                        )
                    )
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
            raise ValueError("Argument에 잘못된 값이 전달되었습니다.")