import copy


#mrv = minimum remaining values
stackOfSuduko = []
exploredNodes = []
answer = []

#prints answer nicely
def printAnswer(count):
    global answer
    print("\n")
    if(answer!=[]):
        for i in range(0,len(answer)):
            for j in range(0,(len(answer[i])-1)):
                temp = str(answer[i][j]) + ","
                print(temp, end=' ')
            print(str(answer[i][len(answer[i])-1]))

        print("\nNumber of Conistency Checks: " + str(count)+ "\n")
    else:
        print("There is no solution to this input.")

#checks if the sudoku puzzle structure is the solution
def isAnswer(inputArray):
    for i in range(0,len(inputArray)):
        for j in range(0,len(inputArray[i])):
            if inputArray[i][j] == "_":
                return False
    return True


#generates arrays representing suduko puzzle with new inputs (ie. "values")
def generateNewPuzzle(inputArray, location, values):
    count = 0
    arrayOfNew = []
    for i in range(0,len(inputArray)):
        for j in range(0, len(inputArray[i])):
            if(count == location):
                for m in values:
                    tempInputArray = copy.deepcopy(inputArray)
                    tempInputArray[i][j] = m
                    arrayOfNew.append(tempInputArray)
            count = count +1
    return arrayOfNew

#checks to see if there is an empty spot in the list of remaining values
def forwardChecking(remainingValues):
    for i in range(0,len(remainingValues)):
        for j in range(0,len(remainingValues[i])):
            if remainingValues[i][j]== []:
                return False
    return True

#constraint propogation
def arcConsistency(remainingValues, nmkArray):
    count = 0
    remainingValuesCopy = copy.deepcopy(remainingValues)
    for i in range(0,len(remainingValuesCopy)):
        for j in range(0,len(remainingValuesCopy[i])):
            #if there is one value, make sure it's edges are consistent
            if((len(remainingValuesCopy[i][j])==1) and(remainingValuesCopy[i][j]!=[-1])):
                change =1
                #until no values need to be changed, ie consistent
                while(change==1):
                    change =0
                    #makes sure row is consistent
                    for m in range(0,len(remainingValuesCopy[i])):
                        if(m!=j):
                            if(remainingValuesCopy[i][j][0] in remainingValuesCopy[i][m]):
                                #remove
                                remainingValuesCopy[i][m].remove(remainingValuesCopy[i][j][0])
                                change = 1
                    if(not forwardChecking(remainingValuesCopy)):
                        return []
                    #makes sure column is consistent
                    for m in range(0,len(remainingValuesCopy)):
                        if(m!=i):
                            if(remainingValuesCopy[i][j][0] in remainingValuesCopy[m][j]):
                                #remove
                                remainingValuesCopy[m][j].remove(remainingValuesCopy[i][j][0])
                                change = 1

                    if(not forwardChecking(remainingValuesCopy)):
                        return []   
                    #makes sure box is consistent
                    mValue = int(count/(nmkArray[0]*nmkArray[1]))
                    row = mValue*nmkArray[1]
                    temp = nmkArray[0]*nmkArray[1]
                    temp2 = count%temp
                    kValue = int((temp2%nmkArray[0])/nmkArray[2])
                    count2 = 0
                    for m in range(row, (row+nmkArray[1])):
                        for t in range(0,len(remainingValuesCopy[m])):
                            if(t>=(kValue*nmkArray[2]) and (t<((kValue+1)*nmkArray[2]))):
                                if(count2!=temp2):
                                    if(remainingValuesCopy[i][j][0] in remainingValuesCopy[m][t]):
                                        remainingValuesCopy[m][t].remove(remainingValuesCopy[i][j][0])
                                        change = 1
                            count2 = count2 +1

                    if(not forwardChecking(remainingValuesCopy)):
                        return []
            count = count +1            
    return remainingValuesCopy

