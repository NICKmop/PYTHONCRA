import re
from common.common_fnc import fnCompareTitle
from common.common_fnc import fnChnagetype
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
import common.common_fnc  as com

class Seongdong:
    def mainCra(cnt,numberCnt):
        try:
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.SEONGDONG_NAME);
            maxCntNumber = max(cntNumber);

            url = 'https://www.sdfac.or.kr/kor/sdfac/board/noti_list.do?gotoMenuNo=06010000';
            soupData = com.pageconnect(cnt, url, "setPage({})".format(cnt));
            
            link = soupData.select('.listType > li > a');
            title = soupData.select('.listType > li > a');
            registrationdate = soupData.select('.writer > li:nth-child(1)');

            linkCount = len(link) - 1;
            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    # javascript:pageNum('frm01','200');
                    cnt += 10;
                    print("Seongdong Next Page : {}".format(cnt));
                    return Seongdong.mainCra(cnt, numberCnt),
                else:
                    # if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT:
                    #     break;
                    if(fnCompareTitle(commonConstant_NAME.SEONGDONG_NAME, title[i].text.strip()) == 1):
                        break;
                    else:
                        maxCntNumber += 1;

                        linkSp = re.sub(r'[^0-9]','',link[i].attrs.get('onclick'));
                        changeText= str(registrationdate[i].text);

                        firebase_con.updateModel( commonConstant_NAME.SEONGDONG_NAME,maxCntNumber,
                            datasModel.toJson(
                                "https://www.sdfac.or.kr/kor/sdfac/board/noti_view.do?page={}&b_idx={}&bbs_id=noti&article_category=&searchCnd=3&searchWrd=".format(cnt , linkSp),
                                maxCntNumber,
                                "",
                                title[i].text.strip(),
                                "",
                                fnChnagetype(changeText.strip()),
                                "성동문화재단"
                            )
                        )
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
            raise ValueError("Argument에 잘못된 값이 전달되었습니다.")