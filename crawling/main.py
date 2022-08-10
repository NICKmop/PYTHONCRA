from siteCrainfo.GwanakCra import craMain
from siteCrainfo.GangnamCra import Gnagnam
from siteCrainfo.GangbukCra import Gnagbuk
from siteCrainfo.Gwangzin import Gwangzin
from siteCrainfo.Dongjak import Dongjak

if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        print(path.dirname( path.dirname( path.abspath(__file__) ) ));
        sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ));

        # craMain.mainCra(0);
        # Gnagnam.mainCra(1,0);
        # Gnagbuk.mainCra(1,0);
        # Gwangzin.mainCra(1,0);
        Dongjak.mainCra(1,0);
    else:
        # craMain.mainCra(0);
        # Gnagnam.mainCra(1,0);
        # Gnagbuk.mainCra(1,0);
        # Gwangzin.mainCra(1,0);
        Dongjak.mainCra(1,0);


        
