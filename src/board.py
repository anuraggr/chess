class Board:
    def __init__(self):
        # Initialize bitboards for each piece type
        self.white_pawns = int("0000000011111111000000000000000000000000000000000000000000000000", 2)
        self.white_rooks = int("1000000100000000000000000000000000000000000000000000000000000000", 2)
        self.white_knights = int("0100001000000000000000000000000000000000000000000000000000000000", 2)
        self.white_bishops = int("0010010000000000000000000000000000000000000000000000000000000000", 2)
        self.white_queen = int("0000100000000000000000000000000000000000000000000000000000000000", 2)
        self.white_king = int("0001000000000000000000000000000000000000000000000000000000000000", 2)
        
        self.black_pawns = int("0000000000000000000000000000000000000000000000001111111100000000", 2)
        self.black_rooks = int("0000000000000000000000000000000000000000000000000000000010000001", 2)
        self.black_knights = int("0000000000000000000000000000000000000000000000000000000001000010", 2)
        self.black_bishops = int("0000000000000000000000000000000000000000000000000000000000100100", 2)
        self.black_queen = int("0000000000000000000000000000000000000000000000000000000000001000", 2)
        self.black_king = int("0000000000000000000000000000000000000000000000000000000000010000", 2)

        self.white_king_moved = False
        self.black_king_moved = False
        self.white_rooks_moved = {56: False, 63: False}
        self.black_rooks_moved = {0: False, 7: False}

    def make_move(self, start: int, end: int, turn: chr, promotion_piece: str = None):
        piece = self.get_piece_at_position(start)
        
        is_promotion = (piece == 'P' and 0 <= end <= 7) or (piece == 'p' and 56 <= end <= 63)
        if is_promotion and not promotion_piece:
            return "promotion"

        if piece == 'K':
            self.white_king_moved = True
            if start == 60:
                if end == 62:
                    self._move_piece(63, 61, 'R')
                elif end == 58:
                    self._move_piece(56, 59, 'R')
        elif piece == 'k':
            self.black_king_moved = True
            if start == 4:
                if end == 6:
                    self._move_piece(7, 5, 'r')
                elif end == 2:
                    self._move_piece(0, 3, 'r')

        elif piece == 'R' and start in self.white_rooks_moved and not self.white_rooks_moved[start]:
            if start == 63: self.white_rooks_moved[start] = True
            elif start == 56: self.white_rooks_moved[start] = True
        elif piece == 'r' and start in self.black_rooks_moved and not self.black_rooks_moved[start]:
            if start == 0: self.black_rooks_moved[start] = True
            elif start == 7: self.black_rooks_moved[start] = True

        mask = ~(1 << start)

        
        self._remove_piece(piece, mask)

        # Handle captures if any
        if self.is_capturable(end, turn):
            self._handle_capture(end, turn)

        # pawn promotion
        if is_promotion and promotion_piece:
            move_mask = (1 << end)
            if turn == 'w':
                if promotion_piece == 'Q': self.white_queen |= move_mask
                elif promotion_piece == 'R': self.white_rooks |= move_mask
                elif promotion_piece == 'B': self.white_bishops |= move_mask
                elif promotion_piece == 'N': self.white_knights |= move_mask
            else:
                if promotion_piece == 'q': self.black_queen |= move_mask
                elif promotion_piece == 'r': self.black_rooks |= move_mask
                elif promotion_piece == 'b': self.black_bishops |= move_mask
                elif promotion_piece == 'n': self.black_knights |= move_mask
            return None

        # Place piece at end position
        move_mask = (1 << end)
        self._place_piece(piece, move_mask)
        return None

    def is_valid_move(self, start: int, end: int, turn: chr, check: bool) -> bool:
        if start < 0 or end >= 64:
            print("Invalid Move. The given squares are outside the bounds of the board")
            return False

        if self.is_occupied(end) and not self.is_capturable(end, turn):
            print("You cannot capture your own piece!")
            return False
            
        piece = self.get_piece_at_position(start)
        if turn == 'w' and piece.islower():
            print(f"Square {start} is not occupied by a whites piece.")
            return False
        if turn == 'b' and piece.isupper():
            print(f"Square {start} is not occupied by a blacks piece.")
            return False

        if check and not self.simulate_move(start, end, turn):
            print("Must move out of check!")
            return False

        p_moves = self.possible_move_dictionary(turn, check)
        if not p_moves:
            print("No valid moves available!")
            return False
        if start not in p_moves or end not in p_moves[start]:
            print("Not a possible move!")
            return False

        return True
    
    def can_castle(self, turn: chr, side: str):
        if turn == 'w':
            if self.white_king_moved:
                return False
            if side == 'kingside':
                if self.white_rooks_moved[63]:
                    return False
                return not any(self.is_occupied(pos) for pos in [61, 62])
            else:
                if self.white_rooks_moved[56]:
                    return False
                return not any(self.is_occupied(pos) for pos in [57, 58, 59])
        else:
            if self.black_king_moved:
                return False
            if side == 'kingside':
                if self.black_rooks_moved[7]:
                    return False
                return not any(self.is_occupied(pos) for pos in [5, 6])
            else:
                if self.black_rooks_moved[0]:
                    return False
                return not any(self.is_occupied(pos) for pos in [1, 2, 3])


    def _move_piece(self, start: int, end: int, piece: str):
        mask = ~(1 << start)
        self._remove_piece(piece, mask)
        move_mask = (1 << end)
        self._place_piece(piece, move_mask)


    def _remove_piece(self, piece, mask):
        if piece == 'P': self.white_pawns &= mask
        elif piece == 'R': self.white_rooks &= mask
        elif piece == 'N': self.white_knights &= mask
        elif piece == 'B': self.white_bishops &= mask
        elif piece == 'Q': self.white_queen &= mask
        elif piece == 'K': self.white_king &= mask
        elif piece == 'p': self.black_pawns &= mask
        elif piece == 'r': self.black_rooks &= mask
        elif piece == 'n': self.black_knights &= mask
        elif piece == 'b': self.black_bishops &= mask
        elif piece == 'q': self.black_queen &= mask
        elif piece == 'k': self.black_king &= mask

    def _handle_capture(self, end, turn):
        capture_mask = ~(1 << end)
        if turn == 'w': 
            if self.black_pawns & (1 << end): self.black_pawns &= capture_mask
            elif self.black_rooks & (1 << end): self.black_rooks &= capture_mask
            elif self.black_knights & (1 << end): self.black_knights &= capture_mask
            elif self.black_bishops & (1 << end): self.black_bishops &= capture_mask
            elif self.black_queen & (1 << end): self.black_queen &= capture_mask
            elif self.black_king & (1 << end): self.black_king &= capture_mask
        else: 
            if self.white_pawns & (1 << end): self.white_pawns &= capture_mask
            elif self.white_rooks & (1 << end): self.white_rooks &= capture_mask
            elif self.white_knights & (1 << end): self.white_knights &= capture_mask
            elif self.white_bishops & (1 << end): self.white_bishops &= capture_mask
            elif self.white_queen & (1 << end): self.white_queen &= capture_mask
            elif self.white_king & (1 << end): self.white_king &= capture_mask

    def _place_piece(self, piece, move_mask):
        if piece == 'P': self.white_pawns |= move_mask
        elif piece == 'R': self.white_rooks |= move_mask
        elif piece == 'N': self.white_knights |= move_mask
        elif piece == 'B': self.white_bishops |= move_mask
        elif piece == 'Q': self.white_queen |= move_mask
        elif piece == 'K': self.white_king |= move_mask
        elif piece == 'p': self.black_pawns |= move_mask
        elif piece == 'r': self.black_rooks |= move_mask
        elif piece == 'n': self.black_knights |= move_mask
        elif piece == 'b': self.black_bishops |= move_mask
        elif piece == 'q': self.black_queen |= move_mask
        elif piece == 'k': self.black_king |= move_mask

    def is_check(self, turn: chr) -> bool:
        opponent_turn = 'b' if turn == 'w' else 'w'
        moves = self.possible_move_dictionary(opponent_turn)  # Get opponent's possible moves
        if turn == 'w':
            for move_list in moves.values():
                if any(self.get_piece_at_position(pos) == 'K' for pos in move_list):
                    return True
        elif turn == 'b':
            for move_list in moves.values():
                if any(self.get_piece_at_position(pos) == 'k' for pos in move_list):
                    return True
        return False

    def simulate_move(self, start: int, end: int, turn: chr) -> bool:
        # # move simulation to handle checks
        state = (
            self.white_pawns, self.white_rooks, self.white_knights, self.white_bishops, self.white_queen, self.white_king,
            self.black_pawns, self.black_rooks, self.black_knights, self.black_bishops, self.black_queen, self.black_king
        )

        self.make_move(start, end, turn)
    
        king_safe = not self.is_check(turn)
        
        (
            self.white_pawns, self.white_rooks, self.white_knights, self.white_bishops, self.white_queen, self.white_king,
            self.black_pawns, self.black_rooks, self.black_knights, self.black_bishops, self.black_queen, self.black_king
        ) = state
        
        return king_safe

    def is_square_under_attack(self, square: int, by_turn: chr) -> bool:
        # Issue was king was able to capture protected pieces. I tried solving it with simulate_move() in
        # possible_moves() but as simulate_move() indirectally called possible_moves() so we were gettig
        # recursion error. So I created this func instead to check if a square is protected or not. In
        # hindsight i should have used possible_moves to add protected moves too and removed them when getting
        # where the piece can move. Maybe later tho.

        
        if by_turn == 'w':   #pawns
            if square % 8 != 0 and square + 7 <= 63 and (self.white_pawns & (1 << (square + 7))):
                return True
            if square % 8 != 7 and square + 9 <= 63 and (self.white_pawns & (1 << (square + 9))):
                return True
        else:
            if square % 8 != 0 and square - 9 >= 0 and (self.black_pawns & (1 << (square - 9))):
                return True
            if square % 8 != 7 and square - 7 >= 0 and (self.black_pawns & (1 << (square - 7))):
                return True

        knight_moves = [17, 15, -15, -17, 6, -6, 10, -10]
        knights = self.white_knights if by_turn == 'w' else self.black_knights
        for move in knight_moves:
            dest = square + move
            if 0 <= dest < 64 and abs((dest % 8) - (square % 8)) <= 2:
                if knights & (1 << dest):
                    return True
                
        rooks = self.white_rooks if by_turn == 'w' else self.black_rooks
        bishops = self.white_bishops if by_turn == 'w' else self.black_bishops
        queens = self.white_queen if by_turn == 'w' else self.black_queen

        for direction in [8, -8, 1, -1]:
            curr = square + direction
            while 0 <= curr < 64 and abs((curr % 8) - ((curr - direction) % 8)) <= 1:
                if (rooks & (1 << curr)) or (queens & (1 << curr)):
                    return True
                if self.is_occupied(curr):
                    break
                curr += direction

        for direction in [7, 9, -7, -9]:
            curr = square + direction
            while 0 <= curr < 64 and abs((curr % 8) - ((curr - direction) % 8)) == 1:
                if (bishops & (1 << curr)) or (queens & (1 << curr)):
                    return True
                if self.is_occupied(curr):
                    break
                curr += direction

        king = self.white_king if by_turn == 'w' else self.black_king
        king_moves = [8, -8, 1, -1, 9, 7, -7, -9]
        for move in king_moves:
            dest = square + move
            if 0 <= dest < 64 and abs((dest % 8) - (square % 8)) <= 1:
                if king & (1 << dest):
                    return True

        return False

    def possible_moves(self, position: int, piece: str, turn: chr=None) -> list:
        moves = []
        if piece == 'p':  # black pawn
            if position >= 8 and position <= 15:  # Starting position
                if not self.is_occupied(position + 8):
                    moves.append(position + 8)
                    if not self.is_occupied(position + 16):
                        moves.append(position + 16)
            else:
                if (position + 8) <= 63 and not self.is_occupied(position + 8):
                    moves.append(position + 8)
            
            # pawn captures
            if position % 8 != 0 and (position + 7) <= 63:  # Left capture
                if self.is_occupied(position + 7) and self.is_capturable(position + 7, turn):
                    moves.append(position + 7)
            if position % 8 != 7 and (position + 9) <= 63:  # Right capture
                if self.is_occupied(position + 9) and self.is_capturable(position + 9, turn):
                    moves.append(position + 9)

        elif piece == 'P':  # white pawn
            if position >= 48 and position <= 55:  # Starting position
                if not self.is_occupied(position - 8):
                    moves.append(position - 8)
                    if not self.is_occupied(position - 16):
                        moves.append(position - 16)
            else:
                if (position - 8) >= 0 and not self.is_occupied(position - 8):
                    moves.append(position - 8)
                    
            # captures
            if position % 8 != 0 and (position - 9) >= 0:  # Left capture
                if self.is_occupied(position - 9) and self.is_capturable(position - 9, turn):
                    moves.append(position - 9)
            if position % 8 != 7 and (position - 7) >= 0:  # Right capture
                if self.is_occupied(position - 7) and self.is_capturable(position - 7, turn):
                    moves.append(position - 7)
            return moves
        elif piece == 'r' or piece == 'R':  # rook
            for i in range(position + 8, 63, 8):  
                if self.is_occupied(i): 
                    if self.is_capturable(i, turn):  
                        moves.append(i)
                    break
                moves.append(i)

            for i in range(position - 8, 0, -8):  
                if self.is_occupied(i):  
                    if self.is_capturable(i, turn): 
                        moves.append(i)
                    break
                moves.append(i)

            for i in range(position + 1, (position // 8 + 1) * 8):  # Move right
                if self.is_occupied(i):  
                    if self.is_capturable(i, turn):  
                        moves.append(i)
                    break
                moves.append(i)

            for i in range(position - 1, (position // 8) * 8-1, -1):  # Move left 
                if self.is_occupied(i):  
                    if self.is_capturable(i, turn):  
                        moves.append(i)
                    break
                moves.append(i)
            return moves
        
        elif piece == 'b' or piece == 'B':  # bishop
            directions = [9, 7, -7, -9]
            for direction in directions:
                for i in range(1, 8):
                    new_position = position + direction * i
                    if new_position < 0 or new_position > 63:
                        break
                    if abs((new_position % 8) - (position % 8)) != i:
                        break
                    if self.is_occupied(new_position):
                        if self.is_capturable(new_position, turn):
                            moves.append(new_position)
                        break
                    moves.append(new_position)
            return moves
        elif piece == 'n' or piece == 'N':
            directions = [17, 15, -15, -17, 6, -6, 10, -10]
            for direction in directions:
                new_position = position + direction
                if 0 <= new_position < 64 and abs((new_position % 8) - (position % 8)) <= 2:
                    if not self.is_occupied(new_position) or self.is_capturable(new_position, turn):
                        moves.append(new_position)
            return moves
        
        # # TODO: combine rook and bishop to get queen moves
        elif piece == 'q' or piece == 'Q':  # queen
            for i in range(position + 8, 63, 8):  
                if self.is_occupied(i): 
                    if self.is_capturable(i, turn):  
                        moves.append(i)
                    break
                moves.append(i)

            for i in range(position - 8, 0, -8):  
                if self.is_occupied(i):  
                    if self.is_capturable(i, turn): 
                        moves.append(i)
                    break
                moves.append(i)

            for i in range(position + 1, (position // 8 + 1) * 8):  # Move right
                if self.is_occupied(i):  
                    if self.is_capturable(i, turn):  
                        moves.append(i)
                    break
                moves.append(i)

            for i in range(position - 1, (position // 8) * 8-1, -1):  # Move left 
                if self.is_occupied(i):  
                    if self.is_capturable(i, turn):  
                        moves.append(i)
                    break
                moves.append(i)
            directions = [9, 7, -7, -9]
            for direction in directions:
                for i in range(1, 8):
                    new_position = position + direction * i
                    if new_position < 0 or new_position > 63:
                        break
                    if abs((new_position % 8) - (position % 8)) != i:
                        break
                    if self.is_occupied(new_position):
                        if self.is_capturable(new_position, turn):
                            moves.append(new_position)
                        break
                    moves.append(new_position)
            return moves
        elif piece == 'k' or piece == 'K':  # king
            opponent_turn = 'b' if turn == 'w' else 'w'
            directions = [8, -8, 1, -1, 9, 7, -7, -9]
            for direction in directions:
                new_position = position + direction
                if 0 <= new_position < 64 and abs((new_position % 8) - (position % 8)) <= 1:
                    # check if move/capture isnt protected by oppo piece
                    if not self.is_square_under_attack(new_position, opponent_turn):
                        if not self.is_occupied(new_position) or self.is_capturable(new_position, turn):
                            moves.append(new_position)

            # castling
            if turn == 'w' and position == 60:
                if self.can_castle(turn, 'kingside'):
                    moves.append(62)
                if self.can_castle(turn, 'queenside'):
                    moves.append(59)
            elif turn == 'b' and position == 4:
                if self.can_castle(turn, 'kingside'):
                    moves.append(6)
                if self.can_castle(turn, 'queenside'):
                    moves.append(2)
            return moves

        # remove moves that expose king to check
        valid_moves = [move for move in moves if self.simulate_move(position, move, turn)]
        return valid_moves

    def get_piece_at_position(self, position: int) -> str:
        if (self.white_pawns & (1 << position)) != 0:
            return 'P'
        elif (self.white_rooks & (1 << position)) != 0:
            return 'R'
        elif (self.white_knights & (1 << position)) != 0:
            return 'N'
        elif (self.white_bishops & (1 << position)) != 0:
            return 'B'
        elif (self.white_queen & (1 << position)) != 0:
            return 'Q'
        elif (self.white_king & (1 << position)) != 0:
            return 'K'
        elif (self.black_pawns & (1 << position)) != 0:
            return 'p'
        elif (self.black_rooks & (1 << position)) != 0:
            return 'r'
        elif (self.black_knights & (1 << position)) != 0:
            return 'n'
        elif (self.black_bishops & (1 << position)) != 0:
            return 'b'
        elif (self.black_queen & (1 << position)) != 0:
            return 'q'
        elif (self.black_king & (1 << position)) != 0:
            return 'k'
        else:
            return '.'

    def possible_move_dictionary(self, turn: chr, check: bool = False) -> dict:
        if check == False:
            all_moves = {}
            for position in range(0,64):
                piece = self.get_piece_at_position(position)
                if piece != '.':
                    if (turn == 'w' and piece.isupper()) or (turn == 'b' and piece.islower()):
                        moves = self.possible_moves(position, piece, turn)
                        if moves:
                            all_moves[position] = all_moves.get(position, []) + moves
            return all_moves
        else:
            all_moves = {}
            for position in range(0, 64):
                piece = self.get_piece_at_position(position)
                if piece != '.' and ((turn == 'w' and piece.isupper()) or (turn == 'b' and piece.islower())):
                    moves = self.possible_moves(position, piece, turn)
                    valid_moves = []
                    for move in moves:
                        if self.simulate_move(position, move, turn):
                            valid_moves.append(move)
                    if valid_moves:
                        all_moves[position] = valid_moves
            return all_moves

    def is_occupied(self, position: int) -> bool: 
        occupied = (
            self.white_pawns | self.white_rooks | self.white_knights | self.white_bishops | self.white_queen | self.white_king |
            self.black_pawns | self.black_rooks | self.black_knights | self.black_bishops | self.black_queen | self.black_king
            )
        return (occupied & (1 << position)) != 0

    def is_capturable(self, position: int, turn: chr) -> bool:   
        if turn == 'w':
                blackPieces = (
                            self.black_pawns | self.black_rooks | self.black_knights | self.black_bishops | self.black_queen | self.black_king
                )
                return (blackPieces & (1<<position)) != 0
        elif turn == 'b':
                whitePieces = (
                            self.white_pawns | self.white_rooks | self.white_knights | self.white_bishops | self.white_queen | self.white_king
                )
                return (whitePieces & (1<<position)) != 0

    def print_board(self):
        # Iterate through 64 squares (8 rows, 8 columns)
        for row in range(8):
            for col in range(8):
                position = row * 8 + col  # Calculate the position in the bitboard
                piece = self.get_piece_at_position(position)  # Get the piece at that position
                print(piece, end=" ")  # Print the piece at this position
            print()  # New line at the end of each row
