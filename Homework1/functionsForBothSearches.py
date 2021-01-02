# import userInput
import time
import os
import psutil
import copy

arrayOfBlankSpaces = [1,2,6,7,8,9,13,14,36,37,41,42,43,44,48,49]
edgeTop = [3,4,5]
edgeRight = [21,28,35]
edgeBottom = [45,46,47]
edgeLeft = [15,22,29]


#sees if input (array) is a valid solution
def isAnswer(input):
    xFoundFlag = 0
    for i in range(0,len(input)):
        for j in range(0,len(input[i])):
            if(input[i][j]=="X"):
                xFoundFlag = xFoundFlag+1
            if(xFoundFlag>1):
                return False
    # if(xFoundFlag ==0):
    #     return False
    return True

def checkIfXs(input):
    xFoundFlag = 0
    for i in range(0,len(input)):
        for j in range(0,len(input[i])):
            if(input[i][j]=="X"):
                xFoundFlag = xFoundFlag+1
    if(xFoundFlag ==0):
        return False
    return True    

#finds valid moves based on pegs that are next to one another (2nd from left or 2nd from right can move)
def produceMovesList(input, xOrY, movesList):
    difference = 0

    if(xOrY ==0):
        difference = 2
    else:
        difference = 14
    
    for i in range(0,len(input)):
        if(len(input[i])>1):
            #moving the second from the front and second from the back are valid moves 
            # as long as it is not a blank spot or dne
            inputLeftOrTop = input[i][1]
            inputRightOrBottom = input[i][-2]

            newLeftOrTopPosition = input[i][1]-difference
            newRightOrBottomPosition = input[i][-2]+difference

            if(xOrY ==0):
                if((newLeftOrTopPosition not in arrayOfBlankSpaces) and (input[i][0] not in edgeLeft)):
                    movesList.append([inputLeftOrTop, newLeftOrTopPosition])
                
                if((newRightOrBottomPosition not in arrayOfBlankSpaces) and (input[i][-1] not in edgeRight)):
                    movesList.append([inputRightOrBottom, newRightOrBottomPosition])
            else:
                if((newLeftOrTopPosition not in arrayOfBlankSpaces) and (input[i][0] not in edgeTop)):
                    movesList.append([inputLeftOrTop, newLeftOrTopPosition])
                
                if((newRightOrBottomPosition not in arrayOfBlankSpaces) and (input[i][-1] not in edgeBottom)):
                    movesList.append([inputRightOrBottom, newRightOrBottomPosition])
    
    return movesList

#takes array of positions, and the move you wish to perform
#outputs a new array of positions
def produceNewInputList(input, move):
    position2Remove = (move[0]+move[1])/2

    index1 = int((position2Remove-1)/7)
    index2 = (int(position2Remove)%7)-1

    input[index1] = input[index1][:index2] + '0' + input[index1][(index2+1):]

    index1 = int((move[0]-1)/7)
    index2 = int(move[0]%7)-1

    input[index1] = input[index1][:index2] + '0' + input[index1][(index2+1):]

    index1 = int((move[1]-1)/7)
    index2 = int(move[1]%7)-1
    input[index1] = input[index1][:index2] + 'X' + input[index1][(index2+1):]

    return input

#takes in input (array) and returns a list of valid moves
def nextMoves(input):
    position = 1
    xConcurrent = []
    yConcurrent = []

    for i in range(0,len(input)):
        for m in range(0,len(input)):
            #if an x is found, search xConcurrent to see if there is a peg next to it, add it to sublist
            if input[i][m]=="X":
                if (len(xConcurrent)==0):
                    xConcurrent.append([position])
                else:
                    if((position - xConcurrent[-1][-1])==1): #different in x to be aligned = 1
                        xConcurrent[-1].append(position)
                    else:
                        xConcurrent.append([position])

                
                if (len(yConcurrent)==0):
                    yConcurrent.append([position])
                else:
                    dif7Flag = 0
                    for j in range(0,len(yConcurrent)):
                        if((position - yConcurrent[j][-1])==7): #different in y to be aligned = 1
                            yConcurrent[j].append(position)
                            dif7Flag =1
                    if(dif7Flag==0):
                        yConcurrent.append([position])
            position = position+1

    movesList = []
    movesList = produceMovesList(xConcurrent, 0, movesList)
    movesList = produceMovesList(yConcurrent, 1, movesList)    

    return movesList

#i used a differnt indexing then was instructed
def convertPositions(inputList):
    for i in range(0,len(inputList)):
        for j in range(0,len(inputList[i])):
            if(inputList[i][j]<=5):
                inputList[i][j] = inputList[i][j]-3
            elif(inputList[i][j]<=12):
                inputList[i][j] = inputList[i][j]-7
            elif(inputList[i][j]<=35):
                inputList[i][j] = inputList[i][j]-9
            elif(inputList[i][j]<=40):
                inputList[i][j] = inputList[i][j]-11
            elif(inputList[i][j]<=47):
                inputList[i][j] = inputList[i][j]-15
    return inputList


#formating
#print single solution
def printSolution(solution, i, inputAnswer):
    if(i==-1):
        print("\nSOLUTION:")
    elif(i==1):
        print("\nSOLUTION WITH MANHATTAN DISTANCE HEURISTIC:")
    elif(i==2):
        print("\nSOLUTION WITH NUMBER OF MOVEABLE PEGS HEURISTIC:")
    elif(i==3):
        print("\nSOLUTION WITH DISTANCE FROM CENTER (CENTER BIAS) HEURISTIC:")
    elif(i==4):
        print("\nSOLUTION FOR ALL FOUR:")
    if(solution==[]):
        if(inputAnswer==1):
            print("< >")
            print("The input was a solution.")
        else:
            print("< >")
            print("No solution was found.")

    else:
        print("< ", end="")
        for i in range(0,len(solution)-1):
            print("( " + str(solution[i][0]) + " , " + str(solution[i][1]) + " ), ", end="")
        print("( " + str(solution[len(solution)-1][0]) + " , " + str(solution[len(solution)-1][1]) + " )", end="")
        print(" >")

#additional information about search algorithm run
def printAdditional(startTime, numberOfNodes, memory):
    TimeToRun = time.time() - startTime #should take only a certain number of digits
    print("\nTime to Complete: "+ str(TimeToRun) + " seconds")
    print("Number of Nodes Expanded: " + str(numberOfNodes))
    print("Memory in bytes: " + str(memory) + "\n")