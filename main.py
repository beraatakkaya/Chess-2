import pygame
import copy

pygame.init()
pygame.mixer.init()

move_sound = pygame.mixer.Sound("sounds/move.mp3")
capture_sound = pygame.mixer.Sound("sounds/capture.mp3")
check_mate_sound = pygame.mixer.Sound("sounds/checkmate.mp3")

Width , Height = 1400 , 1400
Rows,Cols = 8,8
Square_Size = (Width-600) // Rows

White = (240,217,181)
Brown = (181,136,99)
Black = (0, 0, 0)
Gray = (180, 180, 180)

WIN = pygame.display.set_mode((Width,Height))
pygame.display.set_caption('Chess')

white_time = 300 
black_time = 300
last_time = pygame.time.get_ticks()  
valid_moves = []
selected_square = None
turn = 'w'
en_passant_target = None
castling = ['1', '1', '1', '1']

pieces = {}
last_time = pygame.time.get_ticks()

def load_images():
    pieces_types = ['P', 'R', 'N', 'B', 'Q', 'K']
    colors = ['w', 'b']
    for color in colors:
        for piece in pieces_types:
            key = color + piece
            image_path = f'images/{key}.png'
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (Square_Size,Square_Size))
            pieces[key] = image
load_images()

board = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
]
board_history = [copy.deepcopy(board),None,castling]
history_index = 0

def get_rook_moves(board, row, col):
    moves = []
    color = board[row][col][0]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  

    for dr, dc in directions:
        r, c = row + dr, col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            target = board[r][c]
            if target == "--":
                moves.append((r, c))  
            elif target[0] != color: 
                moves.append((r, c))
                break
            else:
                break 
            r += dr
            c += dc
    return moves

def get_knight_moves(board, row, col):
    moves = []
    piece = board[row][col]
    if piece == "--" or piece[1] != "N":
        return moves

    color = piece[0]
    knight_moves = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
    for dr, dc in knight_moves:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8:
            target = board[r][c]
            if target == "--" or target[0] != color:
                moves.append((r, c))
    return moves
def get_bishop_moves(board, row, col):
    moves = []
    color = board[row][col][0]
    directions = [(-1,-1), (-1,1), (1,-1), (1,1)] 

    for dr, dc in directions:
        r, c = row + dr, col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            target = board[r][c]
            if target == "--":
                moves.append((r, c))
            elif target[0] != color:
                moves.append((r, c))
                break
            else:
                break
            r += dr
            c += dc
    return moves

def get_king_moves(board, row, col):
    moves = []
    color = board[row][col][0]
    directions = [(-1, -1), (-1, 0), (-1, 1), 
                  (0, -1),           (0, 1), 
                  (1, -1), (1, 0), (1, 1)] 

    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8:
            target = board[r][c]
            if target == "--" or target[0] != color:
                moves.append((r, c))  

    if color == 'w':
        if castling[1] == '1':
            if board[7][5] == "--" and board[7][6] == "--":
                if not is_in_check(board, "w") and not is_in_check_after_move(board, (7, 4), (7, 5), "w") and not is_in_check_after_move(board, (7, 4), (7, 6), "w"):
                    moves.append((7, 6)) 
        if castling[0] == '1':
            if board[7][1] == "--" and board[7][2] == "--" and board[7][3] == "--":
                if not is_in_check(board, "w") and not is_in_check_after_move(board, (7, 4), (7, 3), "w") and not is_in_check_after_move(board, (7, 4), (7, 2), "w"):
                    moves.append((7, 2)) 

    if color == 'b':
        if castling[3] == '1':
            if board[0][5] == "--" and board[0][6] == "--":
                if not is_in_check(board, "b") and not is_in_check_after_move(board, (0, 4), (0, 5), "b") and not is_in_check_after_move(board, (0, 4), (0, 6), "b"):
                    moves.append((0, 6))
        if castling[2] == '1':
            if board[0][1] == "--" and board[0][2] == "--" and board[0][3] == "--":
                if not is_in_check(board, "b") and not is_in_check_after_move(board, (0, 4), (0, 3), "b") and not is_in_check_after_move(board, (0, 4), (0, 2), "b"):
                    moves.append((0, 2))            
    return moves

def get_queen_moves(board, row, col):
    moves = []
    color = board[row][col][0]
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), 
                  (-1, -1), (-1, 1), (1, -1), (1, 1)] 

    for dr, dc in directions:
        r, c = row + dr, col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            target = board[r][c]
            if target == "--": 
                moves.append((r, c))
            elif target[0] != color:  
                moves.append((r, c))
                break  
            else:
                break 
            r += dr
            c += dc

    return moves

