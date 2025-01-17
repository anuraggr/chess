from board import Board

class Game:
    def __init__(self):
        self.board = Board()
        self.turn = 'w'
        self.check = False

    def play(self):
        while True:
            current_check = self.board.is_check(self.turn)
            
            if current_check and not self.board.possible_move_dictionary(self.turn, current_check):
                winner = "Black" if self.turn == 'w' else "White"
                print(f"Checkmate! {winner} is Victorious")
                break

            color = "White" if self.turn == 'w' else "Black"
            start = int(input(f"{color} to move. Enter Piece to move: "))
            end = int(input("Move to: "))

            if not self.board.is_valid_move(start, end, self.turn, current_check):
                print("Invalid Move")
                continue

            self.board.make_move(start, end, self.turn)
            self.check = self.board.is_check('b' if self.turn == 'w' else 'w')
            self.board.print_board()
            self.turn = 'b' if self.turn == 'w' else 'w'