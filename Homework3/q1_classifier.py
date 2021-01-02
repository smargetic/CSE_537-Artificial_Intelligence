import sys
import csv
from scipy.stats import chi2
import copy
import math

#wrong input
class errorMessageInput(Exception):
    pass

class Tree:
    def __init__(self):
        self.right = None
        self.left = None
        self.data = None
        self.attributeList = None
        self.splitVal = None
        self.parent = None
        self.attribute = None

#reads data and puts into array format
def readData(fileName, output=False): #PUT INTO SEPERATE FILE
    data = []
    with open(fileName, newline='') as csvfile:
        tempData = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in tempData:
            if(output==True):
                data.append(int(row[0]))
            else:
                data.append(row)
    return data


def turnCurrentDataSetToDic(data):
    dic = {}
    for i in range(0,len(data)):
        dic[i] = data[i]

    return dic

#sees if there is a uniform outout or not ==> tell if leaf
def uniformOutput(current_data_set, output):
    outputList = []
    for i in current_data_set.keys():
        if(output[i] not in outputList):
            outputList.append(output[i])
        if(len(outputList)>1):
            return False
    return True

#if it is possible to split
def uniformAttribute(current_data_set, attributeIndex):
    valueList = []
    for i in current_data_set.keys():
        if(current_data_set[i][attributeIndex] not in valueList):
            valueList.append(current_data_set[i][attributeIndex] )
        if(len(valueList) > 1):
            return False
    return True

#count the number of output zeros based on data
def countOutputZeros(data, output):
    zeroCount = 0
    for i in data.keys():
        if(output[i] == 0):
            zeroCount = zeroCount +1
    return zeroCount

#splits original data based on an attribute split value, produces 2 new sets   
def splitData(origData, splitValue, attributeIndex):
    attributeValuesDic = {"SET 1": {}, "SET 2": {}}
    for i in origData.keys():
        if(int(origData[i][attributeIndex])<=splitValue):
            attributeValuesDic["SET 1"][i] = origData[i]
        else:
            attributeValuesDic["SET 2"][i] = origData[i]


    return attributeValuesDic

# calculates p value based on splitting children
def chiSquareGain(parent_data, children, output):
    nParent = len(list(parent_data.keys()))
    zeroCountParent = countOutputZeros(parent_data, output)
    chiSquare = 0
    #calculate chi square for each child
    for i in range(0,len(children)):
        nChild = len(list(children[i].keys()))
        zeroCountChild = countOutputZeros(children[i], output)
        oneCountChild = nChild - zeroCountChild
        expectedZeroChild = (nChild/nParent)*zeroCountParent
        expectedOneChild = (nChild/nParent)*(nParent-zeroCountParent) #nparent - zero count = one count

        chiSquare = chiSquare + (((expectedZeroChild-zeroCountChild)**2)/expectedZeroChild) #zeros
        chiSquare = chiSquare + (((expectedOneChild-oneCountChild)**2)/expectedOneChild) #ones

    pval = chi2.sf(chiSquare, 1)
    return pval

#calculates p value for each split on a particular attribute, returns split value
def chiSquareSplit(currentDataSet, attributeIndex, output):
    #find possible values of attribute we're splitting over
    possibleValuesList = []
    for i in currentDataSet.keys():    
        if(int(currentDataSet[i][attributeIndex]) not in possibleValuesList):
            possibleValuesList.append(int(currentDataSet[i][attributeIndex]))
    
    possibleValuesList.sort() #in order
    pValList = []
    # listOfChildren = []
    #calculated p value at every split
    for i in range(0,len(possibleValuesList)-1):
        splitVal = possibleValuesList[i]
        child1 = {}
        child2 = {}
        #calculate chi square and p value split children
        for j in currentDataSet.keys():
            if(int(currentDataSet[j][attributeIndex])<=splitVal):
                child1[j] = currentDataSet[j]
            else:
                child2[j] = currentDataSet[j]

        pVal = chiSquareGain(currentDataSet,[child1,child2], output)
        pValList.append(pVal)

    splitVal = possibleValuesList[pValList.index(min(pValList))] #returned largest pValue

    return float(splitVal), min(pValList)