#find location where minimum remaining value (mrv) is
def mrv(inputArray, nmkArray, additional = "None"):
    #numbers that are possibe to have in the puzzle
    allPossibleValues = []
    for i in range(1,(nmkArray[0]+1)):
        allPossibleValues.append(i)

    remainingValues = []
    
    #for each row
    for i in range(0,len(inputArray)):
        presentNumbers = []
        for j in range(0,len(inputArray[i])):
            if(inputArray[i][j]!="_"):
                presentNumbers.append(inputArray[i][j])
        
        tempRemainingValue = []
        for j in range(0,len(allPossibleValues)):
            if(allPossibleValues[j] not in presentNumbers):
                tempRemainingValue.append(allPossibleValues[j])

        arrayTempRemainingValue = []
        for j in range(0,nmkArray[0]):
            if(inputArray[i][j]=="_"):
                arrayTempRemainingValue.append(tempRemainingValue)
            else:
                arrayTempRemainingValue.append([-1])

        remainingValues.append(arrayTempRemainingValue)

    #for each column
    for i in range(0,len(inputArray)):
        for j in range(0,len(inputArray[i])):
            if(inputArray[i][j]!="_"):
                for m in range(0,nmkArray[0]):
                    try:
                        temp = copy.deepcopy(remainingValues[m][j]) #because they were linked together before
                        temp.remove(inputArray[i][j])
                        remainingValues[m][j] = temp
                    except ValueError:
                        pass        
    #for each square
    squareValues = []
    count = 1
    numberSquareHoriz = int(nmkArray[0]/nmkArray[2])
    #get box values by getting a certain number of rows constraint to a certain amount of columns
    for i in range(0,len(inputArray)):
        for j in range(0,numberSquareHoriz):
            array = []
            #get each row values for each box
            if(j==0):
                array = copy.deepcopy(inputArray[i][:nmkArray[2]])
            elif(j==(numberSquareHoriz-1)):
                num = (numberSquareHoriz-1)*nmkArray[2]
                array = copy.deepcopy(inputArray[i][num:])
            else:
                begin = j*nmkArray[2]
                end = (j+1)*nmkArray[2]
                array = copy.deepcopy(inputArray[i][begin:end])         

            #get only numbers
            array2 = []
            for m in range(0,len(array)):
                if(array[m]!="_"):
                    array2.append(array[m])

            if(count ==1):
                squareValues.append(array2)
            #if another line is part of previous box
            else:
                for m in array2:
                    squareValues[-numberSquareHoriz+j].append(m)
        #count goes up to m value
        if(count!=nmkArray[1]):
            count = count +1
        else:
            count =1
    countM =0
    countMHelper = 1
    #if element in square is option, remove it
    for i in range(0,len(remainingValues)):
        countK = 0
        for j in range(0,len(remainingValues[i])):
            temp = []
            for m in remainingValues[i][j]:
                if m not in squareValues[int(countK/nmkArray[2])+ (countM*numberSquareHoriz)]:
                    temp.append(m)
            remainingValues[i][j] = temp
            countK = countK +1

        if(countMHelper==nmkArray[1]):
            countM = countM+1
            countMHelper = 1
        else:
            countMHelper = countMHelper +1

    #if constraint proprogation is done, adjust remaining values accordingly
    if(additional=="CP"):
        remainingValues = arcConsistency(remainingValues,nmkArray)
        if(remainingValues == []):
            return []
    
    #location of least remaining value
    minValueLoc = -1
    minValueSize = 1000000
    values = []
    count = 0
    for i in range(0,len(remainingValues)):
        for j in range(0,len(remainingValues[i])):
            if((len(remainingValues[i][j])<minValueSize) and (remainingValues[i][j]!=[-1]) and(remainingValues[i][j]!=[])):
                minValueLoc = count
                values = remainingValues[i][j]
                minValueSize = len(remainingValues[i][j])
            count = count +1

    #if forward checking is done, see if empty set of remaining values is present, if so, don't go further
    newInputArrays = []
    if(additional=="FC"):
        if(forwardChecking(remainingValues)):
            newInputArrays = generateNewPuzzle(inputArray,minValueLoc,values)
    else:
        newInputArrays = generateNewPuzzle(inputArray,minValueLoc,values)

    return newInputArrays


def backtracking(inputArray, nmkArray, additional="None"):
    global stackOfSuduko
    global answer
    global exploredNodes
    stackOfSuduko.append(inputArray)

    truth=0
    count = 0

    while((len(stackOfSuduko)!=0)and(truth==0)):
        #initialize suduko
        inputSuduko = stackOfSuduko.pop()
        exploredNodes.append(inputSuduko)

        #check if answer
        if(isAnswer(inputSuduko)):
            truth=-1
            answer = inputSuduko
        else:
        #if not answer, search for answer
            newInputArrays = mrv(inputSuduko, nmkArray, additional)
            count = count +1
            if(newInputArrays!=[]):
                for inp in newInputArrays:
                    if(inp not in exploredNodes):
                        stackOfSuduko.append(inp)
    printAnswer(count)





    


