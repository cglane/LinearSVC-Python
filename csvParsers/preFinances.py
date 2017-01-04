
class financesCSV(object):
    def __init__(self, filename):
        self.fileName = filename
    def getValue(self,rowList):
            value = 0
            if rowList[1]:
                value = rowList[1]
            elif rowList[2]:
                value = rowList[2]
            elif rowList[3]:
                value = rowList[3]
            elif rowList[4]:
                value = rowList[4]
            return value

    def splitRow(self,row):
        rowList = row.split(',')
        date = rowList[0]
        value = float(self.getValue(rowList))
        location = rowList[6]
        label = rowList[5]
        return (date, value, location, label)

    def readFile(self):
        fileList = []
        try:
            with open(self.fileName,'rb') as csvfile:
                for row in csvfile:
                    fileList.append(self.splitRow(row))
            return fileList
        except Exception as e:
            print ['Error has occured with file']
            return []
