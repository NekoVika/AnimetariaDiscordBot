from animebot.chess.main import ChessGame

game = ChessGame()
r = game.make_move(['a2', 'a3'])
if r['code'] != 0:
    print('!', r['message'])
else:
    message = ''
    for x, col in enumerate(r['message']):
        message += '|'
        for y, pos in enumerate(col):
            message += pos
        message += '|\n'
    print(message)