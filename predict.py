import pickle
import cPickle
import numpy as np
import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn import svm
from csvParsers import preAmex, preCapitolOne, preFinances

from datetime import datetime

def get_date(record):
    return datetime.strptime(record[0], "%m/%d/%Y")

####Check if the same tuple exists in finances list or that the value && description are the same
def isDuplicateEntry(financesTuples, entry):
        if entry in financesTuples:
            print (entry, 'Duplicate entry not added')
            return True

####Training List in (date, value,location, label) format

def trainData(trainingList):
    locationList = trainingList['locations']
    labelsList = trainingList['labels']

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

def addTransactions(transactionList, financesList, excludedLocations = ['ONLINE PAYMENT']):
    rtrnList = []

    print 'Training Data'
    vectorizer, clf = trainData(financesList)

    ###Transaction List is list of tuples (date, value, location)
    financesTuples = [tuple(x) for x in zip(financesList['dates'],financesList['values'],financesList['locations'])]
    for item in transactionList:
        date = item[0]
        value = item[1]
        location = item[2]
        ###Make a prediction for the description
        description = clf.predict(vectorizer.transform([location]).toarray())[0]
        ###Check if entry might be duplicate
        if isDuplicateEntry(financesTuples, (date,float(value),location)):
            pass
                #Append To List
        if location not in excludedLocations:
            rtrnList.append((date,value,description,location))

    return rtrnList

##### Write the completed list to the csv file output

def writeToCSV(outputName,transactions):
    transactions = sorted(transactions, key=get_date, reverse=False)

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
