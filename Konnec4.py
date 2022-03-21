import yaml
from IPython.display import clear_output

dollars = '$'
euros = '€'

"""
Sets up the currency pieces, board, and functions needed to play the game
"""
class CurrencyPiece:
    def __init__(self, team_name):
        if type(team_name) == str:
            if team_name.replace(' ','').lower()  == 'dollars':
                self.team_name = "Dollars"
            elif team_name.replace(' ','').lower()  == 'euros':
                self.team_name = "Euros"
            else:
                raise ValueError
        elif type(team_name) == int:
            if team_name == 0:
                self.team_name = "Dollars"
            elif team_name == 1:
                self.team_name = "Euros"
            else:
                raise ValueError
        else:
            raise TypeError
    
    def __str__(self):
        if self.team_name == "Dollars":
            return '$'
        elif self.team_name == "Euros":
            return '€'

class Board:
    def __init__(self):
        self.board = [
                      [None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None]
                     ]
        self.current = "Dollars"
        
    def addPiece(self, column):
        if column < 1 or column > 7:
            raise ValueError
            
        cur = CurrencyPiece(self.current)
        
        if self.board[0][column-1] == None:
            self.board[0][column-1] = cur
            for row in range(1,6):
                if self.board[row][column-1] == None:
                    self.board[row][column-1] = self.board[row-1][column-1]
                    self.board[row-1][column-1] = None
                else:
                    break
            if self.current == "Dollars":
                self.current = "Euros"
            elif self.current == "Euros":
                self.current = "Dollars"
        else:
            pass 
    
    def checkWinner(self):
        pieceD = str(CurrencyPiece("Dollars"))
        pieceE = str(CurrencyPiece("Euros"))
        
        #Horizontal Check
        for r in range(6):
            for c in range(4):
                if str(self.board[r][c]) == pieceD and str(self.board[r][c+1]) == pieceD and str(self.board[r][c+2]) == pieceD and str(self.board[r][c+3]) == pieceD:
                    return "Dollars"
                elif str(self.board[r][c]) == pieceE and str(self.board[r][c+1]) == pieceE and str(self.board[r][c+2]) == pieceE and str(self.board[r][c+3]) == pieceE:
                    return "Euros"
        
        #Vertical Check
        for c in range(7):
            for r in range(3):
                if str(self.board[r][c]) == pieceD and str(self.board[r+1][c]) == pieceD and str(self.board[r+2][c]) == pieceD and str(self.board[r+3][c]) == pieceD:
                    return "Dollars"
                elif str(self.board[r][c]) == pieceE and str(self.board[r+1][c]) == pieceE and str(self.board[r+2][c]) == pieceE and str(self.board[r+3][c]) == pieceE:
                    return "Euros"
                    
        #Positive Diagonal Check
        for r in range(3,6):
            for c in range(4):
                if str(self.board[r][c]) == pieceD and str(self.board[r-1][c+1]) == pieceD and str(self.board[r-2][c+2]) == pieceD and str(self.board[r-3][c+3]) == pieceD:
                    return "Dollars"
                elif str(self.board[r][c]) == pieceE and str(self.board[r-1][c+1]) == pieceE and str(self.board[r-2][c+2]) == pieceE and str(self.board[r-3][c+3]) == pieceE:
                    return "Euros"
        
        #Negative Diagonal Check
        for r in range(3):
            for c in range(4):
                if str(self.board[r][c]) == pieceD and str(self.board[r+1][c+1]) == pieceD and str(self.board[r+2][c+2]) == pieceD and str(self.board[r+3][c+3]) == pieceD:
                    return "Dollars"
                elif str(self.board[r][c]) == pieceE and str(self.board[r+1][c+1]) == pieceE and str(self.board[r+2][c+2]) == pieceE and str(self.board[r+3][c+3]) == pieceE:
                    return "Euros"
        
        return False
    
    def parseMove(self, column, row = 1):
        return True

    def __str__(self) -> str:
        s = "╔" + ("═══╦" * 6) + "═" * 3 + "╗\n"
        for row_index, row in enumerate(self.board):
            s += "║"
            for col_index, column in enumerate(row):
                s += f" {str(column if column != None else ' ')} ║"
            if row_index < 5:
                s += "\n╠" + ("═══╬" * 6) + "═══╣\n"
            else:
                s += '\n'
        return s + "╚" + "═══╩" * 6 + "═" * 3 + "╝\n"

"""
Playable version of the game (Runs the game itself)
"""
board = Board()
moves = []
while board.checkWinner() == False:
    clear_output()
    print("Board:")
    print(str(board))
    print("Current Player:", board.current)
    print(f'Past Moves: {moves}')
    column = input("Pick a column to place your coin! >> ")
    try:
        if column.lower() in ('q', "quit", 'e', "exit"):
            break
        column = int(column)
        moves.append(column)
        try:
            if hasattr(board, 'parseMove') and callable(board.parseMove):
                if board.parseMove((1, column)):
                    board.addPiece(column)
                else:
                    print("That is an invalid move!")
            else:
                board.addPiece(column)
        except Exception as e:
            print("An error occured:", e)
    except Exception as e:
        print("Uh oh... An error occured:", e)
if board.checkWinner():
    clear_output()
    print("Board:")
    print(str(board))
    print(board.board)
    print("And the winner is:", board.checkWinner())
    print(f'Moves: {moves}')
    
"""
Takes the input from .txt or .yaml files to play the game
"""
class NoKonnec4(Exception):
    pass
class BadMoveSon(Exception):
    pass

def playKonnec4File(move_list):
    if type(move_list) != str:
        raise TypeError
    
    #Opening and parsing moves
    if move_list.endswith(".yaml"):
        try:
            with open(move_list) as file:
                moves = yaml.load(file, Loader=yaml.loader.SafeLoader)
        except:
            raise NoKonnec4
        if moves == None:
            raise NoKonnec4
        theMoves = []
        for mov in moves['data']:
            if mov['game'] == 'Konnec 4':
                theMoves = mov['moves']
                break
        if theMoves == []:
            raise NoKonnec4
    elif move_list.endswith(".txt"):
        try:
            with open(move_list, 'r') as file:
                moves = file.read()
        except:
            raise NoKonnec4
        theMoves = moves.split('\n')
        if theMoves == ['']:
            raise NoKonnec4
    else:
        raise ValueError
    
    theBoard = Board()
    counter = 0
    dWin = 0
    eWin = 0
    for moves in theMoves:
        if moves[0] == 'A':
            theBoard.addPiece(int(moves[1]))
        elif moves[0] == 'P':
            str(theBoard)
            counter += 1
        elif moves[0] == 'R':
            theBoard = Board()
        else:
            raise BadMoveSon
        if theBoard.checkWinner() == "Dollars":
            dWin += 1
        elif theBoard.checkWinner() == "Euros":
            eWin += 1
            
    return (theBoard, counter, (dWin, eWin))