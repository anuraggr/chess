from board import Board
from gui import GUI
import pygame

class Game:
    def __init__(self):
        self.board = Board()
        self.gui = GUI()
        self.turn = 'w'
        self.check = False
        self.selected_square = None
        self.promotion_options = {
            'w': ['Q', 'R', 'B', 'N'],
            'b': ['q', 'r', 'b', 'n']
        }

    def handle_promotion(self, start, end):
        options = self.promotion_options[self.turn]
        self.gui.draw_promotion_options(options)
        
        waiting_for_choice = True
        while waiting_for_choice:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    choice = self.gui.get_promotion_choice(pygame.mouse.get_pos(), options)
                    if choice:
                        self.board.make_move(start, end, self.turn, choice)
                        waiting_for_choice = False
                        break
                elif event.type == pygame.QUIT:
                    return False
        return True

    def play(self):
        self.gui.draw_board(self.board)
        running = True
        while running:
            current_check = self.board.is_check(self.turn)
            
            if current_check and not self.board.possible_move_dictionary(self.turn, current_check):
                winner = "Black" if self.turn == 'w' else "White"
                print(f"Checkmate! {winner} is Victorious")
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    square = self.gui.get_square_from_mouse(pos)
                    if self.selected_square is None:
                        piece = self.board.get_piece_at_position(square)
                        if (self.turn == 'w' and piece.isupper()) or (self.turn == 'b' and piece.islower()):
                            self.selected_square = square
                            self.gui.draw_board(self.board)
                            self.gui.highlight_square(square, self.board)
                            moves = self.board.possible_move_dictionary(self.turn, current_check).get(square, [])
                            self.gui.highlight_moves(moves)
                    else:
                        if self.board.is_valid_move(self.selected_square, square, self.turn, current_check):
                            result = self.board.make_move(self.selected_square, square, self.turn)
                            if result == "promotion":
                                if not self.handle_promotion(self.selected_square, square):
                                    running = False
                            self.turn = 'b' if self.turn == 'w' else 'w'
                            self.gui.draw_board(self.board)
                        else:
                            self.gui.draw_board(self.board)
                        self.selected_square = None

        pygame.quit()