from animebot.chess.main import ChessGame

game = ChessGame()
r = game.make_move(['d2', 'd3'])
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

r = game.make_move(['c1', 'd2'])
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