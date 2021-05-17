"""
Course: Python for Scientist (Part-I)
"""
#%%
def author():
    return 'Austin Schladant'

#%%
import random
import copy
# %%
def DrawBoard(Board):
    '''
    Parameter: Board is a 3x3 matrix (a nested list).
    Return: None
    Description: this function prints the chess board
    hint: Board[i][j] is ' ' or 'X' or 'O' in row-i and col-j
          use print function
    '''
    for i in range(0,3):
        for j in range(0,3):
            if j == 0 or j == 1:
                print(Board[i][j], end='|')
            else:
                print(Board[i][j],)
        print('-+-+-')
    print('\n')
#%% 
def IsSpaceFree(Board, i ,j):
    '''
    Parameters: Board is the game board, a 3x3 matrix
                i is the row index, j is the col index
    Return: True or False
    Description: 
        (1) return True  if Board[i][j] is empty ' '
        (2) return False if Board[i][j] is not empty
        (3) return False if i or j is invalid (e.g. i = -1 or 100)
        think about the order of (1) (2) (3)
        Board[-1][100] will raise error/exception
    '''
    try: 
        if Board[i][j] == ' ':
            return True
        else:
            return False
    except IndexError as excpt:
        print(excpt)
        return False
    
#%%

def GetNumberOfChessPieces(Board):
    '''
    Parameter: Board is the game board, a 3x3 matrix
    Return: the number of chess piceces on Board
            i.e. the total number of 'X' and 'O'
    hint: define a counter and use a nested for loop, like this
          for i in 0 to 3
              for j in 0 to 3
                  add one to the counter if Board[i][j] is not empty
    '''
    count = 0
    for i in range(0,3):
        for j in range(0,3):
            if Board[i][j] != ' ':
                count += 1
                
    return count
    
#%%
def IsBoardFull(Board):
    '''
    Parameter: Board is the game board, a 3x3 matrix
    Return: True or False
    Description: 
        return True if the Board is fully occupied
        return False otherwise 
    hint: use GetNumberOfChessPieces
    '''
    if GetNumberOfChessPieces(Board) == 9:
        return True
    else:
        return False
    
#%%
def IsBoardEmpy(Board):
    '''
    Parameter: Board is the game board, a 3x3 matrix
    Return: True or False
    Description: 
        return True if the Board is empty
        return False otherwise 
    hint: use GetNumberOfChessPieces
    '''
    if GetNumberOfChessPieces(Board) == 0:
        return True
    else:
        return False
#%%
def UpdateBoard(Board, Tag, Choice):
    '''
    Parameters: 
        Board is the game board, a 3x3 matrix
        Tag is 'O' or 'X'
        Choice is a tuple (row, col) from HumanPlayer or ComputerPlayer
    Return: None
    Description: 
         Update the Board after a player makes a choice
         Set an element of the Board to Tag at the location (row, col)
    '''
    if IsSpaceFree(Board, Choice[0], Choice[1]):
        Board[Choice[0]][Choice[1]] = Tag
    
#%%

def HumanPlayer(Tag, Board):
    '''
    Parameters: 
        Tag is 'X' or 'O'. If Tag is 'X': HumanPlayer is PlayerX who goes first
        Board is the game board, a 3x3 matrix
    Return: ChoiceOfHumanPlayer, it is a tuple (row, col)
    Description:
        This function will NOT return until it gets a valid input from the user
    Attention:
        Board is NOT modified in this function
    hint: 
        a while loop is needed, see HumanPlayer in rock-papper-scissors
        the user needs to input row-index and col-index, where a new chess will be placed
        use int() to convert string to int
        use try-except to handle exceptions if the user inputs some random string
        if (row, col) has been occupied, then ask the user to choose another spot
        if (row, col) is invalid, then ask the user to choose a valid spot
    '''
    
    Choice = ()
    
    while len(Choice) != 2:
        try:
            row = int(input('Enter row (0-2): '))
            col = int(input('Enter column (0-2): '))
            
            if (row > 2 or row < 0 or col > 2 or col < 0):
                print('\nRow or column out of index.')
                Choice = ()
            else:    
                Choice = (row, col)
                
                if not IsSpaceFree(Board, row, col):
                    print('\nSpace taken.')
                    Choice = ()
                    
        except ValueError:
            print('Not a valid number')
    
    
    return Choice
    
    
    
