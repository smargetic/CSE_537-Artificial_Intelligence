# import userInput
import time
import os
import psutil
import copy
import functionsForBothSearches
# from guppy import hpy


startTime = time.time()
nodeCount = 0
stack = []
globalMoveList = []



class answerFoundException(Exception):
    pass


def iterativeDeepeningSearch(input):
    # if the original input has the answer
    if((functionsForBothSearches.isAnswer(input))or(functionsForBothSearches.checkIfXs(input)==False)):
        val = 1
        if(functionsForBothSearches.checkIfXs(input)==False):
            val = 0

        functionsForBothSearches.printSolution([], -1, val)
        process = psutil.Process(os.getpid())
        functionsForBothSearches.printAdditional(startTime, 1, process.memory_info().rss)
        raise answerFoundException

    count = 1
    listOfNodes = [[{"INPUT": input, "MOVES": []}]]


    while(listOfNodes!=[]):
        for i in range(0,len(listOfNodes[0])):

            #produce children
            copyListOfNodes = copy.deepcopy(listOfNodes[0][i]["INPUT"])
            movesList = functionsForBothSearches.nextMoves(copyListOfNodes)

            childrenList = []
            for j in range(0, len(movesList)):
                copyListOfNodes = copy.deepcopy(listOfNodes[0][i]["INPUT"])
                newList = functionsForBothSearches.produceNewInputList(copyListOfNodes, movesList[j])

                temp = []
                #calculate the moves for the list
                if(listOfNodes[0][i]["MOVES"]!=[]):
                    for items in listOfNodes[0][i]["MOVES"]:
                        temp.append(items)
                temp.append(movesList[j])

                #I check if the child is a possible solution ==> MORE EFFICIENT, but commented out because 
                #all sources seem to say that a list of children is made before checking them for this algorithm

                # count = count+1
                # if(functionsForBothSearches.isAnswer(newList)):
                #     answerList = functionsForBothSearches.convertPositions(temp)
                #     functionsForBothSearches.printSolution(answerList, -1)
                #     process = psutil.Process(os.getpid())
                #     functionsForBothSearches.printAdditional(startTime, count, process.memory_info().rss)
                #     raise answerFoundException
                
                childrenList.append({"INPUT": newList, "MOVES": temp})


            # where i make the entire list first and then check if solution
            for j in range(0,len(childrenList)):
                count = count +1
                if(functionsForBothSearches.isAnswer(childrenList[j]["INPUT"])):
                    answerList = functionsForBothSearches.convertPositions(childrenList[j]["MOVES"])
                    functionsForBothSearches.printSolution(answerList, -1, 0)
                    process = psutil.Process(os.getpid())
                    functionsForBothSearches.printAdditional(startTime, count, process.memory_info().rss)
                    raise answerFoundException
            if((childrenList!=[]) and (temp!=listOfNodes[0][i]["MOVES"])): #what is temp?? ==> see if runs
                listOfNodes.append(childrenList)

        listOfNodes.pop(0)

    #All nodes have been explored, there is no solution  
    functionsForBothSearches.printSolution([], -1, 0) 
    process = psutil.Process(os.getpid())
    functionsForBothSearches.printAdditional(startTime, count, process.memory_info().rss)       




# < - - 0 0 0 - -, - - 0 X 0 - - , 0 0 X X X 0 0, 0 0 0 X 0 0 0, 0 0 0 X 0 0 0, - - 0 0 0 - -, - - 0 0 0 - - >
