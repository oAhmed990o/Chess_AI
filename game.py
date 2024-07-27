import copy
from piece import Piece
from king import King
from queen import Queen
from rook import Rook
from bishop import Bishop
from knight import Knight
from pawn import Pawn
from board import Board
from player import Player
import pygame as p
import consts

images = {}
logs = ''

def load_images():
    pieces = ['white_pawn', 'white_knight', 'white_bishop', 'white_rook', 'white_queen', 'white_king', 
    'black_pawn', 'black_knight', 'black_bishop', 'black_rook', 'black_queen', 'black_king']
    # load pieces
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load('art/' + piece + '.png'), (consts.SQUARE_SIZE, consts.SQUARE_SIZE))

def draw_board(screen, row, col, update):
    colors = [p.Color(240,216,191,255), p.Color(186,85,70,255)]
    for r in range(consts.DIMENSION):
        for c in range(consts.DIMENSION):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*(consts.SQUARE_SIZE), r*(consts.SQUARE_SIZE), (consts.SQUARE_SIZE), (consts.SQUARE_SIZE)))
    if update:
        if (row+col)%2 == 0:
            p.draw.rect(screen, p.Color(244,232,169,255), p.Rect(col*(consts.SQUARE_SIZE), row*(consts.SQUARE_SIZE), (consts.SQUARE_SIZE), (consts.SQUARE_SIZE)))
        else:
            p.draw.rect(screen, p.Color(217,167,108,255), p.Rect(col*(consts.SQUARE_SIZE), row*(consts.SQUARE_SIZE), (consts.SQUARE_SIZE), (consts.SQUARE_SIZE)))
        
def draw_pieces(screen, board):
    for r in range(consts.DIMENSION):
        for c in range(consts.DIMENSION):
            if board[r][c]:
                screen.blit(images[board[r][c].color + '_' + board[r][c].typ], p.Rect(c*(consts.SQUARE_SIZE), r*(consts.SQUARE_SIZE), (consts.SQUARE_SIZE), (consts.SQUARE_SIZE)))

def get_mouse_row_col(pos):
    row = pos[1]//(consts.SQUARE_SIZE)
    col = pos[0]//(consts.SQUARE_SIZE)
    return row, col        

def promote(board, pos, type):
    x, y = pos
    color = board[x][y].color
    if type.lower() == 'q':
         promoted = Queen([x, y], color, 'queen')
    elif type.lower() == 'n':
        promoted = Knight([x, y], color, 'knight')
    elif type.lower() == 'r':
        promoted = Rook([x, y], color, 'rook')
    elif type.lower() == 'b':
        promoted = Bishop([x, y], color, 'bishop')
    else:
        return
    board[x][y] = promoted
    return board

def key_to_char(key):
    if key == p.K_q:
        return 'q'
    if key == p.K_n:
        return 'n'
    if key == p.K_r:
        return 'r'
    if key == p.K_b:
        return 'b'
    else:
        return ''

def draw_text(screen, font_size, text):
    font = p.font.SysFont('Cairo', font_size, True, False)
    text_object = font.render(text, 0, p.Color('Black'))
    text_location = p.Rect(0, 0, consts.WIDTH, consts.HEIGHT).move(consts.WIDTH/2 - text_object.get_width()/2, consts.HEIGHT/2 - text_object.get_height()/2)
    screen.blit(text_object, text_location)

def switch_players(white):
    if white.is_turn_player:
        return [False, True]
    else:
        return [True, False]

def board_to_string(board):
    ans = []
    for i in range(consts.DIMENSION):
        for j in range(consts.DIMENSION):
            if not board[i][j]:
                ans.append('..')
                continue
            color = 'w' if board[i][j].color == 'white' else 'b'
            if board[i][j].typ == 'pawn':
                ans.append(color + 'p')
            elif board[i][j].typ == 'bishop':
                ans.append(color + 'b')
            elif board[i][j].typ == 'knight':
                ans.append(color + 'n')
            elif board[i][j].typ == 'rook':
                ans.append(color + 'r')
            elif board[i][j].typ == 'queen':
                ans.append(color + 'q')
            elif board[i][j].typ == 'king':
                ans.append(color + 'k')
    return ''.join(ans)

def quit_game(text):
    while 1:
        draw_text(screen, 64, text)
        p.display.update()
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
            if event.type == p.KEYDOWN:
                if event.key == p.K_ESCAPE:
                    p.quit()

