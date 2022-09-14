import common.common_fnc
class datasModel:
    link = "";
    number = "";
    result = "";
    title = "";
    apperiod = "";
    registrationdate = "";

    def __init__(self, link, number, result, title, apperiod,registrationdate):
        self.link = link;
        self.number = number;
        self.result = result;
        self.title = title;
        self.apperiod = apperiod;
        self.registrationdate = registrationdate;

    def toJson(self, link, number, result, title, apperiod, registrationdate):
        dataModel = {
            "link" : self, 
            "number" : link, 
            "result" : number, 
            "title" : result, 
            "apperiod" : title, 
            "registrationdate" : apperiod,
            "center_name " : registrationdate,
        }

        common.common_fnc.loggingdata(dataModel);

        return dataModel;


        