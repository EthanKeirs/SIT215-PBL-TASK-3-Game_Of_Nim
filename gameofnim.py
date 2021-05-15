import random #module implements pseudo-random number generators for various distributions.
import time #This module provides various time-related functions.
import os #This module provides a portable way of using operating system dependent functionalit
import sys #This module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter


def check_empty(list):
    for i in list:
        if i != 0:
            return False
    return True

def check_win(list, mode, computer):
    '''
    Function to declare the winner of the match.
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

def get_computer_move(list):
    if mode:
        num_piles_greater_one = sum(1 for x in list if x > 1)
        # We only need to apply misere strategy if there is one or fewer piles with more than one piece. Otherwise continue as normal.
        if num_piles_greater_one <= 1:
            # Get the number of piles with tokens still on them
            piles_left = sum(1 for x in list if x > 0)
            # Get the size of the largest pile
            max_size = max(list)
            # Get the index of the largest pile
            max_idx = list.index(max_size)
            # If there are an even number of piles left or the largest pile is of size 1, empty the pile
            if piles_left % 2 == 0 or max_size == 1:
                list[max_idx] -= max_size
                print(f"The computer removed {max_size} from pile {max_idx}.")
            # Otherwise, reduce the largest pile to size 1
            else:
                list[max_idx] -= max_size-1
                print(
                    f"The computer removed {max_size-1} from pile {max_idx}.")
            return list

    # Try to make a move that makes the nim sum zero
    for idx, val in enumerate(list):
        # xor nim sum value with current pile
        xor_val = group_nimsum(list) ^ val
        # If the xor value is less than the value of the pile, make the xor value the new value for the pile
        if xor_val < val:
            old_val = val
            list[idx] = xor_val
            # If the new nim sum is zero, make the move
            if group_nimsum(list) == 0:
                print(
                    f"The computer removed {old_val-xor_val} from pile {idx}.")
                return list
            # If the new nim sum wasn't zero, restore the old value and move to the next pile
            list[idx] = old_val
     # If no valid nim sum zeroing move was found, remove a random number from a random stack
    while True:
        pile = random.randint(0, len(list)-1)
        if list[pile] != 0:
            num = random.randint(1, list[pile])
            list[pile] -= num
            print(f"The computer removed {num} from pile {pile}.")
            return list

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


def group_nimsum(list):
    # The nimsum is the xor of the number of discs in each pile
    sum = 0
    for item in list:
        sum ^= item
    return sum

def print_board(list):
    for i, j in enumerate(list):
        print(f"Pile {i}: {j}")
    print()

def generateHeaps():
    numPiles = random.randint(HEAP_MIN, HEAP_MAX) #Constant MIN 2 & MAX 5

    totalItems = random.randint(numPiles+1, numPiles*4)

    # Initialise piles with 1 token each
    discs = [1] * numPiles

    # Distribute tokens randomly amongst piles
    for i in range(totalItems):
        if i == 0:
            discs = [1] * numPiles
        else:
        idx = random.randint(1, numPiles+1)
        discs[idx] += 1
    return discs

def getGameMode():
    '''
    Function to get the game mode. There are two game modes available.
    Normal, where the winner is the player that removes remaining items, and
    Misere, the opposite of normal mode. The last player to move is the loser.
    Will return False if the user chooses to play in normal mode, True otherwise.
    Choosing 3 from the menu will stop the program
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
        if option == 1:
            return False
        elif option == 2:
            return True
        elif option == 3:
            sys.exit(0) #uses sys library
        else:
            print('ERROR: Invalid option')

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
        return False
    else:
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

# Constants
HEAP_MIN = 2   # The minimum amount of heaps
HEAP_MAX = 5   # The maximum amount of heaps

computerMove = False
gameOver = False
discs = initialise_piles()   
mode = getGameMode()
while not gameOver:
    print_board(discs)
    print('=' * 30)
    if not computerMove:
        discs = get_user_move(discs)
    else:
        discs = get_computer_move(discs)
    gameOver = check_win(discs, mode, computerMove)
    computerMove = not computerMove

gameOver = askPlayAgain()

            
