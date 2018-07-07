import re
from animebot.chess.pieces import ChessPawn, ChessBishop, ChessKing, ChessKnight, ChessQueen, ChessRook

class ChessGame(object):
    MOVE_RE = re.compile(r'[abcdefgh][12345678]')
    m2c = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

    def __init__(self):
        self.field = ChessField()
        self.player1 = ChessPlayer('white')
        self.player2 = ChessPlayer('black')
        self.prepare_field()
        self.current = self.player1

    def prepare_field(self):
        # player 1
        self.field.init_piece('a1', ChessRook(player=self.player1))
        self.field.init_piece('b1', ChessKing(player=self.player1))
        self.field.init_piece('c1', ChessBishop(player=self.player1))
        self.field.init_piece('d1', ChessQueen(player=self.player1))
        self.field.init_piece('e1', ChessKing(player=self.player1))
        self.field.init_piece('f1', ChessBishop(player=self.player1))
        self.field.init_piece('g1', ChessKnight(player=self.player1))
        self.field.init_piece('h1', ChessRook(player=self.player1))
        self.field.init_piece('a2', ChessPawn(player=self.player1))
        self.field.init_piece('b2', ChessPawn(player=self.player1))
        self.field.init_piece('c2', ChessPawn(player=self.player1))
        self.field.init_piece('d2', ChessPawn(player=self.player1))
        self.field.init_piece('e2', ChessPawn(player=self.player1))
        self.field.init_piece('f2', ChessPawn(player=self.player1))
        self.field.init_piece('g2', ChessPawn(player=self.player1))
        self.field.init_piece('h2', ChessPawn(player=self.player1))

        # player 2
        self.field.init_piece('a8', ChessRook(player=self.player2))
        self.field.init_piece('b8', ChessKing(player=self.player2))
        self.field.init_piece('c8', ChessBishop(player=self.player2))
        self.field.init_piece('d8', ChessQueen(player=self.player2))
        self.field.init_piece('e8', ChessKing(player=self.player2))
        self.field.init_piece('f8', ChessBishop(player=self.player2))
        self.field.init_piece('g8', ChessKnight(player=self.player2))
        self.field.init_piece('h8', ChessRook(player=self.player2))
        self.field.init_piece('a7', ChessPawn(player=self.player2))
        self.field.init_piece('b7', ChessPawn(player=self.player2))
        self.field.init_piece('c7', ChessPawn(player=self.player2))
        self.field.init_piece('d7', ChessPawn(player=self.player2))
        self.field.init_piece('e7', ChessPawn(player=self.player2))
        self.field.init_piece('f7', ChessPawn(player=self.player2))
        self.field.init_piece('g7', ChessPawn(player=self.player2))
        self.field.init_piece('h7', ChessPawn(player=self.player2))

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
        return dict(code=0, message=self.field.ascii())  # debugging

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
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    numbers = list(range(1, 9))

    def __init__(self, *args):
        self._field = []
        for i, l in enumerate(self.letters):
            for j, n in enumerate(self.numbers):
                self._field.append(ChessFieldCell('{}{}'.format(l, n), 'black' if (i+n) % 2 else 'white', i, j))

    def ascii(self):
        res = []
        for i, l in enumerate(self.numbers):
            r = []
            for j, n in enumerate(self.letters):
                r.append(repr(self.get_by_coord(j, i)))
            res.append(r)
        return res

    def get_by_id(self, id_):
        r = list(filter(lambda x: x.id == id_, self._field))  # ugly
        if not r:
            raise IndexError('Wrong cell ID')
        return r[0]

    def get_by_coord(self, x, y):
        r = list(filter(lambda obj: obj.point == (x, y), self._field))  # ugly
        if not r:
            raise IndexError('Wrong cell coordinates')
        return r[0]

    def init_piece(self, id_, piece):
        cell = self.get_by_id(id_)
        cell.init_piece(piece)

    def __iter__(self):
        return iter(self._field)


class ChessFieldCell(object):
    ASCII_white = '▢'
    ASCII_black = '▦'

    def __init__(self, id_, color, x, y):
        self.id = id_
        self.color = color
        self.point = (x, y)
        self.piece = None

    def init_piece(self, piece):
        self.piece = piece

    def __repr__(self):
        if self.piece is not None:
            return repr(self.piece)
        return getattr(self, 'ASCII_{}'.format(self.color))


class ChessPlayer(object):
    def __init__(self, color):
        self.figures = []
        self.color = color
