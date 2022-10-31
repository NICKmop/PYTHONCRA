import re
from common.common_fnc import fnChnagetype
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
import common.common_fnc  as com

class Dongdaemun:
    def mainCra(cnt,numberCnt):
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
                if numberCnt == commonConstant_NAME.STOPCUOUNT:
                    break;

            if title[i].text.strip() == '':
                continue;
            else:
                linkSp = re.sub(r'[^0-9]','',link[i].attrs.get('href'));
                changeText= str(registrationdate[i].text);
                firebase_con.updateModel( commonConstant_NAME.DONGDAEMUN_NAME,i,
                    datasModel.toJson(
                        "http://ddmac.or.kr/sub04/sub01.php?type=view&uid={}".format(linkSp),
                        i,
                        "",
                        title[i].text.strip(),
                        "",
                        fnChnagetype(changeText.strip()),
                        "동대문문화재단"
                    )
                )