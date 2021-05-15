'''
This code is a mixture combination of some my own code and had taken reference or piece of code from the following:
Geeks for Geeks (Geeks for Geeks 2020),
Jason andrea (andrea 2020),
Batterystaples (Batterystaples 2019)
Links can be found in the submmited document and this code will includes both my own and there incode documentation'''

import random #module implements pseudo-random number generators for various distributions.
import time #This module provides various time-related functions.
import os #This module provides a portable way of using operating system dependent functionalit
import sys #This module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter

def getGameMode():
    '''
    Function to get the user an option of which game mode, they would like to play. The two game modes are:
    Normal, where the winner is the player that removes remaining items, and
    Misere, the opposite of normal mode. The last player to move is the loser.
    Will return False if the user chooses to play in normal mode, True otherwise.
    The third option avaliable to the user is the quit option which will stop the program
    :return: Boolean value for game mode
    '''

    #Prints menu for user 
    print('=' * 20)
    print('''WELCOME TO THE GAME OF NIM!
    SELECT GAME MODE
    1. Normal - The last player to remove wins
    2. Misere - The last player to remove loses
    3. Quit''')
    print('=' * 20)

    while True:
        option = askIntegerRange('Select an option: ', 1, 3) #calls on askIntegerRange to see if input is within range.
        if option == 1: # If option 1, Normal Game mode is selected, the returned bool is False
            return False
        elif option == 2: # If option 2, Misère Game mode is selected, the returned bool is True
            return True
        elif option == 3:  # If option 3, Quit was selected
            sys.exit(0) #uses sys library
        else:
            print('ERROR: Invalid option')  # Alerts user if they have entered an invaild number or character

def askPlayAgain():
    '''
    Function to print and ask to the user whether the user want to play again or not.
    Will return True or False based on the user input. If the input is 1, return False.
    Otherwise, return True.
    
    '''
    print('''Do you wish to play again?
    1. Yes Play Again
    2. No Don't Play Again''')
    option = askIntegerRange('Enter an option: ', 1, 2)
    if option == 1: # If option 1, the program is run again
        return False
    else: # esle the program quits
        return True

def askIntegerRange(prompt, min, max):
    '''
    Function to ask the user for an integer input within range min and max.
    Will keep asking the user until the input is valid.
    Invalid input is when the input is not an integer or out of range.
    :param prompt: The prompt messsage to ask the user
    :param min: The minimum integer value this function accepts
    :param max: The maximum integer value this function accepts
    :return: The validated user input
    '''
    while True:
        try:
            result = int(input(prompt))
            if result < min or result > max:
                raise ValueError
            return result
        except ValueError:
            print('ERROR: Invalid input.')
            print('Your number must be between ' + str(min) + ' and ' + str(max))
def check_empty(list):
    for i in list:
        if i != 0:
            return False
    return True

def check_win(list, mode, computer):
    '''
    This function is used to declare the winner of the match.
    If playerMoveState is True, that means the last move was made by CPU. Hence, the CPU won the game.
    Otherwise, this procedure will announce that the player won the game.
    :param playerMoveState: Current player move state, from player1ToMove
    :param misereMode: The game mode
    :return:nothing
    '''
    empty = check_empty(list)
    if not empty:
        return False
    # For a normal game, a shortcut we can take here is just flipping who made the last turn.
    # Saves a few checks :)
    if not mode:
        computer = not computer
    print("You won!") if computer else print("The computer won!")
    return True

