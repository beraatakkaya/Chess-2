import pygame
import time

pygame.init()
pygame.display.set_caption("Chess")

width, height = 840, 640
rows, cols = 8, 8
square_size = height // cols
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess")

white = (240, 217, 181)
brown = (181, 136, 99)
black = (0, 0, 0)

font = pygame.font.SysFont('Arial', 24)

def load_images():
    pieces = {}
    types = ['P', 'R', 'N', 'B', 'Q', 'K', 'p', 'r', 'n', 'b', 'q', 'k']
    for piece in types:
        img = pygame.image.load(f'images/{piece}.png')
        img = pygame.transform.scale(img, (square_size, square_size))
        pieces[piece] = img
    return pieces

pieces = load_images()

def draw_board(board):
    font = pygame.font.SysFont(None, 24) 
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    ranks = ['8', '7', '6', '5', '4', '3', '2', '1']
    for row in range(8):
        for col in range(8):
            color = white if (row + col) % 2 == 0 else brown
            rect = pygame.Rect(col * square_size, row * square_size, square_size, square_size)
            pygame.draw.rect(screen, color, rect)

            text_color = brown if color == white else white
            if col == cols - 1:
                rank_label = font.render(ranks[row], True, text_color)
                screen.blit(rank_label, (col * square_size + square_size - 15, row * square_size + 5))
            if row == 7:
                file_label = font.render(files[col], True, text_color)
                screen.blit(file_label, (col * square_size + 5,screen.get_height() - 20))


def draw_pieces(board):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != ".":
                screen.blit(pieces[piece], (col * square_size, row * square_size))

def highlight_selected_square(selected_square):
    if selected_square:
        row, col = selected_square
        pygame.draw.rect(screen, (255, 255, 0), (col * square_size, row * square_size, square_size, square_size), 3)

def highlight_valid_moves(valid_moves, board):
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

def highlight_check_square(king_pos):
    if king_pos:
        row, col = king_pos
        pygame.draw.rect(screen, (255, 0, 0), (col * square_size, row * square_size, square_size, square_size), 3)


def draw_icons(game):
    pygame.draw.rect(screen, (50,50,50), (740, 440, 100, 50))
    pygame.draw.rect(screen, (50,50,50), (740, 160, 100, 50))  

    font = pygame.font.SysFont('arial', 26)
    x_font = pygame.font.SysFont('arial', 18)
    game.icon_buttons = {}

    positions = {
        "white_draw": (740, 440),
        "white_resign": (700, 440),
        "black_draw": (740, 160),
        "black_resign": (700, 160)
    }

    normal = (30, 30)
    active = (40, 40)

    if game.draw_offer_white:
        rect = pygame.Rect(positions["white_draw"], active)
        pygame.draw.rect(screen, (160, 100, 100), rect, border_radius=5)
        text = font.render("½", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=rect.center))
        game.icon_buttons["white_draw"] = rect

        cancel_rect = pygame.Rect(rect.right + 5, rect.top, 20, 20)
        x_text = x_font.render("×", True, (255, 255, 255))
        screen.blit(x_text, x_text.get_rect(center=cancel_rect.center))
        game.icon_buttons["white_draw_cancel"] = cancel_rect
    else:
        rect = pygame.Rect(positions["white_draw"], normal)
        pygame.draw.rect(screen, (100, 100, 100), rect, border_radius=5)
        text = font.render("½", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=rect.center))
        game.icon_buttons["white_draw"] = rect

    if game.draw_offer_black:
        rect = pygame.Rect(positions["black_draw"], active)
        pygame.draw.rect(screen, (160, 100, 100), rect, border_radius=5)
        text = font.render("½", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=rect.center))
        game.icon_buttons["black_draw"] = rect

        cancel_rect = pygame.Rect(rect.right + 5, rect.top, 20, 20)
        x_text = x_font.render("×", True, (255, 255, 255))
        screen.blit(x_text, x_text.get_rect(center=cancel_rect.center))
        game.icon_buttons["black_draw_cancel"] = cancel_rect
    else:
        rect = pygame.Rect(positions["black_draw"], normal)
        pygame.draw.rect(screen, (100, 100, 100), rect, border_radius=5)
        text = font.render("½", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=rect.center))
        game.icon_buttons["black_draw"] = rect

    rect = pygame.Rect(positions["white_resign"], normal)
    pygame.draw.rect(screen, (100, 100, 100), rect, border_radius=5)
    flag = font.render("🚩", True, (255, 255, 255))
    screen.blit(flag, flag.get_rect(center=rect.center))
    game.icon_buttons["white_resign"] = rect

    rect = pygame.Rect(positions["black_resign"], normal)
    pygame.draw.rect(screen, (100, 100, 100), rect, border_radius=5)
    flag = font.render("🚩", True, (255, 255, 255))
    screen.blit(flag, flag.get_rect(center=rect.center))
    game.icon_buttons["black_resign"] = rect


