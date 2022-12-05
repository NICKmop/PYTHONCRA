import re
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
import common.common_fnc  as com

class Dongdaemun:
    def mainCra(cnt,numberCnt):
        try:
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.DONGDAEMUN_NAME);
            maxCntNumber = max(cntNumber);

            url = 'https://www.ddmac.or.kr/sub04/sub01.php';
            soupData = com.pageconnect(cnt, url, "javascript:pageNum('frm01','{}')".format(cnt));
            
            link = soupData.select('.b-text-s > a');
            title = soupData.select('.board1');
            registrationdate = soupData.select('td:nth-child(6)');

            linkCount = len(link) - 1;
            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    # javascript:pageNum('frm01','200');
                    cnt += 10;
                    print("Dongdaemun Next Page : {}".format(cnt));
                    return Dongdaemun.mainCra(cnt, numberCnt),
                else:
                    # if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT:
                    #     break;

                    if(fnCompareTitle(commonConstant_NAME.DONGDAEMUN_NAME, title[i].text.strip()) == 1):
                        break;
                    else:
                        maxCntNumber += 1;
                        if title[i].text.strip() == '':
                            continue;
                        else:
                            linkSp = re.sub(r'[^0-9]','',link[i].attrs.get('href'));
                            changeText= str(registrationdate[i].text);
                            if(changeText == '등록일'):
                                numberCnt -= 1;
                            if(changeText != '등록일'):
                                firebase_con.updateModel( commonConstant_NAME.DONGDAEMUN_NAME,maxCntNumber,
                                    datasModel.toJson(
                                        "http://ddmac.or.kr/sub04/sub01.php?type=view&uid={}".format(linkSp),
                                        maxCntNumber,
                                        "",
                                        title[i].text.strip(),
                                        "",
                                        fnChnagetype(changeText.strip()),
                                        "동대문문화재단"
                                    )
                                )
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
            raise ValueError("Argument에 잘못된 값이 전달되었습니다.")