def check_ambiguity_state(board, moved_piece, square_to_check):
    # check if the player has multiple pieces similar to the moved piece
    # check all possible moves of those pieces, if a piece(s) could move to the same chosen square
    # check if the moved piece has a different file than this piece(s), if so return 'different_file'
    # check if the moved piece has a different rank than this piece(s), if so return 'different_rank'
    # else return 'neither'
    found_ambiguity = False
    different_rank_file = [True, True]
    for row in range(len(board)):
        for col in range(len(board[0])):
            # if a player has multiple copies of a piece
            repeated_piece = board[row][col]
            if repeated_piece and [row, col] != moved_piece.pos and repeated_piece.typ == moved_piece.typ and repeated_piece.color == moved_piece.color:
                # if the repeated piece can move to the same square
                if square_to_check in repeated_piece.get_possible_moves(board, reverse):
                    found_ambiguity = True
                    # check if the file is the same
                    if repeated_piece.pos[1] == moved_piece.pos[1]:
                        different_rank_file[1] = False
                    # check if the rank is the same
                    if repeated_piece.pos[0] == moved_piece.pos[0]:
                        different_rank_file[0] = False
                    # return if both file and rank are already repeated
                    if different_rank_file == [False, False]:
                        return 'neither_are_different'
                    
    if different_rank_file == [False, True]:
        return 'different_file'
    if different_rank_file == [True, False]:
        return 'different_rank'
    if found_ambiguity:
        return 'different_file'
    return 'no_ambiguity'

def game_log(piece_moved, start_pos, end_pos, prev_board, curr_board, is_check, is_checkmate, ambiguity_state, is_en_passant, reverse):
    global logs

    rank1, file1 = start_pos
    rank2, file2 = end_pos
    start_pos_rank, start_pos_file = consts.BOARD_RANKS[rank1], consts.BOARD_FILES[file1]
    end_pos_rank, end_pos_file = consts.BOARD_RANKS[rank2], consts.BOARD_FILES[file2]

    # Check for castling
    if piece_moved.typ == 'king' and abs(file1 - file2) == 2:
        if reverse:
            if end_pos_file == 'f':
                logs = logs + ' ' + '0-0-0'
            else:
                logs = logs + ' ' + '0-0'
        else:
            if end_pos_file == 'g':
                logs = logs + ' ' + '0-0'
            else:
                logs = logs + ' ' + '0-0-0'
    else:

        curr_move_notation = ['', '', '', '', '', '']

        if ambiguity_state == 'different_file':
            curr_move_notation[1] = start_pos_file
        elif ambiguity_state == 'different_rank':
            curr_move_notation[1] = start_pos_rank
        elif ambiguity_state == 'neither_are_different':
            curr_move_notation[1] = start_pos_file + start_pos_rank

        if piece_moved.typ == 'pawn':
            piece_letter = ''
        elif piece_moved.typ == 'knight':
            piece_letter = 'N'
        else:
            piece_letter = piece_moved.typ[0].upper()

        curr_move_notation[0] = piece_letter
        curr_move_notation[3] = end_pos_file + end_pos_rank

        if prev_board[rank2][file2] or is_en_passant:
            if piece_letter == '':
                curr_move_notation[1] = start_pos_file
            curr_move_notation[2] = 'x'

        if is_check:
            curr_move_notation[5] = '+'

        if piece_letter == '' and (end_pos_rank == '1' or end_pos_rank == '8'):
            chosen_promotion = curr_board[rank2][file2]
            if chosen_promotion.typ == 'knight':
                promotion_letter = 'N'
            else:
                promotion_letter = chosen_promotion.typ[0].upper()
            curr_move_notation[4] = '=' + promotion_letter

        if is_checkmate:
            curr_move_notation[5] = '#'

        logs = logs + ' ' + ''.join(curr_move_notation) if logs else ''.join(curr_move_notation)
    # print(logs)

