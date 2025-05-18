import time
import random
import sounds

class Game:
    def __init__(self, fen):
        self.board = self.fen_to_board(fen)

        self.selected_square = None
        self.draw_offer_white = False
        self.draw_offer_black = False
        self.turn = fen.split()[1]
        self.valid_moves = []
        self.white_time = 300 
        self.black_time = 300
        self.last_time = time.time()
        self.game_over = False
        self.history = [(fen, self.white_time, self.black_time)]
        self.history_index = 0
        self.castling_rights = fen.split()[2]
        self.en_passant_target = self.get_en_passant_from_fen(fen)
        enemy_color = 'b' if self.turn == 'w' else 'w'
        self.halfmove_clock = int(fen.split()[4])
        self.fullmove_number = int(fen.split()[5])
        self.is_gameover(enemy_color)

    def fen_to_board(self, fen):
        board = []
        fen_rows = fen.split()[0].split("/")
        for row in fen_rows:
            board_row = []
            for char in row:
                if char.isdigit():
                    board_row.extend(["."] * int(char))
                else:
                    board_row.append(char)
            board.append(board_row)
        return board
    def board_to_fen(self):
        fen_rows = []
        for row in self.board:
            empty = 0
            fen_row = ""
            for cell in row:
                if cell == ".":
                    empty += 1
                else:
                    if empty > 0:
                        fen_row += str(empty)
                        empty = 0
                    fen_row += cell
            if empty > 0:
                fen_row += str(empty)
            fen_rows.append(fen_row)
        
        board_fen = "/".join(fen_rows)
        turn_fen = self.turn
        castling_fen = self.castling_rights if self.castling_rights else "-"
        ep_fen = '-' if self.en_passant_target is None else chr(self.en_passant_target[1] + ord('a')) + str(8 - self.en_passant_target[0])
        return f"{board_fen} {turn_fen} {castling_fen} {ep_fen} {self.halfmove_clock} {self.fullmove_number}"
    def get_en_passant_from_fen(self, fen):
        parts = fen.split()
        if len(parts) >= 4 and parts[3] != '-':
            col = ord(parts[3][0]) - ord('a')
            row = 8 - int(parts[3][1])
            return (row, col)
        return None
    def get_pawn_moves(self, row, col):
        moves = []
        piece = self.board[row][col]
        color = 'w' if piece.isupper() else 'b'
        direction = -1 if color == 'w' else 1
        start_row = 6 if color == 'w' else 1
        if 0 <= row + direction < 8:
            if self.board[row + direction][col] == ".":
                moves.append((row + direction, col))

                if row == start_row and self.board[row + 2 * direction][col] == ".":
                    moves.append((row + 2 * direction, col))

        if self.en_passant_target:
            ep_row, ep_col = self.en_passant_target
            if row == (3 if color == 'w' else 4) and abs(ep_col - col) == 1 and ep_row == row + direction:
                moves.append((ep_row, ep_col))

        for dc in [-1, 1]:
            new_col = col + dc
            new_row = row + direction
            if 0 <= new_col < 8 and 0 <= new_row < 8:
                target = self.board[new_row][new_col]
                if target != "." and (
                    (color == 'w' and target.islower()) or
                    (color == 'b' and target.isupper())):
                    moves.append((new_row, new_col))
        return moves
    def get_pawn_attacks(self, row, col):
        moves = []
        piece = self.board[row][col]
        color = 'w' if piece.isupper() else 'b'
        directions = [(-1, -1), (-1, 1)] if color == 'w' else [(1, -1), (1, 1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                moves.append((r, c))
        return moves

    def get_rook_moves(self, row, col):
        moves = []
        piece = self.board[row][col]
        color = 'w' if piece.isupper() else 'b'
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  

        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = self.board[r][c]
                if target == ".":
                    moves.append((r, c))
                elif (color == 'w' and target.islower()) or (color == 'b' and target.isupper()):
                    moves.append((r, c)) 
                    break
                else:
                    break  
                r += dr
                c += dc
        return moves
    def get_knight_moves(self, row, col):
        moves = []
        piece = self.board[row][col]
        color = 'w' if piece.isupper() else 'b'
        knight_moves = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]

        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = self.board[r][c]
                if target == "." or (color == 'w' and target.islower()) or (color == 'b' and target.isupper()):
                    moves.append((r, c))
        return moves
    def get_bishop_moves(self, row, col):
        moves = []
        piece = self.board[row][col]
        color = 'w' if piece.isupper() else 'b'
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  

        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = self.board[r][c]
                if target == ".":
                    moves.append((r, c))
                elif (color == 'w' and target.islower()) or (color == 'b' and target.isupper()):
                    moves.append((r, c))
                    break
                else:
                    break 
                r += dr
                c += dc
        return moves
    def get_queen_moves(self, row, col):
        return self.get_bishop_moves(row, col) + self.get_rook_moves(row, col)
    def get_king_moves(self, row, col):
        moves = []
        piece = self.board[row][col]
        color = 'w' if piece.isupper() else 'b'
        directions = [(-1, -1), (-1, 0), (-1, 1),
                    (0, -1),          (0, 1),
                    (1, -1), (1, 0),  (1, 1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = self.board[r][c]
                if target == "." or (color == 'w' and target.islower()) or (color == 'b' and target.isupper()):
                    moves.append((r, c))
        if not self.is_in_check(color):
            if color == 'w':
                if 'K' in self.castling_rights and self.board[7][5] == self.board[7][6] == ".":
                    if not self.square_attacked(7, 5, 'b') and not self.square_attacked(7, 6, 'b'):
                        moves.append((7, 6))  
                if 'Q' in self.castling_rights and self.board[7][1] == self.board[7][2] == self.board[7][3] == ".":
                    if not self.square_attacked(7, 2, 'b') and not self.square_attacked(7, 3, 'b'):
                        moves.append((7, 2)) 
            else:
                if 'k' in self.castling_rights and self.board[0][5] == self.board[0][6] == ".":
                    if not self.square_attacked(0, 5, 'w') and not self.square_attacked(0, 6, 'w'):
                        moves.append((0, 6))
                if 'q' in self.castling_rights and self.board[0][1] == self.board[0][2] == self.board[0][3] == ".":
                    if not self.square_attacked(0, 2, 'w') and not self.square_attacked(0, 3, 'w'):
                        moves.append((0, 2))  
        return moves
    def square_attacked(self, row, col, attacker_color):
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece == ".":
                    continue
                if (attacker_color == 'w' and piece.isupper()) or (attacker_color == 'b' and piece.islower()):
                    if piece == 'P':
                        if (row, col) in self.get_pawn_attacks(r, c):
                            return True
                    else:
                        if (row, col) in self.get_piece_moves(r, c,ignore =True):
                            return True
        return False
    def is_current_players_piece(self, piece):
        if piece == ".":
            return False
        if self.turn == 'w':
            return piece.isupper()
        else:
            return piece.islower()  
    def get_piece_moves(self, row, col, ignore = False):
        piece = self.board[row][col]
        if piece == ".":
            return []
        if piece.lower() == 'n':
            return self.get_knight_moves(row, col)
        elif piece.lower() == 'b':
            return self.get_bishop_moves(row, col)
        elif piece.lower() == 'r':
            return self.get_rook_moves(row, col)
        elif piece.lower() == 'q':
            return self.get_queen_moves(row, col)
        elif piece.lower() == 'k' and ignore == False:
            return self.get_king_moves(row, col)
        elif piece.lower() == 'p':
            return self.get_pawn_moves(row, col)
        return []
    def make_ai_move(self, ai_color='b'):
        if self.turn != ai_color:
            pass
        else:
            all_moves = []
            for row in range(8):
                for col in range(8):
                    piece = self.board[row][col]
                    if piece != "." and ((ai_color == 'w' and piece.isupper()) or (ai_color == 'b' and piece.islower())):
                        moves = self.get_valid_moves(row, col)
                        for move in moves:
                            all_moves.append(((row, col), move))
            if all_moves:
                move = random.choice(all_moves)
                self.move_piece(*move)
    def move_piece(self, start_pos, end_pos, promote_to=None):
        self.en_passant_target = None

        start_row, start_col = start_pos
        end_row, end_col = end_pos

        piece = self.board[start_row][start_col]
        target = self.board[end_row][end_col]  

        if piece.lower() == 'p' or target != ".":
            self.halfmove_clock = 0 
        else:
            self.halfmove_clock += 1 

        if target != "." or (piece.lower() == 'p' and start_col != end_col and self.board[end_row][end_col] == "."):
            sounds.capture_sound.play()  
        else:
            sounds.move_sound.play()

        if piece.lower() == 'p' and abs(end_row - start_row) == 2:
            self.en_passant_target = ((start_row + end_row) // 2, start_col)

        if piece.lower() == 'p' and (start_col != end_col) and self.board[end_row][end_col] == ".":
            self.board[start_row][end_col] = "."

        self.board[end_row][end_col] = piece

        if piece == 'K':
            self.castling_rights = self.castling_rights.replace('K', '').replace('Q', '')
        elif piece == 'k':
            self.castling_rights = self.castling_rights.replace('k', '').replace('q', '')
        elif piece == 'R':
            if start_row == 7 and start_col == 0:
                self.castling_rights = self.castling_rights.replace('Q', '')
            elif start_row == 7 and start_col == 7:
                self.castling_rights = self.castling_rights.replace('K', '')
        elif piece == 'r':
            if start_row == 0 and start_col == 0:
                self.castling_rights = self.castling_rights.replace('q', '')
            elif start_row == 0 and start_col == 7:
                self.castling_rights = self.castling_rights.replace('k', '')    
        self.board[start_row][start_col] = "."   
        if piece.lower() == 'k':
            if start_row == 7 and start_col == 4:
                if end_row == 7 and end_col == 6: 
                    self.board[7][5] = 'R'
                    self.board[7][7] = '.'
                elif end_row == 7 and end_col == 2:  
                    self.board[7][3] = 'R'
                    self.board[7][0] = '.'
            elif start_row == 0 and start_col == 4:
                if end_row == 0 and end_col == 6: 
                    self.board[0][5] = 'r'
                    self.board[0][7] = '.'
                elif end_row == 0 and end_col == 2: 
                    self.board[0][3] = 'r'
                    self.board[0][0] = '.'

        if promote_to:
            self.board[end_row][end_col] = promote_to

        if self.turn == 'b':
            self.fullmove_number += 1

        self.selected_square = None              
        self.valid_moves = []                
        self.switch_turn()            
        fen = self.board_to_fen()
        print(fen)
        self.history = self.history[:self.history_index + 1]
        self.history.append((fen, self.white_time, self.black_time))  
        self.history_index += 1
        self.board = self.fen_to_board(fen)

        self.is_gameover(self.turn)
        self.check_draw_conditions()


    def switch_turn(self):
        self.turn = 'b' if self.turn == 'w' else 'w'

    def get_valid_moves(self, row, col):
        original_piece = self.board[row][col]
        color = 'w' if original_piece.isupper() else 'b'
        moves = self.get_piece_moves(row, col)
        legal_moves = []

        for r, c in moves:
            captured = self.board[r][c]
            en_passant = False
            ep_captured_piece = None
            ep_row, ep_col = -1, -1

            # En passant kontrolü
            if original_piece.lower() == 'p' and self.en_passant_target == (r, c) and self.board[r][c] == "." and col != c:
                en_passant = True
                ep_row = row  # Yani aynı satırda
                ep_col = c
                ep_captured_piece = self.board[ep_row][ep_col]
                self.board[ep_row][ep_col] = "."

            self.board[r][c] = original_piece
            self.board[row][col] = "."

            if not self.is_in_check(color):
                legal_moves.append((r, c))

            self.board[row][col] = original_piece
            self.board[r][c] = captured

            # En passant alınan piyonu geri koy
            if en_passant:
                self.board[ep_row][ep_col] = ep_captured_piece

        return legal_moves

    def is_in_check(self, color):
        king = 'K' if color == 'w' else 'k'
        king_pos = None
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == king:
                    king_pos = (row, col)
                    break
            if king_pos:
                break
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece == ".":
                    continue
                if color == 'w' and piece.islower():
                    if self.turn == 'b':
                        enemy_moves = self.get_piece_moves(r, c,ignore=True)
                    else:
                        enemy_moves = self.get_piece_moves(r, c)
                    if king_pos in enemy_moves:
                        return True
                elif color == 'b' and piece.isupper():
                    if self.turn == 'w':
                        enemy_moves = self.get_piece_moves(r, c,ignore=True)
                    else:
                        enemy_moves = self.get_piece_moves(r, c)
                    if king_pos in enemy_moves:
                        return True
        return False
    def get_check_square(self):
        if not self.is_in_check(self.turn):
           return None

        king_piece = 'K' if self.turn == 'w' else 'k'
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == king_piece:
                    return (row, col)
        return None
    def is_gameover(self, color):
        if self.halfmove_clock == 75:
            print("75 moves have passed, it's a forced draw.")
            sounds.check_mate_sound.play()
            self.game_over = True
        elif not self.has_legal_moves(color):
            if self.is_in_check(color):
                if color == 'w':
                    print("Checkmate, Black Won!")
                else:
                    print("Checkmate, White Won!")
            else:    
                print("Stalemate!")
            sounds.check_mate_sound.play()
            self.game_over = True
        else:
            self.game_over = False
    def check_draw_conditions(self):
        if self.halfmove_clock >= 50:
            print('50-move rule draw can be claimed.')
            return True
        
        position_counts = {}
        for entry in self.history:
            fen = entry[0]
            fen_parts = fen.split()
            key = " ".join(fen_parts[:4]) 
            if key in position_counts:
                position_counts[key] += 1
            else:
                position_counts[key] = 1

            if position_counts[key] >= 3:
                print('Threefold repetition detected — draw can be claimed.')
                return True
        return False
    def has_legal_moves(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece == ".":
                    continue
                if (color == 'w' and piece.isupper()) or (color == 'b' and piece.islower()):
                    moves = self.get_piece_moves(row, col)
                    for move in moves:
                        if self.is_legal_move((row, col), move):
                            return True
        return False

    def is_legal_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        piece = self.board[start_row][start_col]
        captured = self.board[end_row][end_col]

        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = "."

        in_check = self.is_in_check('w' if piece.isupper() else 'b')

        self.board[start_row][start_col] = piece
        self.board[end_row][end_col] = captured

        return not in_check





    def go_back(self):
        if self.history_index > 0:
            self.history_index -= 1
            fen, white_time, black_time = self.history[self.history_index]
            self.board = self.fen_to_board(fen)
            self.turn = fen.split()[1]
            self.castling_rights = fen.split()[2]
            self.en_passant_target = self.get_en_passant_from_fen(fen)
            self.halfmove_clock = int(fen.split()[4])
            self.fullmove_number = int(fen.split()[5])
            self.white_time = white_time
            self.black_time = black_time
            self.selected_square = None
            self.valid_moves = []
            self.draw_offer_black = False
            self.draw_offer_white = False
            enemy_color = 'b' if self.turn == 'w' else 'w'
            self.is_gameover(enemy_color)

    def go_forward(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            fen, white_time, black_time = self.history[self.history_index]
            self.board = self.fen_to_board(fen)
            self.turn = fen.split()[1]
            self.castling_rights = fen.split()[2]
            self.en_passant_target = self.get_en_passant_from_fen(fen)
            self.halfmove_clock = int(fen.split()[4])
            self.fullmove_number = int(fen.split()[5])
            self.white_time = white_time
            self.black_time = black_time
            self.selected_square = None
            self.valid_moves = []    
            self.draw_offer_black = False
            self.draw_offer_white = False
            enemy_color = 'b' if self.turn == 'w' else 'w'
            if self.history_index>0:
                self.is_gameover(self.turn)
            else:
                self.is_gameover(enemy_color)   
