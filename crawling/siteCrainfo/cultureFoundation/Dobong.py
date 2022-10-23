from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
import common.common_fnc  as com

class Dobong:
    def mainCra(cnt,numberCnt):
        url = 'http://www.dbfac.or.kr/front/board/boardContentsListPage.do?board_id=1';
        soupData = com.pageconnect(cnt, url, "go_Page({})".format(cnt));

        link = soupData.select('td > a');
        title = soupData.select('td > a');
        registrationdate = soupData.select('td:nth-child(4)');
        linkCount = len(link) - 1;

        for i in range(len(link)):
            numberCnt += 1;
            if linkCount == i:
                # javascript:pageNum('frm01','200');
                cnt += 10;
                print("Dobong Next Page : {}".format(cnt));
                return Dobong.mainCra(cnt, numberCnt),
            else:
                if numberCnt == commonConstant_NAME.STOPCUOUNT:
                    break;
                    
            if title[i].text.strip() == '':
                continue;
            else:
                linkAttr = link[i].attrs.get('href');
                linkSub = linkAttr.split("(")[1].replace(")", '');
                linkSubts = linkSub.split(",");

                linkSubts1 = linkSubts[0].replace("'",'');
                linkSubts2 = linkSubts[1].replace("'",'');

                firebase_con.updateModel( commonConstant_NAME.DOBONG_NAME,i,
                    datasModel.toJson(
                        "http://www.dbfac.or.kr/front/board/boardContentsView.do?miv_pageNo=&miv_pageSize=10&total_cnt=&LISTOP=&mode=W&contents_id={}&board_id={}&viewType=&cate_id=&searchkey=T&searchtxt=".format(linkSubts1, linkSubts2),
                        i,
                        "",
                        title[i].text.strip(),
                        "",
                        registrationdate[i].text.strip(),
                        "도봉문화재단"
                    )
                )