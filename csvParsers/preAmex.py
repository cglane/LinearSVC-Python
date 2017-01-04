
class amexCSV(object):
    def __init__(self, fileAddress):
        self.fileAddress = fileAddress
        self.fileList = []
    def getValue(self, rowList):
        value = 0
        if rowList[9]:
            value = rowList[9]
        elif rowList[8]:
            value = rowList[8]
        elif rowList[7]:
            value = rowList[7]
        return float(value) * -1
    def splitRow(self, row):
        rowList = row.split(',')
        ###Remove Day from date string
        date = rowList[0].split('  ')[0]

        ##Adding negative sign to value
        value =  self.getValue(rowList)
        ##Get third item, only text before '-' and not including the "
        location = rowList[2].split(' -')[0][1:]
        if location != 'ONLINE PAYMENT ':
            return (date,value,location)

    def readFile(self):
        try:
            with open(self.fileAddress, 'rb') as csvfile:
                for row in csvfile:
                    formattedRow = self.splitRow(row)
                    if formattedRow:
                        self.fileList.append(formattedRow)
            ###Return the list backwards so it it ends with most recent purchases
            return self.fileList[::-1]
        except Exception as e:
            print "An error has occurred"
            return []
