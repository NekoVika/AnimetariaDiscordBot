import re

class ChessGame(object):
    MOVE_RE = re.compile(r'[abcdefgh][12345678]')
    m2c = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

    def __init__(self):
        self.field = ChessField()
        self.prepare_field()
        self.player1 = ChessPlayer()
        self.player2 = ChessPlayer()
        self.current = self.player1

    def prepare_field(self):
        pass

    def change_player(self):
        self.current = self.player2 if self.current == self.player1 else self.player1

    def make_move(self, move):
        print('@@@', move)
        if not self.validate_spelling(move):
            return dict(code=1, message="Not valid move")
        fr, to = self.to_coord(move)
        # print('move', fr, to)
        # figure = self.get_figure(fr)
        # if not figure:
        #     return dict(code=1, message="You can't move this")
        return dict(code=0, message=self.field)  # debugging

    def to_coord(self, move):
        return [[self.m2c[m[0]], int(m[1])-1] for m in move]

    def get_figure(self, fr):
        for figure in self.current.figures:
            if figure.pos == fr:
                return figure

    def validate_spelling(self, move):
        if not (isinstance(move, (list, tuple)) and len(move) == 2):
            return False
        return any(map(self.MOVE_RE.match, move))


class ChessField(object):
    def __init__(self, *args):
        self._ = [[None]*8]*8

    def __iter__(self):
        return iter(self._)

class ChessPlayer(object):
    def __init__(self):
        self.figures = []
