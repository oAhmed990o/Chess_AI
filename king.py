from piece import Piece

class King(Piece):
    def __init__(self, pos, color, typ):
        super().__init__(pos, color, typ)

    def castle(self, player, board, position, reverse):
        if abs(self.pos[1] - position[1]) != 2 or self.has_moved:
            return
        b = board.board
        clicked_row, clicked_col = position
        if not reverse:
            if clicked_col < self.pos[1]: # long castling
                if b[clicked_row][clicked_col-2] and b[clicked_row][clicked_col-2].typ == 'rook' and (not b[clicked_row][clicked_col-2].has_moved) and b[clicked_row][clicked_col-2].color == self.color:
                    for i in range(self.pos[1]-1, 0, -1):
                        if b[clicked_row][i] or board.is_square_unsafe(player, [clicked_row , i], reverse):
                            return
                    if board.under_check(player, b, reverse):
                        return
                    else:
                        # do the castling
                        # change the saved king pos int he board constructor later*
                        b[clicked_row][clicked_col] = self
                        b[self.pos[0]][self.pos[1]] = None
                        self.pos = [clicked_row, clicked_col]
                        self.has_moved = True
                        b[clicked_row][clicked_col+1] = b[clicked_row][clicked_col-2] # move the rook
                        b[clicked_row][clicked_col-2] = None
                        b[clicked_row][clicked_col+1].pos = [clicked_row, clicked_col+1]
                        b[clicked_row][clicked_col+1].has_moved = True
                        return b
                else:
                    return
            else: # short castling
                if b[clicked_row][clicked_col+1] and b[clicked_row][clicked_col+1].typ == 'rook' and (not b[clicked_row][clicked_col+1].has_moved) and b[clicked_row][clicked_col+1].color == self.color:
                    for i in range(self.pos[1]+1, 7):
                        if b[clicked_row][i] or board.is_square_unsafe(player, [clicked_row , i], reverse):
                            return
                    if board.under_check(player, b, reverse):
                        return
                    else:
                        # do the castling
                        # change the saved king pos int he board constructor later*
                        b[clicked_row][clicked_col] = self
                        b[self.pos[0]][self.pos[1]] = None
                        self.pos = [clicked_row, clicked_col]
                        self.has_moved = True
                        b[clicked_row][clicked_col-1] = b[clicked_row][clicked_col+1] # move the rook
                        b[clicked_row][clicked_col+1] = None
                        b[clicked_row][clicked_col-1].pos = [clicked_row, clicked_col-1]
                        b[clicked_row][clicked_col-1].has_moved = True
                        return b
                else:
                    return
        else:
            if clicked_col > self.pos[1]: # long castling
                if b[clicked_row][clicked_col+2] and b[clicked_row][clicked_col+2].typ == 'rook' and (not b[clicked_row][clicked_col+2].has_moved) and b[clicked_row][clicked_col+2].color == self.color:
                    for i in range(self.pos[1]+1, 7):
                        if b[clicked_row][i] or board.is_square_unsafe(player, [clicked_row , i], reverse):
                            return
                    if board.under_check(player, b, reverse):
                        return
                    else:
                        # do the castling
                        # change the saved king pos int he board constructor later*
                        b[clicked_row][clicked_col] = self
                        b[self.pos[0]][self.pos[1]] = None
                        self.pos = [clicked_row, clicked_col]
                        self.has_moved = True
                        b[clicked_row][clicked_col-1] = b[clicked_row][clicked_col+2] # move the rook
                        b[clicked_row][clicked_col+2] = None
                        b[clicked_row][clicked_col-1].pos = [clicked_row, clicked_col-1]
                        b[clicked_row][clicked_col-1].has_moved = True
                        return b
                else:
                    return
            else: # short castling
                if b[clicked_row][clicked_col-1] and b[clicked_row][clicked_col-1].typ == 'rook' and (not b[clicked_row][clicked_col-1].has_moved) and b[clicked_row][clicked_col-1].color == self.color:
                    for i in range(self.pos[1]-1, 0, -1):
                        if b[clicked_row][i] or board.is_square_unsafe(player, [clicked_row , i], reverse):
                            return
                    if board.under_check(player, b, reverse):
                        return
                    else:
                        # do the castling
                        # change the saved king pos int he board constructor later*
                        b[clicked_row][clicked_col] = self
                        b[self.pos[0]][self.pos[1]] = None
                        self.pos = [clicked_row, clicked_col]
                        self.has_moved = True
                        b[clicked_row][clicked_col+1] = b[clicked_row][clicked_col-1] # move the rook
                        b[clicked_row][clicked_col-1] = None
                        b[clicked_row][clicked_col+1].pos = [clicked_row, clicked_col+1]
                        b[clicked_row][clicked_col+1].has_moved = True
                        return b
                else:
                    return


    def get_possible_moves(self, board, reverse):
        moves = []
        x, y = self.pos[0], self.pos[1]
        for curr_x, curr_y in [[x-1, y-1], [x-1, y], [x-1, y+1], [x, y-1], [x, y+1], [x+1, y-1], [x+1, y], [x+1, y+1]]:
            if curr_x >= 0 and curr_y >= 0 and curr_x < 8 and curr_y < 8:
                if board[curr_x][curr_y] is None:
                    moves.append([curr_x, curr_y])
                else:
                    if self.color != board[curr_x][curr_y].color:
                        moves.append([curr_x, curr_y])
                    # should I specify that I can take?
        return moves