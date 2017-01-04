import pickle
import cPickle
import numpy as np
import csv

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn import svm
from csvParsers import preAmex, preCapitolOne, preFinances

####Check if the same tuple exists in finances list or that the value && description are the same
def checkDuplicateEntry(financesList, entry):
        for value in financesList:
            if value[0] == entry[0] and value[1] == entry[1] and value[2] == entry[2] and value[3] == value [3]:
                print(value[2], value[2])
####Training List in (date, value,location, label) format

def trainData(trainingList):
    locationList = [a[2] for a in trainingList]
    labelsList = [a[3] for a in trainingList]

    vectorizer = CountVectorizer()
    vectorizerArray = vectorizer.fit(locationList)
    ###Vectorize the array of locations
    train_data_features = vectorizer.fit_transform(locationList)
    ###Change to numpyArray
    train_data_features = train_data_features.toarray()

    clf = svm.LinearSVC(random_state=0)
    clf.fit(train_data_features, labelsList)
    return vectorizer, clf

###Using the LinearSVC make a prediction about the description of the transaction
###returning a list of transactions with descriptions

def addTransactions(transactionList, financesList):
    rtrnList = []

    print 'Training Data'

    vectorizer, clf = trainData(financesList)

    ###Transaction List is list of tuples (date, value, location)

    for item in transactionList:
        date = item[0]
        value = item[1]
        location = item[2]
        ###Make a prediction for the description
        description = clf.predict(vectorizer.transform([location]).toarray())[0]

        ###Check if entry might be duplicate
        checkDuplicateEntry(financesList, (date,value,location,description))

        ##Append To List
        rtrnList.append((date,value,description,location))

    return rtrnList

##### Write the completed list to the csv file output

def writeToCSV(outputName,transactions):
    with open(outputName , "wb") as outcsv:
        writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        for item in transactions:
            #Write item to outcsv
            writer.writerow([item[0], item[1],'','','', item[2],item[3]])


#####Determine which files to pass to algorithm

def transactionsRawList():
    ###Get all prior financial transactions
    # financesPath = './csvFiles/'+raw_input("Finances File Name: ") + '.csv'
    financesPath = './csvFiles/finances.csv'
    finances = preFinances.financesCSV(financesPath)
    financesList = finances.readFile()

    ###All of the other files to be proccessed
    # capitoloneFilePath = './csvFiles/'+ raw_input('Capitol One File Name: ') + '.csv'
    capitoloneFilePath = "./csvFiles/capitolone.csv"
    capitolOneList = preCapitolOne.CapitolOneCSV(capitoloneFilePath).readFile()

    # amexFilePath = './csvFiles/'+raw_input("Amex File Name: ") + '.csv'
    amexFilePath = './csvFiles/amex.csv'
    amexList = preAmex.amexCSV(amexFilePath).readFile()

    outputName = "./outputFiles/"+raw_input("What to call the output file: ") + ".csv"
    predictedTransactions = addTransactions((capitolOneList + amexList), financesList)

    ###Write to csv
    writeToCSV(outputName,predictedTransactions)


transactionsRawList()
