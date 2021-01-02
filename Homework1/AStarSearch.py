# import userInput
import functionsForBothSearches
import copy
import os
import psutil
import time



queue = []
exploredInput = []
startTime = time.time()

class answerFoundException(Exception):
    pass

def xYPositions(input):
    listOfXYPositions = []
    for i in range(0,len(input)):
        for j in range(0,len(input[i])):
            if(input[i][j]=="X"):
                listOfXYPositions.append([i,j])
    
    return listOfXYPositions

#heurstic 1
def manhattanDistance(input):
    sum = 0
    listOfXYPositions = xYPositions(input)
    
    for i in range(0,len(listOfXYPositions)):
        for j in range(i, len(listOfXYPositions)):
            tempi = listOfXYPositions[i]
            tempj = listOfXYPositions[j]
            sum = sum + abs(tempi[0]-tempj[0])+ abs(tempi[1]-tempj[1])

    return sum

#heuristic 2
def numberOfMoveablePegs(input):
    movesList = functionsForBothSearches.nextMoves(input)
    return len(movesList)
        
#heuristic 3 ==> corner bias
#center position is at 16 (ie. (3,3))
def distanceFromCenter(input):
    sum = 0
    xYPositionsList = xYPositions(input)
    for i in range(0, len(xYPositionsList)):
        sum = sum + abs(xYPositionsList[i][0]-3) + abs(xYPositionsList[i][1]-3)
    
    return sum

def aStarSearch(heuristic, input):
    #check if input is answer
    if((functionsForBothSearches.isAnswer(input))or(functionsForBothSearches.checkIfXs(input)==False)):
        val = 1
        if(functionsForBothSearches.checkIfXs(input)==False):
            val = 0
        functionsForBothSearches.printSolution([], heuristic, val)
        process = psutil.Process(os.getpid())
        functionsForBothSearches.printAdditional(startTime, 1, process.memory_info().rss)
        raise answerFoundException
    
    start = 0
    end = 1
    if(heuristic==2):
        start = 1
        end = 2
    elif(heuristic ==3):
        start =2
        end = 3
    elif(heuristic ==4):
        end = 3
    
    global queue
    global exploredInput
    for i in range(start,end):
        queue = []
        exploredInput = [input]
        cost = 0
        if(i ==0):
            cost = manhattanDistance(input)
        elif(i==1):
            cost = numberOfMoveablePegs(input)
        elif(i==2):
            cost = distanceFromCenter(input)

        dic = {"INPUT": input, "MOVES": [], "COST": cost, "DEPTH": 0}
        queue.append(dic)
        answerFound = 0
        count = 1
        depth = 0
        while ((queue!=[]) and (answerFound==0)):
            costMin = 1000000000
            locationOfMin = -1
            #find the node with the least cost
            for j in range(0, len(queue)):
                if(queue[j]["COST"]<costMin):
                    costMin = queue[j]["COST"]
                    locationOfMin = j
            
            #check if the least cost is the answer
            if(functionsForBothSearches.isAnswer(queue[locationOfMin]["INPUT"])):
                answerFound = 1
                moves = functionsForBothSearches.convertPositions(queue[locationOfMin]["MOVES"])
                functionsForBothSearches.printSolution(moves, (i+1), 0)
                process = psutil.Process(os.getpid())
                functionsForBothSearches.printAdditional(startTime, count, process.memory_info().rss)
            else:  
                #based on the least cost, I produce it's children and add them to the queue
                tempInput = copy.deepcopy(queue[locationOfMin]["INPUT"]) #NOT SURE IF NEEDED
                movesList = functionsForBothSearches.nextMoves(tempInput)
                
                #add parent to explored list
                exploredInput.append(queue[locationOfMin]["INPUT"])
                for j in range(0,len(movesList)):
                    tempList = copy.deepcopy(queue[locationOfMin]["INPUT"])
                    newList = functionsForBothSearches.produceNewInputList(tempList, movesList[j])
                    
                    #we have not explored this option before
                    if(newList not in exploredInput):
                        cost = 0
                        newDepth = queue[locationOfMin]["DEPTH"] +1
                        #generate cost for new list
                        if(i ==0):
                            cost = manhattanDistance(newList) + newDepth
                        elif(i==1):
                            cost = numberOfMoveablePegs(newList) + newDepth
                        elif(i==2):
                            cost = distanceFromCenter(newList) + newDepth


                        #calculate the moves for the list
                        moves = []
                        if(queue[locationOfMin]["MOVES"]!=[]):
                            for items in queue[locationOfMin]["MOVES"]:
                                moves.append(items)
                        moves.append(movesList[j])

                        dic = {"INPUT": newList, "MOVES": moves, "COST": cost, "DEPTH": newDepth}
                        count = count+1

                        queue.append(dic)

            #remove previously lowest cost
            queue.pop(locationOfMin)
        #All nodes have been explored, there is no solution 
        if(answerFound==0): 
            functionsForBothSearches.printSolution([], (i+1), 0)
            process = psutil.Process(os.getpid())
            functionsForBothSearches.printAdditional(startTime, count, process.memory_info().rss)   
    

    
    

#< - - 0 0 0 - -, - - 0 X 0 - - , 0 0 X X X 0 0, 0 0 0 X 0 0 0, 0 0 0 X 0 0 0, - - 0 0 0 - -, - - 0 0 0 - - >

