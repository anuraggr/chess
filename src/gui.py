import pygame
import os

class GUI:
    def __init__(self):
        pygame.init()
        self.square_size = 80
        self.board_size = self.square_size * 8
        self.screen = pygame.display.set_mode((self.board_size, self.board_size))
        pygame.display.set_caption("Chess")

        self.pieces = {}
        pieces = ['P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']
        for piece in pieces:
            self.pieces[piece] = pygame.image.load(
                os.path.join("assets", f"{piece}.png")
            ).convert_alpha()
            self.pieces[piece] = pygame.transform.scale(
                self.pieces[piece], (self.square_size, self.square_size)
            )
    
    def draw_board(self, board):
        for row in range(8):
            for col in range(8):
                color = (240, 217, 181) if (row + col) % 2 == 0 else (181, 136, 99)
                pygame.draw.rect(
                    self.screen, 
                    color, 
                    (col * self.square_size, row * self.square_size, self.square_size, self.square_size)
                )
                piece = board.get_piece_at_position(row * 8 + col)
                if piece != '.':
                    self.screen.blit(
                        self.pieces[piece],
                        (col * self.square_size, row * self.square_size)
                    )
        pygame.display.flip()

    def get_square_from_mouse(self, pos):
        x, y = pos
        row = y // self.square_size
        col = x // self.square_size
        return row * 8 + col
    
    def highlight_square(self, square):
        row = square // 8
        col = square % 8
        s = pygame.Surface((self.square_size, self.square_size))
        s.set_alpha(128)
        s.fill((124, 252, 0))  # light green
        self.screen.blit(s, (col * self.square_size, row * self.square_size))
        pygame.display.flip()

    def highlight_moves(self, moves):
        for move in moves:
            row = move // 8
            col = move % 8
            s = pygame.Surface((self.square_size, self.square_size))
            s.set_alpha(128)
            s.fill((65, 105, 225))  # blue
            self.screen.blit(s, (col * self.square_size, row * self.square_size))
        pygame.display.flip()
    