#calculate entropy after split
def entropyAfterSplit(parent_data, children, output):
    totalAll = len(children[0]) + len(children[1])
    entropy = 0
    for i in range(0,len(children)):
        #since binary split entropy is only two values
        zeroCount = countOutputZeros(children[i], output)
        total = len(children[i])

        probZero = zeroCount/total
        probOne = (total - zeroCount)/total

        if((probOne!=0) and (probZero!=0)):
            entropy = entropy + ((total/totalAll)*((-probZero*math.log(probZero,2))-(probOne*math.log(probOne,2))))

    return entropy

#calculate entropy of node
def entropyOfNode(parent_data, output):
    zeroCount = countOutputZeros(parent_data, output)
    total = len(parent_data)
    oneCount = total - zeroCount
    probZero = zeroCount/total
    probOne = oneCount/total

    entropy = -probOne*math.log(probOne, 2) - probZero*math.log(probZero,2)

    return entropy

#find minimum entropy over various splits
def minEntropyForSplits(parent_data, output, attributeIndex):
    listAttributeVals = []
    for i in parent_data.keys():
        #get possible attribute values
        if(int(parent_data[i][attributeIndex]) not in listAttributeVals):
            listAttributeVals.append(int(parent_data[i][attributeIndex]))
    listAttributeVals.sort()
    entropyList = []
    for i in range(0,len(listAttributeVals)-1):
        child1 = {}
        child2 = {}
        for j in parent_data.keys():
            if(int(parent_data[j][attributeIndex])<=listAttributeVals[i]):
                child1[j] = parent_data[j]
            else:
                child2[j] = parent_data[j]
        entropyVal = entropyAfterSplit(parent_data, [child1, child2], output)
        entropyList.append(entropyVal)

    listAttributeVals[entropyList.index(min(entropyList))]
    return listAttributeVals[entropyList.index(min(entropyList))], min(entropyList)


def id3Algorithm(train_data_set, current_data_set, output, p):
    numberOfAttributes = len(current_data_set[0])

    #initialize tree
    root = Tree()
    root.data = current_data_set
    root.attributeList = []
    treeList = [root]
    root.attribute = -1

    while(treeList!=[]):
        currentNode = treeList.pop()
        current_data_set = currentNode.data

        if(not uniformOutput(current_data_set, output)): #same out put = leaf
            listOfPassingAttributes = []
            for i in range(0,numberOfAttributes): #see if each attribute passes the p value
                if(not uniformAttribute(current_data_set, i)): #same attribute = cannot split
                    #for each attribute, calculate p-value for each split, return min
                    tempSplitVal, tempPval = chiSquareSplit(current_data_set, i, output)
                    if(tempPval<p):
                        listOfPassingAttributes.append([i,tempSplitVal])
            
            gain = -sys.maxsize
            splitVal = -sys.maxsize
            attributeIndex = -1
            entropy_parent = entropyOfNode(current_data_set, output)
            for i in range(0,len(listOfPassingAttributes)): #go through attributes that passed and calculate information gain
                attributeValuesDic = splitData(current_data_set, listOfPassingAttributes[i][1], listOfPassingAttributes[i][0])
                entropy_split = entropyAfterSplit(current_data_set, [attributeValuesDic["SET 1"], attributeValuesDic["SET 2"]], output)
                tempGain = entropy_parent - entropy_split
                if(tempGain>gain):
                    gain = tempGain
                    splitVal = listOfPassingAttributes[i][1]
                    attributeIndex = listOfPassingAttributes[i][0]

            if(gain>0): #there is some gain for the next node
                attributeValuesDic = splitData(current_data_set, splitVal, attributeIndex)

                currentNode.attribute = attributeIndex
                currentNode.splitVal = splitVal
                #left
                currentNode.left = Tree()
                currentNode.left.data = attributeValuesDic["SET 1"]
                treeList.append(currentNode.left)
                #right
                currentNode.right = Tree()
                currentNode.right.data = attributeValuesDic["SET 2"]
                treeList.append(currentNode.right)
    return root