#%%
def ComputerPlayer(Tag, Board):
    '''
    Parameters:
        Tag is 'X' or 'O'. If Tag is 'X': ComputerPlayer is PlayerX who goes first
        Board is the game board, a 3x3 matrix
    Return: ChoiceOfComputerPlayer, it is a tuple (row, col)   
    Description:
        ComputerPlayer choose:
            (1) top-right corner if Board is empty
            (2) the spot that makes 3 in a row
            (3) the spot that will block HumanPlayer from winning
            (4) any avaiable corner
            (5) any open space if all the above are not possible
    Attention:
        Board is NOT modified in this function
    '''
    
    if Tag == 'O':
        opp_tag = 'X'
    else:
        opp_tag = 'O'

    # If the board is empty, then places Tag in top right corner
    if IsBoardEmpy(Board):
        return (0,0)
    
    # Places tag to make 3 in a row
    for i in range(0,len(Board)):
        for j in range(0,len(Board[i])):
            if IsSpaceFree(Board, i, j):
                CopyBoard = copy.deepcopy(Board)
                UpdateBoard(CopyBoard, Tag, (i,j))
                if Tag == 'O' and Judge(CopyBoard) == 2:
                    return (i,j)
                elif Tag == 'X' and Judge(CopyBoard) == 1:
                    return (i,j)
                
    # Place tag to block 3 in a row
    for i in range(0,len(Board)):
        for j in range(0,len(Board[i])):
            if IsSpaceFree(Board, i, j):
                CopyBoard = copy.deepcopy(Board)
                UpdateBoard(CopyBoard, opp_tag, (i,j))
                if opp_tag == 'O' and Judge(CopyBoard) == 2:
                    return (i,j)
                elif opp_tag == 'X' and Judge(CopyBoard) == 1:
                    return (i,j)
                
    # Places tag in corner
    if IsSpaceFree(Board, 0, 0):
        return (0,0)
    elif IsSpaceFree(Board, 0, 2):
        return (0,2)
    elif IsSpaceFree(Board, 2, 0):
        return (2,0)
    elif IsSpaceFree(Board, 2, 2):
        return (2,2)
    
    # If no other moves are available, then places Tag in first open space
    for i in range(0,len(Board)):
        for j in range(0,len(Board[i])):
            if IsSpaceFree(Board, i, j):
                return (i,j)

    
#%%

def Judge(Board):
    '''
    Parameter:
         Board is the current game board, a 3x3 matrix
    Return: Outcome, an integer
        Outcome is 0 if the game is still in progress
        Outcome is 1 if player X wins
        Outcome is 2 if player O wins
        Outcome is 3 if it is a tie (no winner)
    Description:
        this funtion determines the Outcome of the game
    hint:
        (1) check if anyone wins, i.e., three 'X' or 'O' in
            top row, middle row, bottom row
            lef col, middle col, right col
            two diagonals
            use a if-statment to check if three 'X'/'O' in a row
        (2) if no one wins, then check if it is a tie
            note: if the board is fully occupied, then it is a tie
        (3) otherwise, the game is still in progress
    '''
    for i in range(0,3):
        if (Board[0][i] == Board[1][i]) and (Board[0][i] == Board[2][i]):
            if Board[0][i] == 'X':
                return 1
            elif Board[0][i] == 'O':
                return 2
        elif(Board[i][0] == Board[i][1]) and (Board[i][0] == Board[i][2]):
            if Board[i][0] == 'X':
                return 1
            elif Board[i][0] == 'O':
                return 2
    
    if(Board[0][0] == Board[1][1]) and (Board[0][0] == Board[2][2]):
        if Board[0][0] == 'X':
            return 1
        elif Board[0][0] == 'O':
            return 2
        
    if(Board[0][2] == Board[1][1]) and (Board[0][2] == Board[2][0]):
        if Board[0][2] == 'X':
            return 1
        elif Board[0][2] == 'O':
            return 2
    
    if IsBoardFull(Board):
        return 3
    
    return 0
    
            
    
