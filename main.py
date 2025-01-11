#Bitboard representation
#name = int(string, base)

#   0,   1,  2,  3,  4,  5,  6,  7         black
#   8,   9,  10, 11, 12, 13, 14, 15
#   16, 17,  18, 19, 20, 21, 22, 23
#   24, 25,  26, 27, 28, 29, 30, 31
#   32, 33,  34, 35, 36, 37, 38, 39
#   40, 41,  42, 43, 44, 45, 46, 47
#   48, 49,  50, 51, 52, 53, 54, 55
#   56, 57,  58, 59, 60, 61, 62, 63        white

white_pawns = int(
    "0000000011111111000000000000000000000000000000000000000000000000", 2
)

white_rooks = int(
    "1000000100000000000000000000000000000000000000000000000000000000", 2
)

white_knights = int(
    "0100001000000000000000000000000000000000000000000000000000000000", 2
)

white_bishops = int(
    "0010010000000000000000000000000000000000000000000000000000000000", 2
)

white_queen = int(
    "0001000000000000000000000000000000000000000000000000000000000000", 2
)

white_king = int(
    "0000100000000000000000000000000000000000000000000000000000000000", 2
)

black_pawns = int(
    "0000000000000000000000000000000000000000000000001111111100000000", 2
)

black_rooks = int(
    "0000000000000000000000000000000000000000000000000000000010000001", 2
)

black_knights = int(
    "0000000000000000000000000000000000000000000000000000000001000010", 2
)

black_bishops = int(
    "0000000000000000000000000000000000000000000000000000000000100100", 2
)

black_queen = int(
    "0000000000000000000000000000000000000000000000000000000000010000", 2
)

black_king = int(
    "0000000000000000000000000000000000000000000000000000000000001000", 2
)


def move(start: int, end: int, turn: chr):
    if start < 0 or end >= 64:
        print("Invalid Move. The given squares are outside the bounds of the board")
        exit()
   
    isValidMove(start, end, turn)
         





def isValidMove(start: int, end: int, turn: chr) -> bool:
        if isOccupied(end) and not isCapturable(end, turn):
            print("You cannot capture your own piece!")
            exit()
        piece = getPieceAtPosition(start)
        if turn == 'w':
            if piece.islower():
                print(f"Square {start} is not occupied by a whites piece. {piece} is there.")
                exit()
        if turn == 'b':
            if piece.isupper():
                print(f"Square {start} is not occupied by a blacks piece. {piece} is there.")
                exit()
        p_moves = possibleMoves(start, piece, turn)
        if end not in p_moves:
             print(f"Invalid move. Piece {piece} on square {start} cannot go to the square {end}.\nIt can go to the following squares: {p_moves}")
             exit()
        return True

def move(start: int, end: int, turn: chr):
    if start < 0 or end >= 64:
        print("Invalid Move. The given squares are outside the bounds of the board")
        exit()
   
    isValidMove(start, end, turn)
        

def possibleMoves(position: int, piece: str, turn: chr) -> list:
    moves = []
    if piece == 'p':  # black pawn
        if position >= 8 and position <= 15:
            if not isOccupied(position + 8):
                moves.append(position + 8)
            if not isOccupied(position + 16):
                moves.append(position + 16)
        else:
            if (position + 8) <= 63:
                if not isOccupied(position + 8):
                    moves.append(position + 8)
        print(moves)
        return moves
    elif piece == 'P':  # white pawn
        if position >= 48 and position <= 55:
            if not isOccupied(position - 8):
                moves.append(position - 8)
            if not isOccupied(position - 16):
                moves.append(position - 16)
        else:
            if (position - 8) >= 0:
                if not isOccupied(position - 8):
                    moves.append(position - 8)
        print(moves)
        return moves  
    elif piece == 'r' or piece == 'R':  # rook
        for i in range(position + 8, 63, 8):  
            if isOccupied(i): 
                if isCapturable(i, turn):  
                    moves.append(i)
                break
            moves.append(i)

        for i in range(position - 8, 0, -8):  
            if isOccupied(i):  
                if isCapturable(i, turn): 
                    moves.append(i)
                break
            moves.append(i)

        for i in range(position + 1, (position // 8 + 1) * 8):  # Move right
            if isOccupied(i):  
                if isCapturable(i, turn):  
                    moves.append(i)
                break
            moves.append(i)

        for i in range(position - 1, (position // 8) * 8-1, -1):  # Move left 
            if isOccupied(i):  
                if isCapturable(i, turn):  
                    moves.append(i)
                break
            moves.append(i)
        print(moves)
        return moves
    
    elif piece == 'b' or piece == 'B':  # bishop
        directions = [9, 7, -7, -9]
        for direction in directions:
            for i in range(1, 8):
                new_position = position + direction * i
                if new_position < 0 or new_position >= 64:
                    break
                if abs((new_position % 8) - (position % 8)) != i:
                    break
                if isOccupied(new_position):
                    if isCapturable(new_position, turn):
                        moves.append(new_position)
                    break
                moves.append(new_position)
        print(moves)
        return moves
    # elif piece == 'k' or piece == 'K':

    return moves



def getPieceAtPosition(position: int) -> str:
        if (white_pawns & (1 << position)) != 0:
            return 'P'
        elif (white_rooks & (1 << position)) != 0:
            return 'R'
        elif (white_knights & (1 << position)) != 0:
            return 'N'
        elif (white_bishops & (1 << position)) != 0:
            return 'B'
        elif (white_queen & (1 << position)) != 0:
            return 'Q'
        elif (white_king & (1 << position)) != 0:
            return 'K'
        elif (black_pawns & (1 << position)) != 0:
            return 'p'
        elif (black_rooks & (1 << position)) != 0:
            return 'r'
        elif (black_knights & (1 << position)) != 0:
            return 'n'
        elif (black_bishops & (1 << position)) != 0:
            return 'b'
        elif (black_queen & (1 << position)) != 0:
            return 'q'
        elif (black_king & (1 << position)) != 0:
            return 'k'
        else:
            return '.'


def isOccupied(position: int) -> bool: 
    occupied = (
        white_pawns | white_rooks | white_knights | white_bishops | white_queen | white_king |
        black_pawns | black_rooks | black_knights | black_bishops | black_queen | black_king
        )
    return (occupied & (1 << position)) != 0

def isCapturable(position: int, turn: chr) -> bool:    #turn = 0 -> white trun
    if turn == 'w':
            blackPieces = (
                        black_pawns | black_rooks | black_knights | black_bishops | black_queen | black_king
            )
            return (blackPieces & (1<<position)) != 0
    elif turn == 'b':
            whitePieces = (
                        white_pawns | white_rooks | white_knights | white_bishops | white_queen | white_king
            )
            return (whitePieces & (1<<position)) != 0

def printBoard():
    # Iterate through 64 squares (8 rows, 8 columns)
    for row in range(8):
        for col in range(8):
            position = row * 8 + col  # Calculate the position in the bitboard
            piece = getPieceAtPosition(position)  # Get the piece at that position
            print(piece, end=" ")  # Print the piece at this position
        print()  # New line at the end of each row

# Call the function to print the board
printBoard()


move(26, 27, 'w')
print(getPieceAtPosition(8))
