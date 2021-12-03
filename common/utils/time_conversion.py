from datetime import datetime
import datetime

class TimeConverter:
    def isoJsonArrayToEpochJsonArray(self, JsonArray):
        # input can be either cursor object or json array or list of json, out will be list
        lst = []
        for doc in JsonArray:
            for i in doc:
                if type(doc[i]) == datetime or type(doc[i]) == datetime.datetime:
                    d2 = int(doc[i].timestamp() * 1000)
                    doc[i] = str(d2)
            lst.append(doc)
        return lst

    def dateStringtoISOformat(self,DateString):
        #Format should be "dd-mm-yyy"
        format = "%d-%m-%Y"
        d = datetime.datetime.strptime(DateString, format)
        d.isoformat()
        return d