#finds the size of the current tree
def sizeOfTree(root):
    treeList = [root]
    count = 0
    while(treeList!=[]):
        current_node = treeList.pop()
        count = count +1
        if(current_node.left!=None):
            treeList.append(current_node.left)
        if(current_node.right!=None):
            treeList.append(current_node.right)

    return count

#which is more probable based on the data set, 1 or 0
def probability(data, output):
    zeroCount = 0
    totalCount = 0
    for i in data.keys():
        if(output[i]==0):
            zeroCount = zeroCount +1

    oneCount = totalCount - zeroCount

    if(zeroCount>oneCount):
        return 0
    return 1

#classifies all test data
def classifyTest(root, test_data, train_output):
    labelsList = []
    for i in range(0,len(test_data)):
        pointer = root
        parent = None
        while (pointer!=None):
            splitValue = pointer.splitVal
            if(splitValue != None):
                attributeValue = pointer.attribute
                if(float(test_data[i][attributeValue]) <=splitValue): #follow the tree left
                    parent = pointer
                    pointer = pointer.left
                else:
                    parent = pointer
                    pointer = pointer.right
            else:
                parent = pointer
                pointer = None
        labelsList.append(probability(parent.data, train_output)) #get the most probable

    return labelsList

#print calculates the amount misclassified
def errorAnalysis(labelsList, test_labels):
    errors =0
    dic = {"TRUE NEG": 0, "TRUE POS": 0, "FALSE NEG": 0, "FALSE POS": 0}
    for i in range(0,len(labelsList)):
        if(labelsList[i]!=test_labels[i]):
            errors = errors +1
        
        if(labelsList[i]==0):
            if(test_labels[i]==0):
                dic["TRUE NEG"] = dic["TRUE NEG"] + 1
            else:
                dic["FALSE NEG"] = dic["FALSE NEG"] + 1
        else:
            if(test_labels[i]==1):
                dic["TRUE POS"] = dic["TRUE POS"] + 1
            else:
                dic["FALSE POS"] = dic["FALSE POS"] + 1
    
    accuracy = (dic["TRUE NEG"]+dic["TRUE POS"])/(dic["TRUE NEG"] + dic["FALSE NEG"] + dic["TRUE POS"] + dic["FALSE POS"])
    return errors, accuracy

#prints errors
def printErrors(errors, total, accuracy):
    print("\nNumber Of Errors: " + str(errors))
    print("Total Labels: " + str(total))
    print("\tPERCENT ERROR: "+ str((errors/total)*100))
    print("\tACCURACY: " + str(accuracy))

truth = 0
userInput = sys.argv
try:
    if(len(userInput)!=11):
        raise errorMessageInput

    p = float(userInput[2]) #make sure p value is float and not str

    #flags
    if(userInput[1]!= "-p"):
        raise errorMessageInput
    if(userInput[3]!="-f1"):
        raise errorMessageInput
    if(userInput[5]!="-f2"):
        raise errorMessageInput
    if(userInput[7]!="-o"):
        raise errorMessageInput
    if(userInput[9]!="-to"):
        raise errorMessageInput

    train_data = turnCurrentDataSetToDic(readData(userInput[4]))
    test_data = readData(userInput[6])
    output = readData(userInput[8], True)
    test_output = readData(userInput[10], True)

    current_data_set = turnCurrentDataSetToDic(train_data)
    root = id3Algorithm(train_data, current_data_set, output, p)
    labelsList = classifyTest(root, test_data, output)
    errors, accuracy = errorAnalysis(labelsList, test_output)
    printErrors(errors, len(labelsList), accuracy)
    print("\nSize of tree: " + str(sizeOfTree(root)))


except errorMessageInput:
    print("Sorry, your input is incorrect.")
except ValueError:
    print("Sorry, your input is incorrect.")
except FileNotFoundError:
    print("Sorry, the files you specified do not exist.")

#python q1_classifier_final.py -p 1 -f1 clickstream-data/train.csv -f2 clickstream-data/test.csv -o clickstream-data/train_label.csv -to clickstream-data/test_label.csv