def get_computer_move(discs, mode):
    '''The Computer_move_function() is the function that will control how the ai works. 
    The decisions are based on the Nim sum were if a move to make the Nim sum of the current 
    configuration to 0 then it is taken, if it is impossible to get to a Nim sum of 0 then 
    a random pile is selected and a random about with the range of the items contained in 
    that pile is removed.
    '''
    selectHeap = random.randint(HEAP_MIN, HEAP_MAX)    # used to select a random heap.
    selectItemAmount = -1                       # -1 is just a placeholder. Will be changed below


    if group_nimsum(discs) == 0:   # If the current Nim sum is 0, the bot is in disadvantage
        selectItemAmount = random.randrange(1, discs[selectHeap] + 1)   # Select random amount of items to be removed
    else:   # If the current Nim sum does not equal to 0, this method will find a move that makes it 0
        attempted = []                                                  # List to store attempted bad heap choice
        emptyHeaps = [i for i in range(len(discs)) if discs[i] == 0]    # List to store indices of empty heaps
        heapIndices = [i for i in range(len(discs)) if i != 0]          # List to store indices of heaps that are not empty
        nonEmptyHeaps = len(discs) - len(emptyHeaps)                    # Variable to store the number of heaps that are not empty

        # If there are only 1 item in all heaps, remove the whole heap randomly
        if nonEmptyHeaps == sum(discs):
            selectHeap = random.randrange(discs, emptyHeaps)
            selectItemAmount = 1    # Only 1 as there is only 1 item left in the heap

        while selectItemAmount == -1:
            if not mode:
                for i in range(discs[selectHeap]):
                    tempHeaps = discs.copy()        # Temporary heaps for checking Nim sum after moving
                    tempHeaps[selectHeap] -= i + 1  # Remove i + 1 items from tempHeaps at index selectHeap
                    if getNimSum(tempHeaps) == 0:   # Checks if after removing the items in tempHeaps makes the Nim sum 0
                        selectItemAmount = i + 1    # If yes, then assign i + 1 to selectItemAmount. It will be returned later
                        break                       # Break the while loop as a good move has been found (Nim sum == 0)
                if selectItemAmount == -1:                          # If this check is executed, that means no good move exist in selected heap
                    attempted.append(selectHeap)                    # Add the selected heap to attempted list
                    selectHeap = selectRandomHeap(discs, attempted) # Choose a new heap. Excluding the previous selected heap
            else:
                # A list that stores indices of heaps that has only 1 item
                singleItemHeaps = [i for i in range(len(heaps)) if heaps[i] == 1]
                if nonEmptyHeaps == 1:
                    selectItemAmount = heaps[selectHeap] - 1
                elif nonEmptyHeaps == 2:
                    if len(singleItemHeaps) == 1:
                        if heaps[selectHeap] == 1:
                            attempted.append(selectHeap)
                            selectHeap = random.randrange(heaps, attempted)
                        selectItemAmount = heaps[selectHeap]
                    else:
                        selectItemAmount = heaps[selectHeap] - (heaps[selectHeap] - 1)
                else:
                    if nonEmptyHeaps == 3 and len(singleItemHeaps) == 2:
                        selectHeap = random.randrange(heaps, singleItemHeaps)
                        selectItemAmount = heaps[selectHeap] - 1
                    else:
                        for i in range(heaps[selectHeap]):
                            tempHeaps = heaps.copy()        # Temporary heaps for checking Nim sum after moving
                            tempHeaps[selectHeap] -= i + 1  # Remove i + 1 items from tempHeaps at index selectHeap
                            if getNimSum(tempHeaps) == 0:   # Checks if after removing the items in tempHeaps makes the Nim sum 0
                                selectItemAmount = i + 1    # If yes, then assign i + 1 to selectItemAmount. It will be returned later
                                break                       # Break the while loop as a good move has been found (Nim sum == 0)
                        if selectItemAmount == -1:                          # If this check is executed, that means no good move exist in selected heap
                            attempted.append(selectHeap)                    # Add the selected heap to attempted list
                            selectHeap = random.randrange(heaps, attempted) # Choose a new heap. Excluding the previous selected heap

    # Return the index of selected heap and the amount of items to be removed from the selected heap
    while True:
        pile = random.randint(0, len(list)-1)
        if list[pile] != 0:
            num = random.randint(1, list[pile])
            list[pile] -= num
            print(f"The computer removed {num} from pile {pile}.")
            return list

def get_user_move(list):
    '''The User move function is what accepts the users inputted pile, if it’s in range,
    and asks for the number of items they wish to remove from the said pile and removes 
    them before ending there turn. '''
    pile = 0 #assigns 0 to int pile
    numdiscs = 0 #assigns 0 to the number of discs
    while True:
        # Try-catch here to handle the integer conversion
        try:
            pile = int(
                input(f"Which pile do you want to take from? (0-{len(list)-1}):  ")) #asks user for input
            if pile < 0 or pile > len(list)-1 or list[pile] < 1: #checks if input is vaild and is with in range
                print(
                    "Pile number must be within range and have at least one item in the pile")
            else:
                break
        except:
            print("Invalid selection!")
    while True:
        try:
            numdiscs = int(
                input(f"How many discs do you want to take? (1-{list[pile]}):  "))#asks user for input
            if numdiscs > 0 and numdiscs <= list[pile]: #checks if input is vaild and is with in range
                break
        except:
            print("Invalid selection!")
            
    list[pile] -= numdiscs  #removes the inputted number of  discs off the selected heap
    print(f"You removed {numdiscs} from pile {pile}.\n")
    return list


def group_nimsum(list):
    ''' Used to calculate the Nim sum 
    '''
    sum = 0
    for item in list:
        sum ^= item # Get the Nim sum for the heaps
    return sum # Return the calculated Nim sum

def print_board(list):
    '''The print board function() is the procedure that prints all heaps and items inside each heaps on screen for user to see'''
    for i, j in enumerate(list):
        print(f"Pile {i}: {j}")  #prints heap and it's accompanying items
    print() #prints blank line

def generateHeaps():
    '''
    Procedure to generate random amount of heaps and items for each heap.
    The number of heap is random from between the min to max constants, and
    the number of items in each heap is random from 2N+1 to 2N+5
    :return: The generated heap including all items inside each heaps
    '''
    heapAmount = random.randint(HEAP_MIN, HEAP_MAX)    # Constant MIN 2 & MAX. 5 Randomly generate 2-5 piles
    itemsEachHeap = []                     # Empty list to store the number of items each heap

    for i in range(heapAmount):
        if i == 0:
            itemsEachHeap.append(1) #makes sure heap has at least 1 item
        else:
            itemsEachHeap.append(2 * (i) + 1)

    return itemsEachHeap #return the list



# Constants
HEAP_MIN = 2   # The minimum amount of heaps
HEAP_MAX = 5   # The maximum amount of heaps

computerMove = False # Makes user start first
gameOver = False # If this is False, then the game will run. Otherwise, the game will not run
discs = generateHeaps()  # will assign variable with a random amount of heaps which have a random amount of items in them using generateHeaps function
mode = getGameMode() #sets game mode to either Normal or misere
while not gameOver: # If this is True, then the game will run. Otherwise, the game will not run
    print_board(discs) # prints all heaps and items inside each heaps
    print('=' * 30)
    if not computerMove:
        discs = get_user_move(discs) # preforms users turn
    else:
        discs = get_computer_move(discs, mode) #computers turn
    gameOver = check_win(discs, mode, computerMove) # At this point, there are no items left. The game ends
    computerMove = not computerMove # Sets turn back to user
    if gameOver == True:
        gameOver = askPlayAgain() # Ask whether the user want to have another game

            