def update_timer(game):
    if game.game_over:
        return

    now = time.time()
    elapsed = now - game.last_time
    game.last_time = now

    if game.turn == 'w':
        game.white_time -= elapsed
        if game.white_time <= 0:
            game.white_time = 0
            game.game_over = True
            print("White's time is up, Black wins!")
    else:
        game.black_time -= elapsed
        if game.black_time <= 0:
            game.black_time = 0
            game.game_over = True
            print("Black's time is up, White wins!")

def format_time(seconds):
    minutes = int(seconds) // 60
    secs = int(seconds) % 60
    return f"{minutes:02}:{secs:02}"

def draw_timer(white_time, black_time, turn):
    font = pygame.font.SysFont('arial', 36, bold=True)
    box_width, box_height = 130, 50
    black_pos = (665, 90)
    white_pos = (665, 490)

    white_bg = (0, 100, 0) if turn == 'w' else (80, 80, 80)
    black_bg = (0, 100, 0) if turn == 'b' else (80, 80, 80)

    pygame.draw.rect(screen, white_bg, (*white_pos, box_width, box_height), border_radius=8)
    pygame.draw.rect(screen, black_bg, (*black_pos, box_width, box_height), border_radius=8)

    white_text = font.render(format_time(white_time), True, white)
    black_text = font.render(format_time(black_time), True, white)

    screen.blit(white_text, (white_pos[0] + 10, white_pos[1] + 7))
    screen.blit(black_text, (black_pos[0] + 10, black_pos[1] + 7))



def handle_mouse_click(game, pos):
    if game.game_over:
        return
    if "white_draw_cancel" in game.icon_buttons and game.icon_buttons["white_draw_cancel"].collidepoint(pos):
        game.draw_offer_white = False

    if "black_draw_cancel" in game.icon_buttons and game.icon_buttons["black_draw_cancel"].collidepoint(pos):
        game.draw_offer_black = False

    if game.icon_buttons["white_draw"].collidepoint(pos):
        game.draw_offer_white = not game.draw_offer_white
        if game.draw_offer_white:
            print("White has offered a draw.")
            if game.check_draw_conditions():
                print("Draw conditions have been met. The game ended in a draw.")
                game.game_over = True
        if game.draw_offer_white and game.draw_offer_black:
            print("Both players offered a draw. The game ended in a draw.")
            game.game_over = True
    
    if game.icon_buttons["black_draw"].collidepoint(pos):
        game.draw_offer_black = not game.draw_offer_black
        if game.draw_offer_black:
            print("Black has offered a draw.")
            if game.check_draw_conditions():
                print("Draw conditions have been met. The game ended in a draw.")
                game.game_over = True
        if game.draw_offer_white and game.draw_offer_black:
            print("Both players offered a draw. The game ended in a draw.")
            game.game_over = True

    if game.icon_buttons["white_resign"].collidepoint(pos):
        print("White resigned. Black wins.")
        game.game_over = True

    if game.icon_buttons["black_resign"].collidepoint(pos):
        print("Black resigned. White wins.")
        game.game_over = True
    
    if game.game_over == True:
        game.check_mate_sound.play()
        return

    col = pos[0] // square_size
    row = pos[1] // square_size
    if 0 <= row < 8 and 0 <= col < 8:
        piece = game.board[row][col]
        if game.selected_square and (row, col) in game.valid_moves:
            selected_piece = game.board[game.selected_square[0]][game.selected_square[1]]
            promoted_piece = ''
            if selected_piece == 'P' and row == 0:
                promoted_piece = promote_pawn(game, row, col)
            elif selected_piece == 'p' and row == 7:
                promoted_piece = promote_pawn(game, row, col)
            print("promoted to", promoted_piece)
            game.move_piece(game.selected_square, (row, col), promoted_piece)
        elif game.is_current_players_piece(piece):
            if game.selected_square == (row, col):
                game.selected_square = None
                game.valid_moves = []
            else:# 
                game.selected_square = (row, col)
                game.valid_moves = game.get_valid_moves(row, col)
        else:
            game.selected_square = None
            game.valid_moves = []


def promote_pawn(game, row, col):
    print("buradayim")
    print(row, col)
    promotion_piece = None

    if row==0:
        options = ['Q', 'R', 'N', 'B']
        start_row = 0 
        direction = 1
    else:  
        options = ['b', 'n', 'r', 'q']
        start_row = row - 3  
        direction = 1

    selecting = True
    while selecting:
        draw_board(game.board)
        highlight_selected_square(game.selected_square)
        draw_pieces(game.board)
        update_timer(game)
        draw_timer(game.white_time, game.black_time, game.turn)
        draw_icons(game)

        for i, opt in enumerate(options):
            x = col * square_size
            y = (start_row + i * direction) * square_size

            pygame.draw.rect(screen, (200, 200, 200), (x, y, square_size, square_size))
            screen.blit(pieces[opt], (x, y))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                selected_col = mx // square_size
                selected_row = my // square_size

                for i in range(4):
                    opt_row = start_row + i * direction
                    if selected_row == opt_row and selected_col == col:
                        promotion_piece = options[i]
                        selecting = False
                        break

    return promotion_piece