if __name__ == "__main__":
    b = Board()

    chosen = False

    board_stack = []
    board_count = {}

    p.init()
    screen = p.display.set_mode((consts.WIDTH, consts.HEIGHT))
    p.display.set_caption('Chess')
    load_images()
    run = True
    clock = p.time.Clock()
    update = False
    row, col = 0, 0
    
    sq_selected = []
    player_clicks = []
    
    fifty_move_rule = 0
    num_pieces = 32
    has_any_pawn_moved = False

    while not chosen:
        p.draw.rect(screen, p.Color('white'), p.Rect(0, 0, (consts.WIDTH//2), consts.HEIGHT))
        p.draw.rect(screen, p.Color('black'), p.Rect((consts.HEIGHT//2), (consts.WIDTH//2), (consts.WIDTH//2), consts.HEIGHT))
        clock.tick(consts.FPS)
        p.display.flip()    
        for event in p.event.get():
            if event.type == p.QUIT:
                run = False
            if event.type == p.KEYDOWN:
                if event.key == p.K_ESCAPE:
                    p.quit()
            if event.type == p.MOUSEBUTTONDOWN:
                pos = p.mouse.get_pos()
                if pos[0] < consts.WIDTH//2:
                    reverse = False
                    chosen = True
                else:
                    reverse = True
                    chosen = True

    if reverse:
            # adding black pawns
        for j in range(consts.DIMENSION):
            b.board[6][j] = Pawn([6, j], 'black', 'pawn') # pos, color, typ)
        
        # adding white pawns
        for j in range(consts.DIMENSION):
            b.board[1][j] = Pawn([1, j], 'white', 'pawn')
        
        # adding white pieces
        b.board[7][0] = Rook([7, 0], 'black', 'rook')
        b.board[7][1] = Knight([7, 1], 'black', 'knight')
        b.board[7][2] = Bishop([7, 2], 'black', 'bishop')
        b.board[7][4] = Queen([7, 4], 'black', 'queen')
        b.board[7][3] = King([7, 3], 'black', 'king')
        b.board[7][5] = Bishop([7, 5], 'black', 'bishop')
        b.board[7][6] = Knight([7, 6], 'black', 'knight')
        b.board[7][7] = Rook([7, 7], 'black', 'rook')

        # adding black pieces
        b.board[0][0] = Rook([0, 0], 'white', 'rook')
        b.board[0][1] = Knight([0, 1], 'white', 'knight')
        b.board[0][2] = Bishop([0, 2], 'white', 'bishop')
        b.board[0][4] = Queen([0, 4], 'white', 'queen')
        b.board[0][3] = King([0, 3], 'white', 'king')
        b.board[0][5] = Bishop([0, 5], 'white', 'bishop')
        b.board[0][6] = Knight([0, 6], 'white', 'knight')
        b.board[0][7] = Rook([0, 7], 'white', 'rook')

    else:
        # adding white pawns
        for j in range(consts.DIMENSION):
            b.board[6][j] = Pawn([6, j], 'white', 'pawn') # pos, color, typ)
        
        # adding black pawns
        for j in range(consts.DIMENSION):
            b.board[1][j] = Pawn([1, j], 'black', 'pawn')
        
        # adding white pieces
        b.board[7][0] = Rook([7, 0], 'white', 'rook')
        b.board[7][1] = Knight([7, 1], 'white', 'knight')
        b.board[7][2] = Bishop([7, 2], 'white', 'bishop')
        b.board[7][3] = Queen([7, 3], 'white', 'queen')
        b.board[7][4] = King([7, 4], 'white', 'king')
        b.board[7][5] = Bishop([7, 5], 'white', 'bishop')
        b.board[7][6] = Knight([7, 6], 'white', 'knight')
        b.board[7][7] = Rook([7, 7], 'white', 'rook')

        # adding black pieces
        b.board[0][0] = Rook([0, 0], 'black', 'rook')
        b.board[0][1] = Knight([0, 1], 'black', 'knight')
        b.board[0][2] = Bishop([0, 2], 'black', 'bishop')
        b.board[0][3] = Queen([0, 3], 'black', 'queen')
        b.board[0][4] = King([0, 4], 'black', 'king')
        b.board[0][5] = Bishop([0, 5], 'black', 'bishop')
        b.board[0][6] = Knight([0, 6], 'black', 'knight')
        b.board[0][7] = Rook([0, 7], 'black', 'rook')

    board_stack.append([copy.deepcopy(b.board), [fifty_move_rule, num_pieces, has_any_pawn_moved]])

    white = Player('white')
    white.is_turn_player = True
    black = Player('black')
    piece = None
    
    board_count[board_to_string(b.board)] = board_count.get(board_to_string(b.board), 0) + 1

    while run:
        
        draw_board(screen, row, col, update)
        draw_pieces(screen, b.board)
        clock.tick(consts.FPS)
        p.display.flip()

        player = white if white.is_turn_player else black
        
        if len(board_stack):
            if b.checkmate(player, board_stack[-1][0], b.board, reverse):
                color = 'White' if player.color == 'black' else 'Black'
                quit_game(color + ' wins by checkmate')

        if b.stalemate(player, b.board, reverse):
            quit_game('Stalemate')

        curr_piece_count = 0
        white_pieces, black_pieces = [], []

        for i in range(consts.DIMENSION):
            for j in range(consts.DIMENSION):
                if b.board[i][j] and b.board[i][j].color == 'white':
                    white_pieces.append(b.board[i][j])
                elif b.board[i][j] and b.board[i][j].color == 'black':
                    black_pieces.append(b.board[i][j])
        
        if b.insuficient_material(white_pieces, black_pieces):
            quit_game('Draw due to insuficient material')
        
        if fifty_move_rule == 100:
            quit_game('Draw due to no progress')

        if board_count.get(board_to_string(b.board)) and board_count[board_to_string(b.board)] == 3:
            quit_game('Draw by repetition')

        for event in p.event.get():
            if event.type == p.QUIT:
                run = False
            if event.type == p.KEYDOWN:
                if event.key == p.K_ESCAPE:
                    p.quit()
            if event.type == p.KEYDOWN:
                if event.key == p.K_z and p.key.get_mods() & p.KMOD_LCTRL:
                    if len(board_stack):
                        if board_count.get(board_to_string(b.board)):
                            board_count[board_to_string(b.board)] -= 1
                            
                        b.board, [fifty_move_rule, curr_piece_count, has_any_pawn_moved] = board_stack.pop()
                        update = False
                        white.is_turn_player, black.is_turn_player = switch_players(white)

            if event.type == p.MOUSEBUTTONDOWN:
                pos = p.mouse.get_pos()
                row, col = get_mouse_row_col(pos)
                if b.board[row][col]:
                    if (b.board[row][col].color == white.color and white.is_turn_player) or (b.board[row][col].color == black.color and black.is_turn_player):
                        piece = b.board[row][col]
                        update = True

                if sq_selected == [row, col]: # the user clicked the same square twice
                    sq_selected = [] # deselect
                    player_clicks = [] # clear player clicks
                else:
                    sq_selected = [row, col]
                    player_clicks.append(sq_selected) # append for both 1st and 2nd clicks
                    if (not piece and len(player_clicks) == 1):
                        sq_selected = [] # deselect
                        player_clicks = [] # clear player clicks
                        update = False
                    if len(player_clicks) == 2: # after 2nd click
                        if b.board[player_clicks[0][0]][player_clicks[0][1]] and b.board[player_clicks[1][0]][player_clicks[1][1]] and b.board[player_clicks[0][0]][player_clicks[0][1]].color == b.board[player_clicks[1][0]][player_clicks[1][1]].color:
                            sq_selected = [] # deselect
                            player_clicks = [] # clear player clicks
                            update = False
                            continue
                        
                        if piece:
                            row, col = player_clicks[1][0], player_clicks[1][1]
                            if [row, col] in piece.get_possible_moves(b.board, reverse) and not b.is_pinned(piece, player, [row, col], reverse):
                                board_stack.append([copy.deepcopy(b.board), [fifty_move_rule, curr_piece_count, has_any_pawn_moved]])
                                
                                prev_board = board_stack[-1][0]
                                piece_moved = piece
                                ambiguity_state = check_ambiguity_state(prev_board, piece_moved, [row, col])
                                start_pos = [player_clicks[0][0], player_clicks[0][1]]
                                end_pos = [row, col]

                                b.board = piece.move([row, col], b.board)
                                board_count[board_to_string(b.board)] = board_count.get(board_to_string(b.board), 0) + 1
                                
                                if piece.typ == 'pawn':
                                    has_any_pawn_moved = True
                                    
                                    if (piece.color == 'white' and row == 0 and not reverse) or (piece.color == 'black' and row == 7 and not reverse) or (piece.color == 'white' and row == 7 and reverse) or (piece.color == 'black' and row == 0 and reverse):
                                        board_count[board_to_string(b.board)] -= 1
                                        out = None
                                        while not out:
                                            draw_text(screen, 40, 'Choose promotion q: Queen  n: Knight  r: Rook  b: Bishop')
                                            p.display.update()
                                            for event in p.event.get():
                                                if event.type == p.KEYDOWN:
                                                    out = promote(b.board, [row, col], key_to_char(event.key))
                                                    if out:
                                                        b.board = out
                                                        break
                                        board_count[board_to_string(b.board)] = board_count.get(board_to_string(b.board), 0) + 1

                                curr_board = b.board
                                is_check = b.under_check(black if white.is_turn_player else white, curr_board, reverse)
                                is_checkmate = b.checkmate(black if white.is_turn_player else white, prev_board, curr_board, reverse)
                                game_log(piece_moved, start_pos, end_pos, prev_board, curr_board, is_check, is_checkmate, ambiguity_state, False, reverse)
                                
                                curr_piece_count = 0
                                for i in range(consts.DIMENSION):
                                    for j in range(consts.DIMENSION):
                                        if b.board[i][j]:
                                            curr_piece_count += 1
                                if num_pieces == curr_piece_count and not has_any_pawn_moved:
                                    fifty_move_rule += 1

                                if has_any_pawn_moved or (num_pieces != curr_piece_count):
                                    fifty_move_rule = 0 # incremented if the same number of pieces remains
                                    has_any_pawn_moved = False # if a pawn moves it's set to true
                                    num_pieces = curr_piece_count # changes only if curr_piece_count is different
                                        
                                update = False
                                white.is_turn_player, black.is_turn_player = switch_players(white)

                            elif piece.typ == 'king':
                                board_stack.append([copy.deepcopy(b.board), [fifty_move_rule, curr_piece_count, has_any_pawn_moved]])
                                
                                start_pos = piece.pos
                                out = piece.castle(player, b, [row, col], reverse)
                                if out:
                                    b.board = out
                                    
                                    piece_moved = piece
                                    curr_board = b.board
                                    is_check = b.under_check(black if white.is_turn_player else white, curr_board, reverse)
                                    is_checkmate = b.checkmate(black if white.is_turn_player else white, prev_board, curr_board, reverse)
                                    end_pos = [row, col]
                                    game_log(piece_moved, start_pos, end_pos, prev_board, curr_board, is_check, is_checkmate, ambiguity_state, False, reverse)

                                    board_count[board_to_string(b.board)] = board_count.get(board_to_string(b.board), 0) + 1
                                    curr_piece_count = 0
                                    for i in range(consts.DIMENSION):
                                        for j in range(consts.DIMENSION):
                                            if b.board[i][j]:
                                                curr_piece_count += 1
                                    if num_pieces == curr_piece_count and not has_any_pawn_moved:
                                        fifty_move_rule += 1

                                    if has_any_pawn_moved or (num_pieces != curr_piece_count):
                                        fifty_move_rule = 0 # incremented if the same number of pieces remains
                                        has_any_pawn_moved = False # if a pawn moves it's set to true
                                        num_pieces = curr_piece_count # changes only if curr_piece_count is different

                                    update = False
                                    white.is_turn_player, black.is_turn_player = switch_players(white)

                                else:
                                    board_stack.pop()

                            elif piece.typ == 'pawn' and len(board_stack) > 0:
                                board_stack.append([copy.deepcopy(b.board), [fifty_move_rule, curr_piece_count, has_any_pawn_moved]])
                                out = piece.en_passant(board_stack[-2][0], b.board, [row, col], reverse)
                                if out and not b.under_check(player, out, reverse):
                                    
                                    has_any_pawn_moved = True
                                    b.board = out
                                    curr_board = b.board
                                    is_check = b.under_check(player, curr_board, reverse)
                                    is_checkmate = b.checkmate(player, prev_board, curr_board, reverse)
                                    game_log(piece_moved, start_pos, end_pos, prev_board, curr_board, is_check, is_checkmate, ambiguity_state, True, reverse)
                                    
                                    board_count[board_to_string(b.board)] = board_count.get(board_to_string(b.board), 0) + 1
                                    
                                    curr_piece_count = 0
                                    for i in range(consts.DIMENSION):
                                        for j in range(consts.DIMENSION):
                                            if b.board[i][j]:
                                                curr_piece_count += 1
                                    if num_pieces == curr_piece_count and not has_any_pawn_moved:
                                        fifty_move_rule += 1

                                    if has_any_pawn_moved or (num_pieces != curr_piece_count):
                                        fifty_move_rule = 0 # incremented if the same number of pieces remains
                                        has_any_pawn_moved = False # if a pawn moves it's set to true
                                        num_pieces = curr_piece_count # changes only if curr_piece_count is different

                                    update = False
                                    white.is_turn_player, black.is_turn_player = switch_players(white)
                                else:
                                    board_stack.pop()

                        
                        piece = None
                        sq_selected = [] # deselect
                        player_clicks = [] # clear player clicks
                        update = False
                        