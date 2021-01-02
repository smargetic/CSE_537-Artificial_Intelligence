#Run this file to execute other searches

from pip._vendor.distlib.compat import raw_input
import time
import re
import IterativeDeepeningSearch
import AStarSearch


class inputStringError(Exception):
    pass


try:
    print("Please specify which search you would like to perform: (1/2)")
    print("\t1) Iterative Deepening Search")
    print("\t2) A* Search")
    userInputSearch = raw_input("").replace(" ", "")
    if((userInputSearch!="1")and (userInputSearch!="2")):
        raise inputStringError
        
    userInputHeuristic = ""
    if(userInputSearch=="2"):
        print("Please specify which heuristic you would like to use: (1/2/3/4)")
        print("\t1) Manhattan Distance")
        print("\t2) Number of Moveable Pegs")
        print("\t3) Distance From Center (Corner Bias)")
        print("\t4) All")

        userInputHeuristic = raw_input("").replace(" ", "")

        if((userInputHeuristic!="1")and(userInputHeuristic!="2")and(userInputHeuristic!="3")and(userInputHeuristic!="4")):
            raise inputStringError

    userInput = raw_input("\nPlease provide a string representing where you want your peg's to be:\n")
    listHoldingUnusablePegs = [0,1,5,6]
    userInputArray = []
    userInput = userInput.replace(" ", "")

    #values other than <, -, X, x, 0
    if(not re.match('[-<>xX0]', userInput)):
        raise inputStringError


    #remove brackets
    if((userInput[0]=="<") and (userInput[-1]==">")):
            userInput = userInput.replace("<", "")
            userInput = userInput.replace(">", "")

    #unmatched brackets
    if(("<" in userInput) or(">" in userInput)):
        raise inputStringError

    userInput = userInput.upper()
    userInputArray = userInput.split(",")

    #make sure it's the right board orientation
    if(len(userInputArray)!=7):
        raise inputStringError

    for i in range(0,len(userInputArray)):
        if(len(userInputArray[i])!=7):
            raise inputStringError

        if(i in listHoldingUnusablePegs):
            for j in listHoldingUnusablePegs:
                if(userInputArray[i][j]!="-"):
                    raise inputStringError

    if(int(userInputSearch)==1):
        IterativeDeepeningSearch.iterativeDeepeningSearch(userInputArray)
    else:
        AStarSearch.aStarSearch(int(userInputHeuristic), userInputArray)


except inputStringError:
    print("Input String Error: please try again.")
except IterativeDeepeningSearch.answerFoundException:
    pass
except AStarSearch.answerFoundException:
    pass
    

    
# < - - 0 0 0 - -, - - 0 X 0 - - , 0 0 X X X 0 0, 0 0 0 X 0 0 0, 0 0 0 X 0 0 0, - - 0 0 0 - -, - - 0 0 0 - - >
# < - - 0 X 0 - -, - - 0 X 0 - - , X X X X X X 0, 0 X 0 X 0 0 0, 0 0 0 X 0 0 0, - - X 0 0 - -, - - 0 0 0 - - >
# < - - 0 0 0 - -, - - 0 X 0 - - , 0 X X X X X 0, 0 0 X X X 0 0, 0 0 X X X 0 0, - - 0 0 0 - -, - - 0 0 0 - - > 
# < - - 0 0 0 - -, - - 0 0 0 - - , 0 0 0 0 0 0 0, 0 0 0 0 0 0 0, 0 0 0 0 0 X 0, - - 0 0 0 - -, - - 0 0 0 - - >

# < - - 0 0 0 - -, - - 0 X 0 - - , 0 0 X X X 0 0, 0 0 0 X 0 0 0, 0 0 0 X 0 0 0, - - 0 0 0 - -, - - 0 0 0 - - >
# < - - 0 0 0 - -, - - 0 X 0 - - , 0 0 X X X 0 0, 0 0 0 X 0 0 0, 0 0 0 X 0 0 0, - - 0 0 0 - -, - - 0 0 0 - - >





