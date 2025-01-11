#Bitboard representation
#name = int(string, base)

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
            return False
        piece = getPieceAtPosition(start)
        p_moves = possibleMoves(start, piece)
        if end in p_moves:
             print("valid move")
        else:
             print("Invalid move")
        exit()

def move(start: int, end: int, turn: chr):
    if start < 0 or end >= 64:
        print("Invalid Move. The given squares are outside the bounds of the board")
        exit()
   
    isValidMove(start, end, turn)
        

def possibleMoves(position: int, piece: str) -> bool:
    moves = []
    if piece == 'p':
        if position >= 8 and position <= 15:
            if not isOccupied(position+8):
                moves.append(position + 8)
            if not isOccupied(position+16):
                moves.append(position + 16)
        else:
            if (position + 8) <= 63:
                if not isOccupied(position+8):
                    moves.append(position + 8)
        return moves
    elif piece == 'P':
        if position >= 48 and position <= 55:
            if not isOccupied(position-8):
                moves.append(position - 8)
            if not isOccupied(position-16):
                moves.append(position - 16)
        else:
            if (position - 8) >= 0:
                if not isOccupied(position-8):
                    moves.append(position - 8)
               
          


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
            return (blackPieces & (1<<position)) != 0

def isFriendly(position: int, turn: chr) -> bool:    #turn = 0 -> white trun
    if turn == 'b':
            blackPieces = (
                        black_pawns | black_rooks | black_knights | black_bishops | black_queen | black_king
            )
            return (blackPieces & (1<<position)) != 0
    elif turn == 'w':
            whitePieces = (
                        white_pawns | white_rooks | white_knights | white_bishops | white_queen | white_king
            )
            return (blackPieces & (1<<position)) != 0

# for i in range(64):
#     print(isCapturable(i, 0))
move(8, 32, 'w')
print(getPieceAtPosition(8))