#%%
def ShowOutcome(Outcome, NameX, NameO):
    '''
    Parameters:
        Outcome is from Judge
        NameX is the name of PlayerX who goes first at the beginning
        NameO is the name of PlayerO 
    Return: None
    Description:
        print a meassage about the Outcome
        NameX/NameO may be 'human' or 'computer'
    hint: the message could be
        PlayerX (NameX, X) wins 
        PlayerO (NameO, O) wins
        the game is still in progress
        it is a tie
    '''
    if Outcome == 0:
        print('The game is still in progress')
    elif Outcome == 1:
        print(NameX, 'wins')
    elif Outcome == 2:
        print(NameO, 'wins')
    elif Outcome == 3:
        print('It is a tie')
#%% read but do not modify this function
def Which_Player_goes_first():
    '''
    Parameter: None
    Return: two function objects: PlayerX, PlayerO
    Description:
        Randomly choose which player goes first.
        PlayerX/PlayerO is ComputerPlayer or HumanPlayer
    '''
    if random.randint(0, 1) == 0:
        print("Computer player goes first")
        PlayerX = ComputerPlayer
        PlayerO = HumanPlayer
    else:
        print("Human player goes first")
        PlayerO = ComputerPlayer
        PlayerX = HumanPlayer
    return PlayerX, PlayerO
#%% the game
def TicTacToeGame():
    #---------------------------------------------------    
    print("Wellcome to Tic Tac Toe Game")
    Board = [[' ', ' ', ' '],
             [' ', ' ', ' '],
             [' ', ' ', ' ']]
    DrawBoard(Board)
    # determine the order
    PlayerX, PlayerO = Which_Player_goes_first()
    # get the name of each function object
    NameX = PlayerX.__name__
    NameO = PlayerO.__name__
    #---------------------------------------------------    
    # suggested steps in a while loop:
    # (1)  get a choice from PlayerX, e.g. ChoiceX=PlayerX('X', Board)
    # (2)  update the Board
    # (3)  draw the Board
    # (4)  get the outcome from Judge
    # (5)  show the outcome
    # (6)  if the game is completed (win or tie), then break the loop
    # (7)  get a choice from PlayerO
    # (8)  update the Board
    # (9)  draw the Board
    # (10) get the outcome from Judge
    # (11) show the outcome
    # (12) if the game is completed (win or tie), then break the loop
    #---------------------------------------------------
    # your code starts from here
    
    while not IsBoardFull(Board):
        ChoiceX=PlayerX('X', Board) #(1)
        UpdateBoard(Board, 'X', ChoiceX) #(2)
        print(NameX, 'has made their choice')
        DrawBoard(Board) #(3)
        outcome = Judge(Board) #(4)
        ShowOutcome(outcome, NameX, NameO) #(5)
        if outcome == 1 or outcome == 2 or outcome == 3: #(6)
            break;
        ChoiceO = PlayerO('O', Board) #(7)
        UpdateBoard(Board, 'O', ChoiceO) #(8)
        print(NameO, 'has made their choice')
        DrawBoard(Board) #(9)
        outcome = Judge(Board) #(10)
        ShowOutcome(outcome, NameX, NameO) #(11)
        if outcome == 1 or outcome == 2 or outcome == 3: #(12)
            break;
        
    
#%% play the game many rounds until the user wants to quit
# read but do not modify this function
def PlayGame():
    while True:
        TicTacToeGame()
        print('Do you want to play again? (yes or no)')
        if not input().lower().startswith('y'):
            break
    print("GameOver")
#%% do not modify anything below
if __name__ == '__main__':
    PlayGame()
