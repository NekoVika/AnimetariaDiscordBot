class ChessPiece(object):
    ASCII = None

    def __init__(self, player):
        self.player = player
        self.player.figures.append(self)

    def check_move(self, to):
        pass


class ChessPawn(ChessPiece):
    ASCII_white = '♙'
    ASCII_black = '♟'

    def __init__(self, *args, **kwargs):
        super(ChessPawn, self).__init__(*args, **kwargs)


class ChessBishop(ChessPiece):
    ASCII_white = '♗'
    ASCII_black = '♝'

    def __init__(self, *args, **kwargs):
        super(ChessBishop, self).__init__(*args, **kwargs)


class ChessKnight(ChessPiece):
    ASCII_white = '♘'
    ASCII_black = '♞'

    def __init__(self, *args, **kwargs):
        super(ChessKnight, self).__init__(*args, **kwargs)


class ChessRook(ChessPiece):
    ASCII_white = '♖'
    ASCII_black = '♜'

    def __init__(self, *args, **kwargs):
        super(ChessRook, self).__init__(*args, **kwargs)


class ChessQueen(ChessPiece):
    ASCII_white = '♕'
    ASCII_black = '♛'

    def __init__(self, *args, **kwargs):
        super(ChessQueen, self).__init__(*args, **kwargs)


class ChessKing(ChessPiece):
    ASCII_white = '♔'
    ASCII_black = '♚'

    def __init__(self, *args, **kwargs):
        super(ChessKing, self).__init__(*args, **kwargs)