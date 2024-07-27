class Piece():
    def __init__(self, pos, color, typ):
        self.pos = pos
        self.color = color
        self.typ = typ
        self.has_moved = False
    
    def get_possible_moves(self, board, reverse):
        pass

    def move(self, new_pos, board): # return board and don't modify a class board
        board[new_pos[0]][new_pos[1]] = self
        board[self.pos[0]][self.pos[1]] = None
        self.pos = new_pos
        self.has_moved = True
        return board