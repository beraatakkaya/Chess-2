import pygame
from time import sleep
from game import Game
from ai import minimax
from ui import (
    draw_board,
    draw_pieces,
    highlight_selected_square,
    highlight_valid_moves,
    highlight_check_square,
    handle_mouse_click,
    draw_timer,
    main_menu,
    update_timer,
    draw_icons
)
#from util import start_simulation, end_simulation

fen = 'rnb1k2r/pp1ppppp/1Q5b/3q3b/8/4q2n/PPPP2PP/RNB1KBNR w KQkq - 0 1'

game = Game(fen)

def run(game):
    running = True
    choice = main_menu()
    ai_color = 'b' if choice =='ai' else None
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_click(game, pygame.mouse.get_pos(), ai_color=ai_color)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.go_back()
                elif event.key == pygame.K_RIGHT:
                    game.go_forward()
        draw_board(game.board)
        highlight_selected_square(game.selected_square)
        draw_pieces(game.board)
        highlight_valid_moves(game.valid_moves, game.board)
        highlight_check_square(game.get_check_square())
        update_timer(game)
        draw_icons(game)
        draw_timer(game.white_time, game.black_time, game.turn)
        pygame.display.flip()

        if not game.game_over and ai_color == game.turn:
            _, best_move = minimax(game, depth=4, alpha=float('-inf'), beta=float('inf'),
                           maximizing_player=True, ai_color=ai_color) 
            if best_move:
                game.move_piece(*best_move)

            #sleep(0.5)
            #if choice == 'ai':
                #ai_color = 'w' if ai_color == 'b' else 'b'

run(game)



