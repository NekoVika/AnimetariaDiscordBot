from .helper import Point


class ChessPiece(object):
    ASCII_white = None
    ASCII_black = None
    name = None

    def __init__(self, player, position, game):
        self.player = player
        self.player.figures.append(self)
        self.position = position
        self.game = game

    def validate_move(self, to):
        pass

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

    def validate_move(self, to):
        viable_moves = [self.position+Point(-1, 1*self.player.mod), self.position+Point(0, 1*self.player.mod),
                        self.position + Point(1, 1 * self.player.mod), self.position+Point(0, 2*self.player.mod)]
        print('###', to)
        print('vvv', viable_moves)
        return to in viable_moves


class ChessBishop(ChessPiece):
    ASCII_white = '♗'
    ASCII_black = '♝'
    name = 'bishop'

    def __init__(self, *args, **kwargs):
        super(ChessBishop, self).__init__(*args, **kwargs)


class ChessKnight(ChessPiece):
    ASCII_white = '♘'
    ASCII_black = '♞'
    name = 'knight'

    def __init__(self, *args, **kwargs):
        super(ChessKnight, self).__init__(*args, **kwargs)


class ChessRook(ChessPiece):
    ASCII_white = '♖'
    ASCII_black = '♜'
    name = 'rook'

    def __init__(self, *args, **kwargs):
        super(ChessRook, self).__init__(*args, **kwargs)


class ChessQueen(ChessPiece):
    ASCII_white = '♕'
    ASCII_black = '♛'
    name = 'queen'

    def __init__(self, *args, **kwargs):
        super(ChessQueen, self).__init__(*args, **kwargs)


class ChessKing(ChessPiece):
    ASCII_white = '♔'
    ASCII_black = '♚'
    name = 'king'

    def __init__(self, *args, **kwargs):
        super(ChessKing, self).__init__(*args, **kwargs)