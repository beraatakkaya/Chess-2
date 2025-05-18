import pygame

pygame.init()

# Ekran ayarları
width, height = 840, 640
rows, cols = 8, 8
square_size = height // cols
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess")

# Renkler
white = (240, 217, 181)
brown = (181, 136, 99)
black = (0, 0, 0)

# Font
font = pygame.font.SysFont('Arial', 24)

def load_images():
    pieces = {}
    types = ['P', 'R', 'N', 'B', 'Q', 'K', 'p', 'r', 'n', 'b', 'q', 'k']
    for piece in types:
        img = pygame.image.load(f'images/{piece}.png')
        img = pygame.transform.scale(img, (square_size, square_size))
        pieces[piece] = img
    return pieces
def draw_board(screen, board, square_size, white, brown):
    for row in range(8):
        for col in range(8):
            color = white if (row + col) % 2 == 0 else brown
            rect = pygame.Rect(col * square_size, row * square_size, square_size, square_size)
            pygame.draw.rect(screen, color, rect)

def draw_pieces(screen, board, pieces, square_size):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != ".":
                screen.blit(pieces[piece], (col * square_size, row * square_size))

def highlight_selected_square(screen, selected_square, square_size):
    if selected_square:
        row, col = selected_square
        pygame.draw.rect(screen, (255, 255, 0), (col * square_size, row * square_size, square_size, square_size), 3)

def highlight_valid_moves(screen, valid_moves, square_size,board):
    for row, col in valid_moves:
        x = col * square_size
        y = row * square_size
        size = 25
        if board[row][col] == ".":
            pygame.draw.circle(screen, (0, 255, 0), (col * square_size + square_size // 2, row * square_size + square_size // 2), square_size // 6)
        else:
            pygame.draw.polygon(screen, (0, 255, 0), [(x, y), (x + size, y), (x, y + size)])
            pygame.draw.polygon(screen, (0, 255, 0), [(x + square_size, y), (x + square_size - size, y), (x + square_size, y + size)])
            pygame.draw.polygon(screen, (0, 255, 0), [(x + square_size, y + square_size), (x + square_size - size, y + square_size), (x + square_size, y + square_size - size)])
            pygame.draw.polygon(screen, (0, 255, 0), [(x, y + square_size), (x + size, y + square_size), (x, y + square_size - size)])

def highlight_check_square(screen, king_pos, square_size):
    if king_pos:
        row, col = king_pos
        pygame.draw.rect(screen, (255, 0, 0), (col * square_size, row * square_size, square_size, square_size), 3)

def draw_timer(screen, white_time, black_time, font):
    white_text = font.render(f"White: {int(white_time)}s", True, (255, 255, 255))
    black_text = font.render(f"Black: {int(black_time)}s", True, (255, 255, 255))
    screen.blit(white_text, (10, 10))
    screen.blit(black_text, (10, 40))

'''def draw_icons(screen, icon_buttons):  # örnek
    for name, rect in icon_buttons.items():
        pygame.draw.rect(screen, (200, 200, 200), rect)'''
