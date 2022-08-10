import requests
from bs4 import BeautifulSoup
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel

class common_fnc:

    def mainCraData(link, title, registrationdate):
        return link, title, registrationdate;

    def mainCra(cnt,numberCnt,url):
        requests.packages.urllib3.disable_warnings()
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

        numberCnt = numberCnt;
        cnt  = cnt; # 1
        url = url;
        response = requests.get(url);

        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser');

            # 타이틀 ,기관, 링크, 등록일, 번호
            link = common_fnc.mainCraData();
            print(link);
            title = common_fnc.mainCraData();
            registrationdate = common_fnc.mainCraData();

            linkCount = len(link) - 1;
            print("linkCount : ", linkCount);

            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print("Next Page : {}".format(cnt));
                    return common_fnc.mainCra(cnt, numberCnt, url);
                else:
                    print("title : ", title[i].text.strip());
                    print(link[i].attrs.get('href'))
                    # print("https://www.gbcf.or.kr/{}".format(link[i].attrs.get('href')));
                    print("registrationdate : ", registrationdate[i].text);
                    
                    # if "2022-07" in registrationdate[i].text:
                    #     break;
                    if numberCnt == commonConstant_NAME.STOPCUOUNT:
                        break;
                    
                    firebase_con.updateModel(commonConstant_NAME.DONGJAK_NAME,numberCnt,
                        datasModel.toJson(
                            link[i].attrs.get('href'),
                            numberCnt,
                            "",
                            title[i].text.strip(),
                            "",
                            registrationdate[i].text,
                            "동작문화재단",
                        )
                    );
        else : 
            print(response.status_code)