# main.py
import pygame
from game import Game
from ui import (
    draw_board,
    draw_pieces,
    highlight_selected_square,
    highlight_valid_moves,
    highlight_check_square,
    draw_timer,
    load_images,
    screen
    #draw_icons
)


pieces = load_images()

# Game başlat
fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
game = Game(
    fen,
    screen,
    pieces
)

# Ana oyun döngüsü
def run(game):
    running = True
    while running:
        draw_board(game.screen, game.board, game.square_size, game.white, game.brown)
        highlight_selected_square(game.screen, game.selected_square, game.square_size)
        draw_pieces(game.screen, game.board, game.pieces, game.square_size)
        highlight_valid_moves(game.screen, game.valid_moves, game.square_size,game.board)
        highlight_check_square(game.screen, game.get_check_square(), game.square_size)
        draw_timer(game.screen, game.white_time, game.black_time, game.font)
        #draw_icons(game.screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_mouse_click(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.go_back()
                elif event.key == pygame.K_RIGHT:
                    game.go_forward()

run(game)



