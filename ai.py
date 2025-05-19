from copy import deepcopy

def evaluate_board(game, color: str) -> int:

    values = {
        'P': 1, 'N': 3, 'B': 3,
        'R': 5, 'Q': 9, 'K': 0
    }
    total = 0
    for row in game.board:
        for cell in row:
            if cell == ".":
                continue
            val = values.get(cell.upper(), 0)
            if cell.isupper() and color == 'w':
                total += val
            elif cell.islower() and color == 'b':
                total += val
            elif cell.isupper() and color == 'b':
                total -= val
            elif cell.islower() and color == 'w':
                total -= val
    return total

from copy import deepcopy

def minimax(game, depth, alpha, beta, maximizing_player, ai_color):
    if depth == 0:
        return evaluate_board(game, ai_color), None

    best_move = None
    color = ai_color if maximizing_player else ('b' if ai_color == 'w' else 'w')
    all_moves = []

    for row in range(8):
        for col in range(8):
            piece = game.board[row][col]
            if piece != "." and ((color == 'w' and piece.isupper()) or (color == 'b' and piece.islower())):
                for move in game.get_valid_moves(row, col):
                    all_moves.append(((row, col), move))

    if maximizing_player:
        max_eval = float('-inf')
        for start, end in all_moves:
            new_game = deepcopy(game)
            new_game.move_piece(start, end, simulate=True)
            eval, _ = minimax(new_game, depth - 1, alpha, beta, False, ai_color)
            if eval > max_eval:
                max_eval = eval
                best_move = (start, end)
            alpha = max(alpha, eval)  # ✅ Alpha güncellenir
            if beta <= alpha:
                break  # ✅ Budama (Pruning)
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for start, end in all_moves:
            new_game = deepcopy(game)
            new_game.move_piece(start, end, simulate=True)
            eval, _ = minimax(new_game, depth - 1, alpha, beta, True, ai_color)
            if eval < min_eval:
                min_eval = eval
                best_move = (start, end)
            beta = min(beta, eval)  # ✅ Beta güncellenir
            if beta <= alpha:
                break  # ✅ Budama (Pruning)
        return min_eval, best_move
