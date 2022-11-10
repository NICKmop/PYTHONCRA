import functions_framework
# 재단
from siteCrainfo.cultureFoundation.Seoul import Seoul
from siteCrainfo.cultureFoundation.Seodaemun import Seodaemun
from siteCrainfo.cultureFoundation.Youthseoul import Youthseoul
from siteCrainfo.cultureFoundation.Sbaseoul import Sbaseoul 
from siteCrainfo.cultureFoundation.Housingseoul import Housingseoul 
from siteCrainfo.cultureFoundation.Dobong import Dobong
from siteCrainfo.cultureFoundation.Geuamcheoun import Geuamcheoun
from siteCrainfo.cultureFoundation.Eunpyeng import Eunpyeng
from siteCrainfo.cultureFoundation.GwanakCra import Gwanak
from siteCrainfo.cultureFoundation.GangnamCra import Gangnam
from siteCrainfo.cultureFoundation.GangbukCra import Gnagbuk
from siteCrainfo.cultureFoundation.Gwangzin import Gwangzin
from siteCrainfo.cultureFoundation.Dongjak import Dongjak
from siteCrainfo.cultureFoundation.Seocho import Seocho
from siteCrainfo.cultureFoundation.Seongbuk import Seongbuk
from siteCrainfo.cultureFoundation.Yangcheon import Yangcheon
from siteCrainfo.cultureFoundation.Yeongdeungpo import Yeongdeungpo
from siteCrainfo.cultureFoundation.Jongro import Jongro
from siteCrainfo.cultureFoundation.Junggu import Junggu
from siteCrainfo.cultureFoundation.Dongdaemun import Dongdaemun
from siteCrainfo.cultureFoundation.Mapo import Mapo
from siteCrainfo.cultureFoundation.Seongdong import Seongdong
from siteCrainfo.cultureFoundation.Songpa import Songpa
from siteCrainfo.cultureFoundation.Npocra import Npocra
#자치구 
from siteCrainfo.cultureBorough.notice.Gangnam_Borough_Notice import Gangnam_notice
from siteCrainfo.cultureBorough.notice.Gangdong_Borough_Notice import Gangdong_notice
from siteCrainfo.cultureBorough.notice.Gangbuk_Borough_Notice import Gangbuk_notice
from siteCrainfo.cultureBorough.notice.Gangseo_Borough_Notice import Gangseo_notice
from siteCrainfo.cultureBorough.notice.Gwangzin_Borough_Notice import Gwangzin_notice
from siteCrainfo.cultureBorough.notice.Gwanak_Borough_Notice import Gwanak_notice
from siteCrainfo.cultureBorough.notice.Guro_Borough_Notice import Guro_notice
from siteCrainfo.cultureBorough.notice.Geuamcheoun_Borough_Notice import Geuamcheoun_notice
from siteCrainfo.cultureBorough.notice.Nowon_Borough_Notice import Nowon_notice
from siteCrainfo.cultureBorough.notice.Dobong_Borough_Notice import Dobong_notice
from siteCrainfo.cultureBorough.notice.Dongdaemun_Borough_Notice import Dongdaemun_notice
from siteCrainfo.cultureBorough.notice.Dongjak_Borough_Notice import Dongjak_notice
from siteCrainfo.cultureBorough.notice.Mapo_Borough_Notice import Mapo_notice
from siteCrainfo.cultureBorough.notice.Seocho_Borough_Notice import Seocho_notice
from siteCrainfo.cultureBorough.notice.Seongdong_Borough_Notice import Seongdong_notice
from siteCrainfo.cultureBorough.notice.Songpa_Borough_Notice import Songpa_notice
from siteCrainfo.cultureBorough.notice.Yangcheon_Borough_Notice import Yangcheon_notice
from siteCrainfo.cultureBorough.notice.Yeongdeungpo_Borough_Notice import Yeongdeungpo_notice
from siteCrainfo.cultureBorough.notice.Youngsan_Borough_Notice import Youngsan_notice
from siteCrainfo.cultureBorough.notice.Eunpyeng_Borough_Notice import Eunpyeng_notice
from siteCrainfo.cultureBorough.notice.Jongro_Borough_Notice import Jongro_notice
from siteCrainfo.cultureBorough.notice.Junggu_Borough_Notice import Junggu_notice
from siteCrainfo.cultureBorough.notice.Jungnang_Borough_Notice import Jungnang_notice

from siteCrainfo.cultureBorough.otherInstitutions.Gangnam_Borough_Other_Institutions import Gangnam_Institutions
from siteCrainfo.cultureBorough.otherInstitutions.Gangdong_Borough_Other_Institutions import Gangdong_Institutions
from siteCrainfo.cultureBorough.otherInstitutions.Gwanak_Borough_Other_Institutions import Gwanak_Institutions
from siteCrainfo.cultureBorough.otherInstitutions.Gwangjin_Borough_Other_Institutions import Gwanagjin_Institutions
from siteCrainfo.cultureBorough.otherInstitutions.Guro_Borough_Other_Institutions import Guro_Institutions
from siteCrainfo.cultureBorough.otherInstitutions.Geuamcheoun_Borough_Other_Institutions import Geuamcheoun_Institutions
from siteCrainfo.cultureBorough.otherInstitutions.Nowon_Borough_Other_Institutions import Nowon_Institutions
from siteCrainfo.cultureBorough.otherInstitutions.Dongdaemun_Borough_Other_Institutions import Dongdaemun_Institutions
from siteCrainfo.cultureBorough.otherInstitutions.Dongjak_Borough_Other_Institutions import Dongjak_Institutions
from siteCrainfo.cultureBorough.otherInstitutions.Mapo_Borough_Other_Institutions import Mapo_Institutions

