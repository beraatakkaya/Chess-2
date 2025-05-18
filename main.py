import pygame
from game import Game
from ui import (
    draw_board,
    draw_pieces,
    highlight_selected_square,
    highlight_valid_moves,
    highlight_check_square,
    handle_mouse_click,
    draw_timer,
    update_timer,
    draw_icons
)
#from util import start_simulation, end_simulation

fen = 'rnbqkbnr/ppppppPp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
game = Game(
    fen,
)

def run(game):
    running = True
    while running:
        draw_board(game.board)
        highlight_selected_square(game.selected_square)
        draw_pieces(game.board)
        highlight_valid_moves(game.valid_moves, game.board)
        highlight_check_square(game.get_check_square())
        update_timer(game)
        draw_icons(game)
        draw_timer(game.white_time, game.black_time, game.turn)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_click(game, pygame.mouse.get_pos())

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.go_back()
                elif event.key == pygame.K_RIGHT:
                    game.go_forward()

run(game)



