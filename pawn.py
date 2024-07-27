from piece import Piece

class Pawn(Piece):
    def __init__(self, pos, color, typ):
        super().__init__(pos, color, typ)

    def en_passant(self, flashback, board, pos, reverse):
        x, y = pos # new position
        r, c = self.pos[0], self.pos[1] # current position
        
        if reverse:
            step = 1 if self.color == 'white' else -1
        else:
            step = -1 if self.color == 'white' else 1
        
        if c-1 >= 0 and board[r][c-1] and board[r][c-1].typ == 'pawn' and board[r][c-1].color != self.color and (board[r+2*step][c-1] is None) and flashback[r+2*step][c-1] and flashback[r+2*step][c-1].typ == 'pawn' and flashback[r+2*step][c-1].color != self.color and (flashback[r][c-1] is None):
            if x == r+step and y == c-1:
                board[r][c-1] = None # remove opp pawn
                board[x][y] = self # move player's pawn
                board[r][c] = None # remove player's pawn from old pos
                self.pos = [x, y] # update piece's pos
                return board

        if c+1 < 8 and board[r][c+1] and board[r][c+1].typ == 'pawn' and board[r][c+1].color != self.color and (board[r+2*step][c+1] is None) and flashback[r+2*step][c+1] and flashback[r+2*step][c+1].typ == 'pawn' and flashback[r+2*step][c+1].color != self.color and (flashback[r][c+1] is None):
            if x == r+step and y == c+1:
                board[r][c+1] = None # remove opp pawn
                board[x][y] = self # move player's pawn
                board[r][c] = None # remove player's pawn from old pos
                self.pos = [x, y] # update piece's pos
                return board
        return

    def get_possible_moves(self, board, reverse):
        moves = []
        x, y = self.pos[0], self.pos[1]

        if reverse:
            step = 1 if self.color == 'white' else -1
        else:
            step = -1 if self.color == 'white' else 1
        
        # two squares forward
        if not self.has_moved:
            if board[x+step][y] is None and board[x+step*2][y] is None:
                moves.append([x+step*2, y])

        # if can take
        if x+step >= 0 and y-1 >= 0 and x+step < 8 and y-1 < 8:
            if board[x+step][y-1] and self.color != board[x+step][y-1].color:
                moves.append([x+step, y-1])
        
        if x+step >= 0 and y+1 >= 0 and x+step < 8 and y+1 < 8:
            if board[x+step][y+1] and self.color != board[x+step][y+1].color:
                moves.append([x+step, y+1])

        # one step forward
        if x+step >= 0 and y >= 0 and x+step < 8 and y < 8:
            if board[x+step][y] is None:
                moves.append([x+step, y])

        return moves