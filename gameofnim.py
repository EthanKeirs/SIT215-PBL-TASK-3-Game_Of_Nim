import random
import sys

def getGameMode():
    print('=' * 20)
    print('''WELCOME TO THE GAME OF NIM!
    PLEASE SELECT DESIRED GAME MODE
    1. Normal - The last player to remove wins
    2. Misere - The last player to remove loses
    3. Quit''')
    print('=' * 20)
    option = askIntegerRange('Select an option: ', 1, 3)
    if option == 1:
        mode = False
    elif option == 2:
        mode = True
    elif option == 3:
        sys.exit(0)
    return option

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
            print('Your number must be between ' + str(min) + ' and ' + str(max)+ ' inclusive.')


def askPlayAgain():
    '''
    Function to print and ask to the user whether the user want to play again or not.
    Will return True or False based on the user input. If the input is 1, return True.
    Otherwise, return False.
    :return: Boolean value. True if input is 1, False if input is 2
    '''
    print('''Do you wish to play again?
    1. Yes
    2. No''')
    option = askIntegerRange('Enter an option: ', 1, 2)
    if option == 1:
        return True
    else:
        return False


def generateHeaps(min, max):
    '''
    Procedure to generate random amount of heaps and items for each heap.
    The number of heap is random from min to max piles, and
    the number of items in each heap is random from 2N+1 to 2N+5
    :param min: The minimum number for the random generated number
    :param max: The maximum number for the random generated number, exclusive
    :return: The generated heap including all items inside each heaps
    '''
    heapAmount = random.randrange(2, 6)    # Randomly generate 2-5 piles
    itemsEachHeap = []                     # Empty list to store the number of items each heap

    # Randomly generate the number of items each heap
    for i in range(heapAmount):
        if i == 0:
            itemsEachHeap.append(1)
        else:
            itemsEachHeap.append(2 * (i) + 1)

    return itemsEachHeap

def print_board(list):
    for i, j in enumerate(list):
        print(f"Pile {i}: {j}")
    print()


def get_user_move(list):
    # Get the user's move
    pile = 0
    numdiscs = 0
    while True:
        # Try-catch here to handle the integer conversion
        try:
            pile = int(
                input(f"Which pile do you want to take from? (0-{len(list)-1}):  "))
            if pile < 0 or pile > len(list)-1 or list[pile] < 1:
                print(
                    "Pile number must be within range and have at least one item in the pile")
            else:
                break
        except:
            print("Invalid selection!")
    while True:
        try:
            numdiscs = int(
                input(f"How many discs do you want to take? (1-{list[pile]}):  "))
            if numdiscs > 0 and numdiscs <= list[pile]:
                break
        except:
            print("Invalid selection!")
    # Take the discs off the pile
    list[pile] -= numdiscs
    print(f"You removed {numdiscs} from pile {pile}.\n")
    return list

def check_empty(list):
    for i in list:
        if i != 0:
            return False
    return True

def check_win(list, mode, computer):
    empty = check_empty(list)
    if not empty:
        return False
    # For a normal game, a shortcut we can take here is just flipping who made the last turn.
    # Saves a few checks :)
    if not mode:
        computer = not computer
    print("You won!") if computer else print("The computer won!")
    return True

def getNimSum(heaps):
    '''
    Function to calculate the Nim sum of current item configuration
    for all heaps. This method is used for the AI opponent to calculate
    a good move.
    :param heaps: The heaps for this method to get the Nim sum
    :return: The Nim sum of the passed heaps
    '''
    heapAmount = len(heaps)         # Get the amount of heaps
    nimSum = heaps[0] ^ heaps[1]    # Get the Nim sum for the first two heaps

    # If there are more than three heaps, calculate Nim sum for heap #3 and more
    if heapAmount > 2:
        i = 2
        while i < heapAmount:
            nimSum = nimSum ^ heaps[i]
            i += 1

    # Return the calculated Nim sum
    return nimSum

