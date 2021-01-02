import csv
import math
import sys
import copy
# from anytree import Node, RenderTree

#wrong input
class errorMessageInput(Exception):
    pass

# moneyWords = ["buy", "money", "customer", "gold", "sell", "price", "spend", "currency", "transfer", "free", "interest",
#                 "million", "recieved", "100", "billion", "earn", "cash", "bonus", "satisfied", 'double',
#                 "gift", "trial", "prize", "approved", "help", "visit", "now", "exclusive", "deal", "available",
#                 "mon", "mailer", "congradulations", "content", "party"]
moneyWords = ["exchange", "number", "customer", "time" ,"limited","buy", "money", "customer", "gold", "sell", "price", "spend", "currency", "transfer", "free", "interest",
                 "million", "recieved", "100", "billion", "earn", "cash", "bonus", "satisfied", 'double',
                 "gift", "trial", "prize", "approved", "visit", "now", "exclusive", "deal", "available",
                 "congradulations", "content", "urgent", "price"]
#reads data and puts into array format
def readData(fileName):
    data = []
    with open(fileName, newline='') as csvfile:
        tempData = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in tempData:
            data.append(row)
    return data

#counts words and their association with spam/not spam
def countAndOrganizeWords(train_data, smoothing_param, feature = "NONE"):
    dicValues = {}
    spamTotal = 0
    hamTotal = 0

    if((feature=="NUMBER") or (feature=="KEYWORDS")):
        dicValues["NUMBER SPAM"] = smoothing_param
        dicValues["NUMBER HAM"] = smoothing_param
        dicValues["NO NUMBER SPAM"] = smoothing_param
        dicValues["NO NUMBER HAM"] = smoothing_param

        dicValues["TOTAL NUMBER"] = 2*smoothing_param
        dicValues["TOTAL NO NUMBER"] = 2*smoothing_param

    for i in range(0,len(train_data)):
        #if spam
        spamFlag = 0
        if(train_data[i][1]=="spam"):
            spamFlag =1

        #counts each word and seperates based on spam or not
        for j in range(2,len(train_data[i])):
            if((j%2)==0): #word
                # print(train_data[i][j])
                count = int(train_data[i][j+1]) #already existing count
                newFlag = 0
                #adds word to dictionary
                if(train_data[i][j] not in dicValues.keys()):
                    if(spamFlag==1):
                        dicValues[train_data[i][j]]={"SPAM":(count+smoothing_param),"NOT SPAM":smoothing_param}

                    else:
                        dicValues[train_data[i][j]]={"SPAM":smoothing_param,"NOT SPAM":(count+smoothing_param)}

                    newFlag = smoothing_param
                else:
                    if(spamFlag==1):
                        dicValues[train_data[i][j]]["SPAM"] = dicValues[train_data[i][j]]["SPAM"] + count

                    else:
                        dicValues[train_data[i][j]]["NOT SPAM"] = dicValues[train_data[i][j]]["NOT SPAM"] + count

                #totals
                if(spamFlag==1):
                    spamTotal = spamTotal + count + newFlag #new flag is only when new word is found
                    hamTotal = hamTotal + newFlag

                    ifStatement = None
                    if(feature=="NUMBER"):
                        ifStatement = ((any(char.isdigit() for char in train_data[i][j])) and (any(char.isalpha() for char in train_data[i][j])))
                    elif(feature=="KEYWORDS"):
                        ifStatement = train_data[i][j] in moneyWords
                    if(feature!="NONE"):
                    # if(feature=="NUMBER"):
                    #     if(train_data[i][j] in moneyWords):
                        if(ifStatement):
                        # if((any(char.isdigit() for char in train_data[i][j])) and (any(char.isalpha() for char in train_data[i][j]))):
                            dicValues["NUMBER SPAM"] = dicValues["NUMBER SPAM"] + count
                            dicValues["TOTAL NUMBER"] = dicValues["TOTAL NUMBER"] + count
                        else:
                            dicValues["NO NUMBER SPAM"] = dicValues["NO NUMBER SPAM"] + count
                            dicValues["TOTAL NO NUMBER"] = dicValues["TOTAL NO NUMBER"] + count
                else:
                    hamTotal = hamTotal + count + newFlag
                    spamTotal = spamTotal + newFlag
                    ifStatement = None
                    if(feature=="NUMBER"):
                        ifStatement = ((any(char.isdigit() for char in train_data[i][j])) and (any(char.isalpha() for char in train_data[i][j])))
                    elif(feature=="KEYWORDS"):
                        ifStatement = train_data[i][j] in moneyWords
                    if(feature!="NONE"):
                        if(ifStatement):
                        # if(train_data[i][j] in moneyWords):
                        # if((any(char.isdigit() for char in train_data[i][j])) and (any(char.isalpha() for char in train_data[i][j]))):
                            # print(train_data[i][j])
                            dicValues["NUMBER HAM"] = dicValues["NUMBER HAM"] + count
                            dicValues["TOTAL NUMBER"] = dicValues["TOTAL NUMBER"] + count
                        else:
                            dicValues["NO NUMBER HAM"] = dicValues["NO NUMBER HAM"] + count
                            dicValues["TOTAL NO NUMBER"] = dicValues["TOTAL NO NUMBER"] + count
    # print(dicValues)
    listNotToUse = ["NUMBER SPAM","NUMBER HAM", 'NO NUMBER SPAM', 'NO NUMBER HAM', 'TOTAL NUMBER', 'TOTAL NO NUMBER']
    #get probabilities of each word
    for i in dicValues.keys():
        if(i not in listNotToUse):
            # print(dicValues[i]["SPAM"])
            # print(spamTotal)
            spamPercent = dicValues[i]["SPAM"]/spamTotal
            notSpamPercent = dicValues[i]["NOT SPAM"]/hamTotal
            dicValues[i]["SPAM PERCENT"] = spamPercent
            dicValues[i]["NOT SPAM PERCENT"] = notSpamPercent

    #prob of spam/ham
    probSpam = spamTotal/(spamTotal+hamTotal)
    probHam = hamTotal/(hamTotal+spamTotal)

    return dicValues, probSpam, probHam, spamTotal, hamTotal


