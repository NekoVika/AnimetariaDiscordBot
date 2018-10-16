from .pieces import ChessPawn, ChessBishop, ChessKing, ChessKnight, ChessQueen, ChessRook
from .helper import Point

import re
import logging
import math

M2C = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
C2M = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}


def id2coord(id_):
    return Point(M2C[id_[0]], int(id_[1]) - 1)


def coord2id(coord):
    return


class ChessGame(object):
    MOVE_RE = re.compile(r'[abcdefgh][12345678]')

    def __init__(self, custom_field=None):
        self.player1 = ChessPlayer('white', 1)
        self.player2 = ChessPlayer('black', -1)
        self.current_player = self.player1

        if custom_field is not None:
            self.field = custom_field
        else:
            self.field = ChessField()
            self.prepare_field()

    def prepare_field(self):   # FIXME: ugly?
        # player 1
        self.field.init_piece('a1', self.player1, ChessRook)
        self.field.init_piece('b1', self.player1, ChessKnight)
        self.field.init_piece('c1', self.player1, ChessBishop)
        self.field.init_piece('d1', self.player1, ChessQueen)
        self.field.init_piece('e1', self.player1, ChessKing)
        self.field.init_piece('f1', self.player1, ChessBishop)
        self.field.init_piece('g1', self.player1, ChessKnight)
        self.field.init_piece('h1', self.player1, ChessRook)
        self.field.init_piece('a2', self.player1, ChessPawn)
        self.field.init_piece('b2', self.player1, ChessPawn)
        self.field.init_piece('c2', self.player1, ChessPawn)
        self.field.init_piece('d2', self.player1, ChessPawn)
        self.field.init_piece('e2', self.player1, ChessPawn)
        self.field.init_piece('f2', self.player1, ChessPawn)
        self.field.init_piece('g2', self.player1, ChessPawn)
        self.field.init_piece('h2', self.player1, ChessPawn)

        # player 2
        self.field.init_piece('a8', self.player2, ChessRook)
        self.field.init_piece('b8', self.player2, ChessKnight)
        self.field.init_piece('c8', self.player2, ChessBishop)
        self.field.init_piece('d8', self.player2, ChessQueen)
        self.field.init_piece('e8', self.player2, ChessKing)
        self.field.init_piece('f8', self.player2, ChessBishop)
        self.field.init_piece('g8', self.player2, ChessKnight)
        self.field.init_piece('h8', self.player2, ChessRook)
        self.field.init_piece('a7', self.player2, ChessPawn)
        self.field.init_piece('b7', self.player2, ChessPawn)
        self.field.init_piece('c7', self.player2, ChessPawn)
        self.field.init_piece('d7', self.player2, ChessPawn)
        self.field.init_piece('e7', self.player2, ChessPawn)
        self.field.init_piece('f7', self.player2, ChessPawn)
        self.field.init_piece('g7', self.player2, ChessPawn)
        self.field.init_piece('h7', self.player2, ChessPawn)

    def change_player(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def make_move(self, move):
        if not self.validate_spelling(move):
            return dict(code=1, message="Not valid move")
        print('Move', *move)
        fr, to = id2coord(move[0]), id2coord(move[1])
        piece = self.field.get_by_coord(fr).piece

        if piece is None or piece.player != self.current_player:
            return dict(code=1, message="You can't move this")

        if not piece.validate_move(to, self.field):
            return dict(code=1, message="You can't move {} like this".format(piece))

        self.field.move(fr, to)

        # self.field.move(fr, to)
        return dict(code=0, message=self.field.ascii())  # debugging

    def get_figure(self, fr):
        for figure in self.current_player.figures:
            if figure.pos == fr:
                return figure

    def validate_spelling(self, move):
        if not (isinstance(move, (list, tuple)) and len(move) == 2):
            return False
        return all(map(self.MOVE_RE.match, move))


class ChessField(object):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    numbers = list(range(1, 9))

    def __init__(self, *args):
        self._field = []
        for i, l in enumerate(self.letters):
            for j, n in enumerate(self.numbers):
                self._field.append(ChessFieldCell('{}{}'.format(l, n), 'black' if (i+n) % 2 else 'white', i, j))

    def get_field(self):
        return self._field

    def move(self, fr, to):
        cell_fr = self.get_by_coord(fr)
        piece = cell_fr.pickup_piece()
        cell_to = self.get_by_coord(to)
        if cell_to.piece is None:
            cell_to.put_piece(piece)

    def is_path_clear(self, fr, to):
        beets = self.get_cell_between(fr, to)
        if not beets:
            return True
        return not(all(beets))

    def get_cell_between(self, fr, to):
        res = []
        x = fr.x
        y = fr.y
        if x == to.x:
            for i in range(1, to.y-fr.y):
                res.append(self.get_by_coord(x, y+i))
            return res
        if y == to.y:
            for i in range(1, to.x-fr.x):
                res.append(self.get_by_coord(x+i, y))
            return res
        if abs(to.y - y) == abs(to.x - x):
            for i in range(1, to.x - x):
                res.append(self.get_by_coord(x+i, y+i))
            return res
        return []

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

    def get_by_coord(self, x, y=None):
        p = x if isinstance(x, Point) else Point(x, y)
        r = list(filter(lambda obj: obj.point == p, self._field))  # ugly
        if not r:
            raise IndexError('Wrong cell coordinates')
        return r[0]

    def init_piece(self, id_, player, pc):
        cell = self.get_by_id(id_)
        cell.init_piece(pc, player)

    def __iter__(self):
        return iter(self._field)


class ChessFieldCell(object):
    ASCII_white = '▢ '
    ASCII_black = '▦ '

    def __init__(self, id_, color, x, y):
        self.id = id_
        self.color = color
        self.point = Point(x, y)
        self.piece = None

    def init_piece(self, pc, player):
        self.piece = pc(player, self.point)

    def pickup_piece(self):
        piece = self.piece
        self.piece = None
        return piece

    def put_piece(self, piece):
        piece.position = self.point
        self.piece = piece

    def __repr__(self):
        if self.piece is not None:
            return repr(self.piece)
        return getattr(self, 'ASCII_{}'.format(self.color))

    def __bool__(self):
        return False if self.piece is None else True


class ChessPlayer(object):
    def __init__(self, color, mod):
        self.mod = mod
        self.figures = []
        self.color = color

    def __str__(self):
        return 'Player {}'.format(self.color)