def get_computer_move(list):
    '''
    This function is the brain of the AI opponent. This function will return the index of heap selected
    and the amount of items to be removed from the selected heap. The decisions are based on the Nim sum.
    This method will try to find a move that makes the Nim sum of the current configuration to 0.
    If it is impossible to get Nim sum of 0 after the AI opponent's move, then the AI will move randomly.
    :param heaps: The heaps for the AI opponent to decide
    :param misereMode: If the game is running in Misere mode, decision will be adjusted
    :return: The index of selected heap, the amount of item to be removed from the selected heap
    '''
    
    selectHeap = random.randint(0, len(list)-1)    # Select a random heap. No exclusion
    selectItemAmount = -1                       # -1 is just a placeholder. Will be changed below


    if getNimSum(heaps) == 0:   # If the current Nim sum is 0, the bot is in disadvantage
        selectItemAmount = random.randrange(1, heaps[selectHeap] + 1)   # Select random amount of items to be removed
    else:   # If the current Nim sum does not equal to 0, this method will find a move that makes it 0
        attempted = []                                                  # List to store attempted bad heap choice
        emptyHeaps = [i for i in range(len(heaps)) if heaps[i] == 0]    # List to store indices of empty heaps
        heapIndices = [i for i in range(len(heaps)) if i != 0]          # List to store indices of heaps that are not empty
        nonEmptyHeaps = len(heaps) - len(emptyHeaps)                    # Variable to store the number of heaps that are not empty

        # If there are only 1 item in all heaps, remove the whole heap randomly
        if nonEmptyHeaps == sum(heaps):
            selectHeap = selectRandomHeap(heaps, emptyHeaps)
            selectItemAmount = 1    # Only 1 as there is only 1 item left in the heap

        while selectItemAmount == -1:
            if not mode:
                for i in range(heaps[selectHeap]):
                    tempHeaps = heaps.copy()        # Temporary heaps for checking Nim sum after moving
                    tempHeaps[selectHeap] -= i + 1  # Remove i + 1 items from tempHeaps at index selectHeap
                    if getNimSum(tempHeaps) == 0:   # Checks if after removing the items in tempHeaps makes the Nim sum 0
                        selectItemAmount = i + 1    # If yes, then assign i + 1 to selectItemAmount. It will be returned later
                        break                       # Break the while loop as a good move has been found (Nim sum == 0)
                if selectItemAmount == -1:                          # If this check is executed, that means no good move exist in selected heap
                    attempted.append(selectHeap)                    # Add the selected heap to attempted list
                    selectHeap = selectRandomHeap(heaps, attempted) # Choose a new heap. Excluding the previous selected heap
            else:
                # A list that stores indices of heaps that has only 1 item
                singleItemHeaps = [i for i in range(len(heaps)) if heaps[i] == 1]
                if nonEmptyHeaps == 1:
                    selectItemAmount = heaps[selectHeap] - 1
                elif nonEmptyHeaps == 2:
                    if len(singleItemHeaps) == 1:
                        if heaps[selectHeap] == 1:
                            attempted.append(selectHeap)
                            selectHeap = selectRandomHeap(heaps, attempted)
                        selectItemAmount = heaps[selectHeap]
                    else:
                        selectItemAmount = heaps[selectHeap] - (heaps[selectHeap] - 1)
                else:
                    if nonEmptyHeaps == 3 and len(singleItemHeaps) == 2:
                        selectHeap = selectRandomHeap(heaps, singleItemHeaps)
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
                            selectHeap = selectRandomHeap(heaps, attempted) # Choose a new heap. Excluding the previous selected heap

    # Return the index of selected heap and the amount of items to be removed from the selected heap
    #return selectHeap, selectItemAmount

    # Take the discs off the pile
    list[selectHeap] -= selectItemAmount
    print(f"Computer removed {numdiscs} from pile {pile}.\n")
    return list


# Constants
HEAP_MIN = 2   # The minimum amount of heaps
HEAP_MAX = 5   # The maximum amount of heaps

computerMove = False
gameOver = False
itemsEachHeap = generateHeaps(HEAP_MIN, HEAP_MAX + 1)   
mode = getGameMode()
while not gameOver:
    print_board(itemsEachHeap)
    print('=' * 30)
    if not computerMove:
        discs = get_user_move(itemsEachHeap)
    else:
        discs = get_computer_move(itemsEachHeap)
    gameOver = check_win(itemsEachHeap, mode, computerMove)
    computerMove = True

gameOver = askPlayAgain()


            
