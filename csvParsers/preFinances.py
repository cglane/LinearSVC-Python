import pandas as pd
from math import isnan

###Values may be strings or NaN
def extendValues(list):
    if list:
        try:
            return float(list[0])
        except Exception as e:
            return 0
    else:
        return 0

class financesCSV(object):
    def __init__(self, filename = '../csvFiles/finances.csv', dateCol = "Date",valueCols = ['Amount Salary', 'Amount BankSC','13 Drews Ct.','Work Related/Other'], locationCol = 'Description II', labelCol = "Description"):
        self.fileName = filename
        self.values = valueCols
        self.locations = locationCol
        self.labels = labelCol
        self.dates = dateCol

    def readFile(self):
        try:
            data = pd.read_csv(self.fileName)
            dates = data[self.dates]
            locations = data[self.locations].fillna('empty')
            labels = data[self.labels].fillna('empty')
            valuesArray = [[a for a in x if a != 'empty' ] for x in data[self.values].fillna('empty').values]
            values =  map(lambda x: extendValues(x) ,valuesArray)
            return {'dates':dates, 'locations':locations, 'labels':labels, 'values':values}
        except Exception as e:
            print (e,'Error has occured with preFinance')
            return {}
