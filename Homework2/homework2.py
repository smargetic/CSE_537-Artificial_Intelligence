import sys
import backtracking
import copy
import sys

class error_incorrect_input(Exception):
    pass

def checkInput(inputArray, nmkArray):
    #rows
    for i in range(0,len(inputArray)):
        tempArray = []
        for j in range(0,len(inputArray[i])):
            if(inputArray[i][j]!="_"):
                if(inputArray[i][j] in tempArray):
                    raise error_incorrect_input
                tempArray.append(inputArray[i][j])
    
    tempArray = []
    for i in range(0,len(inputArray[0])):
        tempArray.append([])
    #columns
    for i in range(0, len(inputArray)):
        for j in range(0,len(inputArray[i])):
            if(inputArray[i][j]!="_"):
                if(inputArray[i][j]in tempArray[j]):
                      raise error_incorrect_input                  
                tempArray[j].append(inputArray[i][j])


    #box
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

    for i in range(0,len(squareValues)):
        temp = 1
        while(temp<=nmkArray[0]):
            answer = squareValues[i].count(temp)
            if(answer>1):
                raise error_incorrect_input
            temp+=temp


try:
    # fileName = input("Please proved the file you would like to read: \n")
    fileName = sys.argv[1]
    # fileName = "testInput7.txt"
    #reads file
    with open(fileName, 'r') as f:
        contents = f.read()

    #each line is a new array
    contents = contents.replace(" ", "")
    newContents = contents.split("\n")
    #extra line
    if(newContents[-1]==''):
        newContents.pop()

    #each element was previously seperated by a comma
    inputArray = []
    for i in range(0,len(newContents)):
        temp = newContents[i].split(",")
        inputArray.append(temp)

    #convert string of numbers to numbers
    for i in range(0,len(inputArray)):
        for j in range(0, len(inputArray[i])):
            try:
                inputArray[i][j] = int(inputArray[i][j])
            except ValueError:
                pass

    # make sure only m,n,k are provided
    if (len(inputArray[0])!=3):
        raise error_incorrect_input
    
    n = inputArray[0][0]
    m = inputArray[0][1]
    k = inputArray[0][2]

    #make sure all values are right format
    if((type(n)!=int)or(type(m)!=int)or(type(k)!=int)):
        raise error_incorrect_input

    #make sure value of n,m, and k are provided and correct
    if((m*k)!=n):
        raise error_incorrect_input

    # rows and columns have value of n
    if((len(inputArray)-1)!=n):
        raise error_incorrect_input

    for i in range(1,len(inputArray)):
        if(len(inputArray[i])!=n):
            raise error_incorrect_input

    nmkArray = inputArray.pop(0)
    
    #make sure values are correct
    for i in range(0,len(inputArray)):
        for j in range(0,len(inputArray[i])):
            if(type(inputArray[i][j])==int):
                if(inputArray[i][j]>n):
                    raise error_incorrect_input
            else:
                if(inputArray[i][j]!='_'):
                    raise error_incorrect_input

    checkInput(inputArray, nmkArray)
    print("Which would you like to implement: ")
    print("\t1. Backtracking + MRV heuristic")
    print("\t2. Backtracking + MRV + Forward Checking")
    print("\t3. Backtracking + MRV + Constraint Propagation")
    num = input("")
    
    temp = "None"
    if(num=="2"):
        temp="FC"
    elif(num=="3"):
        temp ="CP"
    
    backtracking.backtracking(inputArray, nmkArray,temp)


except error_incorrect_input:
    print("\nIncorrect input, please try again!\n")
except FileNotFoundError:
    print("\nThis file does not exist, please try again!\n")





# testInput2.txt
# testInput.txt