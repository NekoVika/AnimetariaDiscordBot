from copy import deepcopy
from .helper import Point


class ChessPiece(object):
    ASCII_white = None
    ASCII_black = None
    name = None

    def __init__(self, player, position):
        self.player = player
        self.player.figures.append(self)
        self.position = position

    def viable_moves(self):  # FIXME: merge this into validation maybe
        return []

    def validate_move(self, to, field):
        return False

    def __repr__(self):
        return getattr(self, 'ASCII_{}'.format(self.player.color))

    def __str__(self):
        return self.name


class ChessPawn(ChessPiece):
    ASCII_white = '♙'
    ASCII_black = '♟'
    name = 'pawn'

    def __init__(self, *args, **kwargs):
        super(ChessPawn, self).__init__(*args, **kwargs)

    def viable_moves(self):
        return [self.position + Point(0, 1 * self.player.mod),
                self.position + Point(0, 2 * self.player.mod),
                self.position + Point(-1, 1 * self.player.mod),
                self.position + Point(1, 1 * self.player.mod)]

    def validate_move(self, to, field):  # FIXME
        vm = self.viable_moves()
        cell_to = field.get_by_coord(to)
        if to in filter(bool, vm):
            if to == vm[0] and cell_to.piece is not None:
                return False
            if (to == vm[2] or to ==vm[3]) and cell_to is None:
                return False
            if to == vm[1] and (not field.is_path_clear(self.position, to) or
                                not ((self.position.y == 1 and self.player.mod == 1)
                                     or (self.position.y == 7 and self.player.mod == -1))):
                return False
            return True
        return False


class ChessBishop(ChessPiece):
    ASCII_white = '♗'
    ASCII_black = '♝'
    name = 'bishop'

    def __init__(self, *args, **kwargs):
        super(ChessBishop, self).__init__(*args, **kwargs)

    def viable_moves(self):
        all_moves = []
        for i in range(1, 9):
            moves = filter(bool, [self.position+Point(i, i), self.position+Point(i, -i),
                                  self.position+Point(-i, i), self.position+Point(-i, -i)])
            if not moves:
                break
            all_moves.extend(moves)
        return all_moves

    def validate_move(self, to, field):
        vm = self.viable_moves()
        # cell_to = field.get_by_coord(to)
        if to in vm and field.is_path_clear(self.position, to):

            return True
        return False


class ChessKnight(ChessPiece):
    ASCII_white = '♘'
    ASCII_black = '♞'
    name = 'knight'

    def __init__(self, *args, **kwargs):
        super(ChessKnight, self).__init__(*args, **kwargs)

    def viable_moves(self):
        return filter(bool, [self.position + Point(1, 2), self.position + Point(-1, 2),
                             self.position + Point(2, 1), self.position + Point(-2, 1),
                             self.position + Point(2, -1), self.position + Point(-2, -1),
                             self.position + Point(1, -2), self.position + Point(-1, -2),
                             ])

    def validate_move(self, to, field):
        vm = self.viable_moves()
        if to in vm and field.is_path_clear(self.position, to):
            return True
        return False


class ChessRook(ChessPiece):
    ASCII_white = '♖'
    ASCII_black = '♜'
    name = 'rook'

    def __init__(self, *args, **kwargs):
        super(ChessRook, self).__init__(*args, **kwargs)

    def viable_moves(self):
        all_moves = []
        for i in range(1, 9):
            moves = filter(bool, [self.position+Point(i, 0), self.position+Point(-i, 0),
                                  self.position+Point(0, i), self.position+Point(0, -i),
                                  self.position + Point(i, i), self.position + Point(i, -i),
                                  self.position + Point(-i, i), self.position + Point(-i, -i)]
                           )
            if not moves:
                break
            all_moves.extend(moves)
        return all_moves

    def validate_move(self, to, field):
        vm = self.viable_moves()
        if to in vm and field.is_path_clear(self.position, to):
            return True
        return False


class ChessQueen(ChessPiece):
    ASCII_white = '♕'
    ASCII_black = '♛'
    name = 'queen'

    def viable_moves(self):
        all_moves = []
        for i in range(1, 9):
            moves = filter(bool, [self.position+Point(i, 0), self.position+Point(-i, 0),
                                  self.position+Point(0, i), self.position+Point(0, -i)])
            if not moves:
                break
            all_moves.extend(moves)
        return all_moves

    def validate_move(self, to, field):
        vm = self.viable_moves()
        if to in vm:
            return True
        return False

    def __init__(self, *args, **kwargs):
        super(ChessQueen, self).__init__(*args, **kwargs)


class ChessKing(ChessPiece):
    ASCII_white = '♔'
    ASCII_black = '♚'
    name = 'king'

    def __init__(self, *args, **kwargs):
        super(ChessKing, self).__init__(*args, **kwargs)