def get_pawn_moves(board, row, col):
    moves = []
    color = board[row][col][0]
    direction = -1 if color == "w" else 1 
    start_row = 6 if color == "w" else 1 

    r, c = row + direction, col
    if 0 <= r < 8 and board[r][c] == "--":
        moves.append((r, c))

    if row == start_row:
        r2 = row + 2 * direction
        if 0 <= r2 < 8 and board[r][c] == "--" and board[r2][c] == "--":
            moves.append((r2, c))

    for dc in [-1, 1]:
        r, c = row + direction, col + dc
        if 0 <= r < 8 and 0 <= c < 8:
            target = board[r][c]
            if target != "--" and target[0] != color:
                moves.append((r, c))

            if en_passant_target == (r, c):
                moves.append((r, c))

    return moves

def promote_pawn(win, turn):
    font = pygame.font.SysFont("Arial", 32)
    promotion_pieces = ["Q", "R", "B", "N"] 
    box_width = 300
    box_height = 80
    box_x = Width // 2 - box_width // 2
    box_y = Height // 2 - box_height // 2

    piece_width = box_width // 4
    selected_piece = None

    pygame.draw.rect(WIN, Gray, (box_x, box_y, box_width, box_height))
    for i, piece in enumerate(promotion_pieces):
        rect = pygame.Rect(box_x + i * piece_width, box_y, piece_width, box_height)
        pygame.draw.rect(WIN, White, rect, 2)
        piece_text = font.render(piece, True, Black)
        text_rect = piece_text.get_rect(center=rect.center)
        WIN.blit(piece_text, text_rect)
    pygame.display.flip()

def is_in_check_after_move(board, from_pos, to_pos, color):
    temp_board = copy.deepcopy(board)
    r1, c1 = from_pos
    r2, c2 = to_pos
    temp_board[r2][c2] = temp_board[r1][c1]
    temp_board[r1][c1] = "--"
    return is_in_check(temp_board, color)

def is_in_check(board, color):
    king_pos = None
    for row in range(8):
        for col in range(8):
            if board[row][col] == color + "K":
                king_pos = (row, col)
                break
        if king_pos:
            break

    enemy_color = "b" if color == "w" else "w"
    for r in range(8):
        for c in range(8):
            if board[r][c].startswith(enemy_color):
                piece_type = board[r][c][1]
                
                if piece_type == "N":
                    moves = get_knight_moves(board, r, c)
                elif piece_type == "B":
                    moves = get_bishop_moves(board, r, c)
                elif piece_type == "R":
                    moves = get_rook_moves(board, r, c)
                elif piece_type == "Q":
                    moves = get_queen_moves(board, r, c)
                elif piece_type == "K":
                    moves = get_king_moves(board, r, c)
                elif piece_type == "P":
                    moves = get_pawn_moves(board, r, c)
                else:
                    moves = []

                if king_pos in moves:
                    return True
    return False