#if word was unseen before, calculate its value as smoothing val/total, where total now increased by respective smoothing param (for all)
def wordNotSeen(probDicValues, test_data_line, smoothing, probSpam, probHam, spamTotal, hamTotal, feature="NONE"):
    probS = copy.deepcopy(probSpam) #spam
    probH = copy.deepcopy(probHam) #not spam (ham)
    spamT = copy.deepcopy(spamTotal)
    hamT = copy.deepcopy(hamTotal)

    count = 0
    for j in range(2,len(test_data_line)):
        #count how many unseen words
        try:
            temp = probDicValues[test_data[j]]["SPAM"]
            temp2 = probDicValues[test_data[j]]["NOT SPAM"]
        except KeyError:
            count = count+1

    spamT = spamT + (count*smoothing)
    hamT = hamT + (count*smoothing)

    for j in range(2,len(test_data_line)):
        try:
            probS = probS * ((probDicValues[test_data[j]]["SPAM"]/spamT)**int(test_data[j+1]))
            probH = probH * ((probDicValues[test_data[j]]["NOT SPAM"]/hamT)**int(test_data[j+1]))                
        except KeyError:
            probS = probS* (smoothing/spamT)
            probH = probH * (smoothing/hamT)
        ifStatement = None
        if(feature=="NUMBER"):
            ifStatement = ((any(char.isdigit() for char in train_data[j])) and (any(char.isalpha() for char in train_data[j])))
        elif(feature=="KEYWORDS"):
            ifStatement = train_data[j][j] in moneyWords
        
        if(feature!="NONE"): #number feature
            if(ifStatement):
            # if((any(char.isdigit() for char in train_data[j])) and (any(char.isalpha() for char in train_data[j]))): #if number present
                probS = probS * (((probDicValues[test_data[j]]["NUMBER SPAM"]+(count*smoothing))/(probDicValues[test_data[j]]["TOTAL NUMBER"]+(count*smoothing)))**int(test_data[j+1]))
                probH = probH * (((probDicValues[test_data[j]]["NUMBER HAM"]+(count*smoothing))/(probDicValues[test_data[j]]["TOTAL NUMBER"]+(count*smoothing)))**int(test_data[j+1]))
            else:
                probS = probS * (((probDicValues[test_data[j]]["NO NUMBER SPAM"]+(count*smoothing))/(probDicValues[test_data[j]]["TOTAL NO NUMBER"]+(count*smoothing)))**int(test_data[j+1]))
                probH = probH * (((probDicValues[test_data[j]]["NO NUMBER HAM"]+(count*smoothing))/(probDicValues[test_data[j]]["TOTAL NO NUMBER"]+(count*smoothing)))**int(test_data[j+1]))    
    return probS, probH
            


