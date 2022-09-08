from siteCrainfo.Geuamcheoun import Geuamcheoun
from siteCrainfo.Eunpyeng import Eunpyeng
from siteCrainfo.GwanakCra import Gwanak
from siteCrainfo.GangnamCra import Gangnam
from siteCrainfo.GangbukCra import Gnagbuk
from siteCrainfo.Gwangzin import Gwangzin
from siteCrainfo.Dongjak import Dongjak
from siteCrainfo.Seocho import Seocho
from siteCrainfo.Seongdong import Seongdong
from siteCrainfo.Seongbuk import Seongbuk
from siteCrainfo.Yangcheon import Yangcheon
from siteCrainfo.Yeongdeungpo import Yeongdeungpo
from siteCrainfo.Jongro import Jongro
from siteCrainfo.Junggu import Junggu

if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        print(path.dirname( path.dirname( path.abspath(__file__) ) ));
        sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ));

        # Gwanak.mainCra(0,0);
        # Gangnam.mainCra(0,0);
        # Gnagbuk.mainCra(1,0);
        # Gwangzin.mainCra(1,0);
        # Dongjak.mainCra(1,0);
        # Seocho.mainCra(1,0);
        # Seongbuk.mainCra(1,0);
        # Yangcheon.mainCra(1,0);
        # Yeongdeungpo.mainCra(1,0);
        # Jongro.mainCra(1,0);
        # Junggu.mainCra(1,0);
        # Eunpyeng.mainCra(1,0);
        Geuamcheoun.mainCra(1,0);
    else:
        # Gwanak.mainCra(0,0);
        # Gangnam.mainCra(0,0);
        # Gnagbuk.mainCra(1,0);
        # Gwangzin.mainCra(1,0);
        # Dongjak.mainCra(1,0);
        # Seocho.mainCra(1,0);
        # Seongbuk.mainCra(1,0);
        # Yangcheon.mainCra(1,0);
        # Yeongdeungpo.mainCra(1,0);
        # Jongro.mainCra(1,0);
        # Junggu.mainCra(1,0);
        # Eunpyeng.mainCra(1,0);
        Geuamcheoun.mainCra(1,0);


        