def highlight_king_in_check(win, board, color):
    if not is_in_check(board, color):
        return 

    for row in range(8):
        for col in range(8):
            if board[row][col] == color + "K":
                center_x = col * Square_Size + Square_Size // 2
                center_y = row * Square_Size + Square_Size // 2

                # Parıltı efekti: kırmızı yarı saydam çember
                glow_surface = pygame.Surface((Square_Size, Square_Size), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (255, 0, 0, 90), (Square_Size // 2, Square_Size // 2), Square_Size // 2)
                win.blit(glow_surface, (col * Square_Size, row * Square_Size))

                break

def filter_legal_moves(board, moves, row, col, color):
    legal_moves = []

    for r, c in moves:
        temp_board = copy.deepcopy(board) 
        temp_board[r][c] = temp_board[row][col] 
        temp_board[row][col] = "--"  

        if not is_in_check(temp_board, color):
            legal_moves.append((r, c))

    return legal_moves    

def is_gameover(board, color):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != "--" and piece[0] == color:
                piece_type = piece[1]
                if piece_type == "P":
                    moves = get_pawn_moves(board, row, col)
                elif piece_type == "R":
                    moves = get_rook_moves(board, row, col)
                elif piece_type == "N":
                    moves = get_knight_moves(board, row, col)
                elif piece_type == "B":
                    moves = get_bishop_moves(board, row, col)
                elif piece_type == "Q":
                    moves = get_queen_moves(board, row, col)
                elif piece_type == "K":
                    moves = get_king_moves(board, row, col)
                else:
                    moves = []

                legal_moves = filter_legal_moves(board, moves, row, col, color)
                if legal_moves:
                    return False
    return True

def draw_pieces(screen, board):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != "--":
                screen.blit(pieces[piece], (col * Square_Size, row * Square_Size))
def highlight_selected_square(win, selected):
    if selected:
        row, col = selected
        s = pygame.Surface((Square_Size, Square_Size))
        s.set_alpha(100)  # saydamlık (0-255)
        s.fill((0, 255, 0))  # yeşil vurgu rengi
        win.blit(s, (col * Square_Size, row * Square_Size))
def highlight_valid_moves(win, moves):
    for move in moves:
        row, col = move
        x = col * Square_Size
        y = row * Square_Size
        size = 25

        if board[row][col] == "--": 
            pygame.draw.circle(win, (0, 255, 0), (x + Square_Size // 2, y + Square_Size // 2), 15)
        else: 
            pygame.draw.polygon(win, (0, 255, 0), [(x, y), (x + size, y), (x, y + size)])
            pygame.draw.polygon(win, (0, 255, 0), [(x + Square_Size, y), (x + Square_Size - size, y), (x + Square_Size, y + size)])
            pygame.draw.polygon(win, (0, 255, 0), [(x + Square_Size, y + Square_Size), (x + Square_Size - size, y + Square_Size), (x + Square_Size, y + Square_Size - size)])
            pygame.draw.polygon(win, (0, 255, 0), [(x, y + Square_Size), (x + size, y + Square_Size), (x, y + Square_Size - size)])

def draw_board(win):
    for row in range(Rows):
        for col in range(Cols):
            if (row + col) % 2 == 0:
                color = White
            else:
                color = Brown
            pygame.draw.rect(win,color,(col*Square_Size,row*Square_Size,Square_Size,Square_Size))
def get_square_under_mouse(pos):
    x, y = pos
    col = x // Square_Size
    row = y // Square_Size
    return row, col


def show_time(win, color, time, pos):
    font = pygame.font.SysFont('Arial', 30)
    timer_text = font.render(f"{color} {int(time//60):02d}.{int(time%60):02d}", True, (255, 255 , 255))
    win.blit(timer_text, pos)

run = True
promotion = False
game_over = False
while run:
    current_time = pygame.time.get_ticks()
    delta_time = (current_time - last_time) / 1000  
    if turn == "w":
        white_time -= delta_time
    else:
        black_time -= delta_time
    last_time = current_time
    WIN.fill((0,0,0))
    white_timer_text = show_time(WIN, "White: ", white_time, (900, 600))
    black_timer_text = show_time(WIN, "Black: ", black_time, (900, 400))

    draw_board(WIN)
    highlight_selected_square(WIN, selected_square)
    draw_pieces(WIN,board)
    highlight_valid_moves(WIN, valid_moves)
    highlight_king_in_check(WIN, board, turn)
    if promotion:
        promote_pawn(WIN, turn)
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if promotion:
                    font = pygame.font.SysFont("Arial", 32)
                    promotion_pieces = ["Q", "R", "B", "N"] 
                    box_width = 300
                    box_height = 80
                    box_x = Width // 2 - box_width // 2
                    box_y = Height // 2 - box_height // 2

                    piece_width = box_width // 4
                    selected_piece = None
                    mx, my = pygame.mouse.get_pos()
                    if box_y <= my <= box_y + box_height:
                        index = (mx - box_x) // piece_width
                        if 0 <= index < 4:
                            selected_piece = promotion_pieces[index]
                            board[row][col] = turn + selected_piece
                            promotion = False
                            turn =  'b' if turn == 'w' else 'w'
                            board_copy = copy.deepcopy(board)
                            board_history.append((board_copy, en_passant_target,copy.deepcopy(castling)))
                            history_index += 1          
                            selected_square = None           
                            valid_moves = []

            else:
                pos = pygame.mouse.get_pos()
                row, col = get_square_under_mouse(pos)
                print("Tıklanan kare:", row, col)
                if row > 7 or row < 0 or col > 7 or col < 0:
                    continue
                print(castling)
                print(f'Beyazin zamani: {round(white_time/60,3)}')
                print(f'Siyahin zamani: {round(black_time/60,3)}')
                if selected_square and (row, col) in valid_moves:
                    if history_index < len(board_history) - 1:
                        board_history = board_history[:history_index + 1]
                    sr, sc = selected_square

                    if board[sr][sc][1] == "K" and abs(sc - col) == 2:
                        if col == 6:
                            board[sr][5] = board[sr][7]
                            board[sr][7] = "--"
                        elif col == 2: 
                            board[sr][3] = board[sr][0]
                            board[sr][0] = "--"

                    if board[sr][sc][1] == 'K':
                        if turn == 'w':
                            castling[0]  = castling[1]  = '0'
                        else:
                            castling[2]  = castling[3]  = '0'
                    if board[sr][sc][1] == 'R':
                            if turn == 'w':
                                if sr == 7 and sc == 0:
                                    castling[0] = '0' 
                                elif sr == 7 and sc == 7:
                                    castling[1] = '0'
                            else:
                                if sr == 0 and sc == 0:
                                    castling[2] = '0'
                                elif sr == 0 and sc == 7:
                                    castling[3] = '0'

                    if board[sr][sc][1] == "P":
                        if (row, col) == en_passant_target:
                            board[sr][col] = "--"
                    if board[row][col] == "--":
                        move_sound.play()
                    else:
                        capture_sound.play()  
                    board[row][col] = board[sr][sc]  
                    board[sr][sc] = "--"
                    if board[row][col][1] == "P" and (row == 0 or row == 7):
                        promotion = True

                    if board[0][0] != "bR":
                        castling[2] = '0'
                    if board[0][7] != "bR":
                        castling[3] = '0'
                    if board[7][0] != "wR":
                        castling[0] = '0'
                    if board[7][7] != "wR":
                        castling[1] = '0'   

                    if board[row][col][1] == "P" and abs(sr - row) == 2:
                        en_passant_target = ((sr + row) // 2, sc)
                    else:
                        en_passant_target = None

                    if not promotion:
                        board_copy = copy.deepcopy(board)
                        board_history.append((board_copy, en_passant_target,copy.deepcopy(castling)))
                        history_index += 1          
                        selected_square = None           
                        valid_moves = []
                        turn = 'b' if turn == 'w' else 'w' 
                if selected_square == (row, col):
                    selected_square = None
                    valid_moves = []
                elif board[row][col][0] == turn:
                    selected_square = (row, col)
                    piece_type = board[row][col][1]
                    if piece_type == "N":
                        valid_moves = get_knight_moves(board, row, col)
                    elif piece_type == "B":
                        valid_moves = get_bishop_moves(board, row, col)
                    elif piece_type == "P":
                        valid_moves = get_pawn_moves(board, row, col)
                    elif piece_type == "R":
                        valid_moves = get_rook_moves(board, row, col)
                    elif piece_type == "Q":
                        valid_moves = get_queen_moves(board, row, col)
                    elif piece_type == "K":
                        valid_moves = get_king_moves(board, row, col)
                    else:
                        valid_moves = []
                    valid_moves = filter_legal_moves(board, valid_moves, row, col, turn)
                else:
                    selected_square = None
                    valid_moves = []

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z: 
                if history_index > 0:
                    history_index -= 1
                    board = copy.deepcopy(board_history[history_index][0])
                    en_passant_target = board_history[history_index][1]
                    castling = board_history[history_index][2]
                    turn = turn if promotion else 'b' if turn == 'w' else 'w'
                    selected_square = None
                    valid_moves = []
                    game_over = False

            elif event.key == pygame.K_x:
                if history_index < len(board_history) - 1:
                    history_index += 1
                    board = copy.deepcopy(board_history[history_index][0])
                    en_passant_target = board_history[history_index][1]
                    castling = board_history[history_index][2]
                    turn = turn if promotion else 'b' if turn == 'w' else 'w'
                    selected_square = None
                    valid_moves = []    


    '''                         for boarda in board_history:
                            if board_history.count(boarda) == 3:
                                font = pygame.font.SysFont('arial', 50)
                                print("PAT!")
                                text = font.render(('PAT!'), True, (255, 0, 0))
                                WIN.blit(text, ((Width-600) // 2 - text.get_width() // 2, (Height-600) // 2 - text.get_height() // 2))

                                pygame.display.update()
                                pygame.time.set_timer(pygame.USEREVENT, 3000) 
                                game_over = True'''
    if is_gameover(board, turn):
        font = pygame.font.SysFont('arial', 50)
        if is_in_check(board,turn):
            print("ŞAH MAT! Kazanan:", "Beyaz" if turn == 'b' else "Siyah")
            text = font.render(f'SAH MAT! Kazanan: {"Beyaz" if turn == "b" else "Siyah"}', True, (255, 0, 0))
            WIN.blit(text, ((Width-600) // 2 - text.get_width() // 2, (Height-600) // 2 - text.get_height() // 2))
        else:
            print("PAT!")
            text = font.render('PAT!'), True, (255, 0, 0)
            WIN.blit(text, ((Width-600) // 2 - text.get_width() // 2, (Height-600) // 2 - text.get_height() // 2))
            

        pygame.display.update()
        pygame.time.set_timer(pygame.USEREVENT, 3000)
        if not game_over:
            check_mate_sound.play()
        game_over = True



    pygame.display.update()