#predict if spam/not spam
def classifyTestData(test_data, probDicValues, probSpam, probHam, spamTotal, hamTotal, smoothing, feature="NONE"):
    answerList = []


    for i in range(0,len(test_data)):
        #calculate prob of spam and not spam for words present
        probS = copy.deepcopy(probSpam) #spam
        probH = copy.deepcopy(probHam) #not spam (ham)
        for j in range(2,len(test_data[i])):
            if((j%2)==0):
                try:
                    probS = probS*((probDicValues[test_data[i][j]]["SPAM PERCENT"])**int(test_data[i][j+1])) #mult by amount of times word occurs
                    probH = probH*((probDicValues[test_data[i][j]]["NOT SPAM PERCENT"])**int(test_data[i][j+1]))
                    ifStatement = None
                    if(feature=="NUMBER"):
                        ifStatement = ((any(char.isdigit() for char in test_data[i][j])) and (any(char.isalpha() for char in test_data[i][j])))
                    elif(feature=="KEYWORDS"):
                        ifStatement = test_data[i][j] in moneyWords
                    
                    if(feature!="NONE"):
                        if(ifStatement):
                        # if((any(char.isdigit() for char in test_data[i][j])) and (any(char.isalpha() for char in test_data[i][j]))):
                            probS = probS*((probDicValues["NUMBER SPAM"]/probDicValues["TOTAL NUMBER"])**int(test_data[i][j+1]))
                            probH = probH*((probDicValues["NUMBER HAM"]/probDicValues["TOTAL NUMBER"])**int(test_data[i][j+1]))
                        else:
                            probS = probS*((probDicValues["NO NUMBER SPAM"]/probDicValues["TOTAL NO NUMBER"])**int(test_data[i][j+1]))
                            probH = probH*((probDicValues["NO NUMBER HAM"]/probDicValues["TOTAL NO NUMBER"])**int(test_data[i][j+1]))                       
                except KeyError:
                    probS, probH = wordNotSeen(probDicValues, test_data[i], smoothing, probSpam, probHam, spamTotal, hamTotal, feature)
                    break
                    # probS = smoothing/spamTotal #smoothing, should increase total but is relatively the same ==> SHOULD FIX
                    # probH = smoothing/hamTotal

        if(probS>probH):
            answerList.append("spam")
        else:
            answerList.append("ham")

    return answerList

#error testing
def overallErrorTest(test_data, answerList):
    dicCategory = {"TOTAL ACTUAL SPAM": 0, "TOTAL ACTUALLY NOT SPAM": 0}
    dicWrong = {"SPAM": 0, "NOT SPAM": 0, "TOTAL WRONG": 0}
    for i in range(0,len(test_data)):
        if(test_data[i][1]=="spam"):
            dicCategory["TOTAL ACTUAL SPAM"] = dicCategory["TOTAL ACTUAL SPAM"] + 1
        else:
            dicCategory["TOTAL ACTUALLY NOT SPAM"] = dicCategory["TOTAL ACTUALLY NOT SPAM"] + 1

        if(test_data[i][1]!=answerList[i]):
            dicWrong["TOTAL WRONG"] = dicWrong["TOTAL WRONG"] +1
            if(test_data[i][1]=="spam"):
                dicWrong["SPAM"] = dicWrong["SPAM"] +1
            else:
                dicWrong["NOT SPAM"] = dicWrong["NOT SPAM"] +1
    dicWrong["TOTAL"] = len(test_data)
    return dicWrong, dicCategory

def printOverallError(dicWrong, dicCategory):
    print("\nOverall Errors:")
    for key in dicWrong.keys():
        print("\t"+key + ": " + str(dicWrong[key]))
    
    # print("\n")
    for key in dicCategory.keys():
        print("\t"+key + ": " + str(dicCategory[key]))
        
                
truth = 0
userInput = sys.argv
# print(sys.argv)
try:
    if((len(userInput)!=7) and (len(userInput)!=9)):
        raise errorMessageInput

    feature = "NONE"
    if(userInput[1]!="-f1"):
        raise errorMessageInput
    if(userInput[3]!="-f2"):
        raise errorMessageInput
    if(userInput[5]!="-s"):
        raise errorMessageInput
    if(len(userInput)==9):
        if(userInput[7]!="-f"):
            raise errorMessageInput 
        if((userInput[8]!="number") and (userInput[8]!="keywords")):
            raise errorMessageInput
        if(userInput[8]=="number"):
            feature = "NUMBER"
        else:
            feature = "KEYWORDS"

    train_data = readData(userInput[2])
    test_data = readData(userInput[4])
    smoothing_param = float(userInput[6]) #make sure smoothing value is float and not str
    # print(type(smoothing_param))

    probDicValues, probSpam, probHam, spamTotal, hamTotal = countAndOrganizeWords(train_data, smoothing_param, feature)
    answerList = classifyTestData(test_data, probDicValues, probSpam, probHam, spamTotal, hamTotal, smoothing_param, feature)
    dicWrong, dicCategory = overallErrorTest(test_data, answerList)
    printOverallError(dicWrong, dicCategory)


except errorMessageInput:
    print("Sorry, your input is incorrect.")
except ValueError:
    print("Sorry, your input is incorrect.")
except FileNotFoundError:
    print("Sorry, the files you specified do not exist.")
# python q2_classifier.py -f1 spam_data/train -f2 spam_data/test -s 1 
# python q2_classifier.py -f1 spam_data/train -f2 spam_data/test -s 1 -f number

