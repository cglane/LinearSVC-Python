import csv
class CapitolOneCSV(object):
    def __init__(self, fileName):
        self.fileName = fileName
    ###Row 7 is for credits but 6 for debits
    def getValue(self,row):
        if row[6]:
            return float(row[6]) * -1
        elif row[7]:
            return float(row[7])

    def readFile(self):
        rtrnList = []
        try:
            with open(self.fileName, 'rb') as csvfile:
                reader = csv.reader(csvfile)
                your_list = list(reader)

                ###Ignore First Column and reverse list
                for row in your_list[1:][::-1]:
                    ###Don't want to include credit card payments
                    if ("CAPITAL ONE ONLINE" not in row[4]):
                        date = row[1]
                        value = self.getValue(row)
                        location = row[4]
                        rtrnList.append((date,value,location))
                return rtrnList
        except Exception as e:
            print 'Error has occured'
            return []