# @functions_framework.http
# def runningCra(request):
if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        # print(path.dirname( path.dirname( path.abspath(__file__) ) ));
        sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ));
        # 재단
        try:
            # Dobong.mainCra(1,0); 
            # Dobong_notice.mainCra(1);

            # Dongdaemun.mainCra(1,0);
            # Dongdaemun_notice.mainCra(1);

            # Dongjak.mainCra(1,0);
            # Dongjak_notice.mainCra(1);

            # Eunpyeng.mainCra(1,0);
            # Eunpyeng_notice.mainCra(1);

            # Gnagbuk.mainCra(1,0);

            # Gangdong_notice.mainCra(1,0);

            # Gangnam.mainCra(0,0);
            # Gangnam_notice.mainCra(1);

            # Gangseo_notice.mainCra(1,0);

            # Geuamcheoun.mainCra(1,0);
            # Geuamcheoun_notice.mainCra(1);

            # Guro_notice.mainCra(1,0);

            # Gwanak.mainCra(0,0);
            # Gwanak_notice.mainCra(1);

            # Gwangzin.mainCra(1,0);
            # Gwangzin_notice.mainCra(1);

            # Jongro.mainCra(1,0);
            # Jongro_notice.mainCra(1);

            # Junggu.mainCra(1,0);
            # Junggu_notice.mainCra(1);

            # Jungnang_notice.mainCra(1,0);

            # Mapo.mainCra(1,0);
            # Mapo_notice.mainCra(1);

            # Nowon_notice.mainCra(1,0);

            # Seocho.mainCra(1,0);
            # Seocho_notice.mainCra(1);

            # Seongbuk.mainCra(1,0);

            # Seongdong.mainCra(1,0);
            # Seongdong_notice.mainCra(1);

            # Npocra.mainCra(1,0);
            # Youthseoul.mainCra(1);
            # Sbaseoul.mainCra(1);
            Housingseoul.mainCra(1);

            # Songpa.mainCra(1,0);
            # Songpa_notice.mainCra(1);

            # Yangcheon.mainCra(1,0);
            # Yangcheon_notice.mainCra(1);

            # Yeongdeungpo.mainCra(1,0);
            # Yeongdeungpo_notice.mainCra(1);

            # Youngsan_notice.mainCra(1,0);

            #서울시는 따로 진행 
            # 크롤링 확인 필요 부분
            # Gangbuk_notice.mainCra(1);
            # Seoul.mainCra(1,0);
            # Seodaemun.mainCra(1,0);
        except ConnectionError as conerror:
            print(conerror);

    else:
        # 재단
        try:
            # 크롤링 다시 확인 필요
            # Yeongdeungpo.mainCra(1,0);
            # Yeongdeungpo_notice.mainCra(1);

            Dobong.mainCra(1,0);
            Dobong_notice.mainCra(1);

            # 데이터 다시 크롤링 필요
            # Mapo.mainCra(1,0);
            # Mapo_notice.mainCra(1);

            # Gnagbuk.mainCra(1,0);

            # Gwangzin.mainCra(1,0);
            # Gwangzin_notice.mainCra(1);

            # Seocho.mainCra(1,0);
            # Seocho_notice.mainCra(1);

            # Geuamcheoun.mainCra(1,0);
            # Geuamcheoun_notice.mainCra(1);

            # Songpa.mainCra(1,0);
            # Songpa_notice.mainCra(1);

            # Yangcheon.mainCra(1,0);
            # Yangcheon_notice.mainCra(1);

            # Jongro.mainCra(1,0);
            # Jongro_notice.mainCra(1);

            # Gwanak.mainCra(0,0);
            # Gwanak_notice.mainCra(1);

            # Gangnam.mainCra(0,0);
            # Gangnam_notice.mainCra(1);

            # Dongjak.mainCra(1,0);
            # Dongjak_notice.mainCra(1);

            # Seongbuk.mainCra(1,0);

            # Junggu.mainCra(1,0);
            # Junggu_notice.mainCra(1);

            # Eunpyeng.mainCra(1,0);
            # Eunpyeng_notice.mainCra(1);

            # Dongdaemun.mainCra(1,0);
            # Dongdaemun_notice.mainCra(1);

            # Seongdong.mainCra(1,0);
            # Seongdong_notice.mainCra(1);

            # Gangdong_notice.mainCra(1,0);

            # Gangseo_notice.mainCra(1,0);

            # Guro_notice.mainCra(1,0);

            # Nowon_notice.mainCra(1,0);

            # Youngsan_notice.mainCra(1,0);

            # Jungnang_notice.mainCra(1,0);

            # Npocra.mainCra(1,0);
            # Youthseoul.mainCra(1);
            # Sbaseoul.mainCra(1);
            # Housingseoul.mainCra(1);

            # 크롤링 확인 필요 부분
            # 서울시는 따로 적용 필요
            # Gangbuk_notice.mainCra(1);
            # Seoul.mainCra(1,0); 링크 한번 확인 필요
            # Seodaemun.mainCra(1,0);
        except ConnectionError as conerror:
            print(conerror);
    
        