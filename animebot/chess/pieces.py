import sys
from copy import deepcopy
from .helper import Point, another_color

ABBR = {
    'P': 'ChessPawn',
    'R': 'ChessRook',
    'N': 'ChessKnight',
    'B': 'ChessBishop',
    'K': 'ChessKing',
    'Q': 'ChessQueen',
}


def create_piece(piece, position, color='white'):
    if len(piece) == 1:
        color = 'black' if piece.isupper() else 'white'
        piece = ABBR[piece.upper()]
    module = sys.modules[__name__]
    return module.__dict__[piece](color, position)


class ChessPiece(object):
    ASCII_white = None
    ASCII_black = None
    name = None

    def __init__(self, color, position):
        self.color = color
        self.position = position

    def _viable_moves(self, field, diagonal=False, orthogonal=False, radius=8):
        viable_moves = []
        orth = ((-1, 0), (0, -1), (0, 1), (1, 0))
        diag = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        if diagonal and orthogonal:
            moves = diag + orth
        elif orthogonal:
            moves = orth
        else:
            moves = diag

        for x, y in moves:
            hit = False
            for step in range(1, radius+1):
                if hit:
                    break
                dest = self.position + Point(step*x, step*y)
                dest_cell = field.get_by_coord(dest)
                if not dest_cell:
                    continue
                if not dest_cell.occupied:
                    viable_moves.append(dest)
                elif dest_cell.piece.color == self.color:
                    hit = True
                else:
                    viable_moves.append(dest)
                    hit = True

        return filter(bool, viable_moves)

    def validate_move(self, to, field):
        return False

    def __repr__(self):
        return getattr(self, 'ASCII_{}'.format(self.color))

    def __str__(self):
        return self.name


class ChessPawn(ChessPiece):
    ASCII_white = '♙'
    ASCII_black = '♟'
    name = 'pawn'

    def __init__(self, *args, **kwargs):
        super(ChessPawn, self).__init__(*args, **kwargs)

    def viable_moves(self, field):
        if self.color == 'white':
            home, direction = 1, 1
        else:
            home, direction = 6, -1
        viable_moves = []

        forward_dest = self.position + Point(0, direction)
        dest_cell = field.get_by_coord(forward_dest)
        if dest_cell and not field.get_by_coord(forward_dest).occupied:
            viable_moves.append(forward_dest)
            double_forward_dest = self.position + Point(0, direction*2)
            dest_cell = field.get_by_coord(double_forward_dest)
            if dest_cell and self.position.y == home and not dest_cell.occupied:
                viable_moves.append(double_forward_dest)

        for side in (-1, 1):
            enemy_dest = self.position + Point(side, direction)
            enemy_cell = field.get_by_coord(enemy_dest)
            if enemy_cell and enemy_cell.occupied \
                    and enemy_cell.piece.color == another_color(self.color):
                viable_moves.append(enemy_dest)
        return viable_moves

    def validate_move(self, to, field):  # FIXME
        vm = self.viable_moves(field)
        return to in vm


class ChessBishop(ChessPiece):
    ASCII_white = '♗'
    ASCII_black = '♝'
    name = 'bishop'

    def __init__(self, *args, **kwargs):
        super(ChessBishop, self).__init__(*args, **kwargs)

    def viable_moves(self, field):
        return self._viable_moves(field, True, False)

    def validate_move(self, to, field):
        vm = self.viable_moves(field)
        return to in vm


class ChessKnight(ChessPiece):
    ASCII_white = '♘'
    ASCII_black = '♞'
    name = 'knight'

    def __init__(self, *args, **kwargs):
        super(ChessKnight, self).__init__(*args, **kwargs)

    def viable_moves(self, field):
        points = (Point(1, 2), Point(-1, 2), Point(2, 1), Point(-2, 1),
                  Point(2, -1), Point(-2, -1), Point(1, -2), Point(-1, -2))
        viable_moves = []
        for p in points:
            dest = self.position + p
            dest_cell = field.get_by_coord(dest)
            if not dest_cell:
                continue
            if not dest_cell.occupied or dest_cell.piece.color != self.color:
                viable_moves.append(dest)
        return viable_moves

    def validate_move(self, to, field):
        vm = self.viable_moves(field)
        return to in vm


class ChessRook(ChessPiece):
    ASCII_white = '♖'
    ASCII_black = '♜'
    name = 'rook'

    def __init__(self, *args, **kwargs):
        super(ChessRook, self).__init__(*args, **kwargs)

    def viable_moves(self, field):
        return self._viable_moves(field, False, True)

    def validate_move(self, to, field):
        vm = self.viable_moves(field)
        return to in vm


class ChessQueen(ChessPiece):
    ASCII_white = '♕'
    ASCII_black = '♛'
    name = 'queen'

    def viable_moves(self, field):
        return self._viable_moves(field, True, True)

    def validate_move(self, to, field):
        vm = self.viable_moves(field)
        return to in vm

    def __init__(self, *args, **kwargs):
        super(ChessQueen, self).__init__(*args, **kwargs)


class ChessKing(ChessPiece):
    ASCII_white = '♔'
    ASCII_black = '♚'
    name = 'king'

    def viable_moves(self, field):
        return self._viable_moves(field, True, True, 1)

    def __init__(self, *args, **kwargs):
        super(ChessKing, self).__init__(*args, **kwargs)