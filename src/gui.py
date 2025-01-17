import pygame
import os

class GUI:
    def __init__(self):
        pygame.init()
        self.square_size = 80  # Reduced from 80 to 60
        self.board_size = self.square_size * 8
        self.screen = pygame.display.set_mode((self.board_size, self.board_size))
        pygame.display.set_caption("Chess")

        # Configure piece sizes with padding
        self.piece_size = int(self.square_size * 0.9)  # Pieces slightly smaller than squares
        self.piece_padding = (self.square_size - self.piece_size) // 2

        # Load and scale pieces with better quality
        self.pieces = {}
        pieces = ['P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']
        for piece in pieces:
            img = pygame.image.load(os.path.join("assets", f"{piece}.png")).convert_alpha()
            self.pieces[piece] = pygame.transform.smoothscale(img, (self.piece_size, self.piece_size))
    
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
                    # Center piece in square
                    piece_x = col * self.square_size + self.piece_padding
                    piece_y = row * self.square_size + self.piece_padding
                    self.screen.blit(self.pieces[piece], (piece_x, piece_y))
        pygame.display.flip()

    def get_square_from_mouse(self, pos):
        x, y = pos
        row = y // self.square_size
        col = x // self.square_size
        return row * 8 + col
    
    def highlight_square(self, square, board):
        row = square // 8
        col = square % 8
        original_surface = self.screen.copy()
        s = pygame.Surface((self.square_size, self.square_size))
        s.set_alpha(128)
        s.fill((100,110,64,255))
        self.screen.blit(s, (col * self.square_size, row * self.square_size))

        piece = board.get_piece_at_position(square)
        if piece != '.':
            piece_x = col * self.square_size + self.piece_padding
            piece_y = row * self.square_size + self.piece_padding
            self.screen.blit(self.pieces[piece], (piece_x, piece_y))
        pygame.display.flip()

    def highlight_moves(self, moves):
        for move in moves:
            row = move // 8
            col = move % 8
            s = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
            pygame.draw.circle(s, (100,110,64,255), (self.square_size//2, self.square_size//2), self.square_size//6)
            self.screen.blit(s, (col * self.square_size, row * self.square_size))
        pygame.display.flip()
