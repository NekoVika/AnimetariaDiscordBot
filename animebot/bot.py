import discord
import asyncio
import yaml


from pathlib import Path
from animebot.tools import randomize, check_condition, reduce_keys, id2user, find_channel
from animebot.chess.main import ChessGame
from animebot.client import AnimeClient

client = AnimeClient()

PWD = Path('.')
ETC_PATH = PWD / 'etc'
LINES = yaml.safe_load((ETC_PATH / 'lines.yaml').open(mode='r', encoding='utf-8'))
CONFIG = yaml.safe_load((ETC_PATH / 'config.yaml').open(mode='r', encoding='utf-8'))


@client.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(client.user.name)
    client.server = client.get_server(CONFIG.get('GUILD_ID'))
    yield from client.change_presence(game=discord.Game(name=CONFIG.get('DEFAULT_GAME')))
    print('------')


@client.event
@asyncio.coroutine
def on_message(message):
    cnt = message.content
    if message.author == client.user:  # FIXME
        return
    if cnt.startswith('!chess'):
        client.game = ChessGame()
        return
    if isinstance(client.game, ChessGame) and message.content.startswith('!move'):
        move = cnt[6:].split(' ')
        result = client.game.make_move(move)
        if result['code'] == 1:
            yield from client.send_message(message.channel, result['message'])
        else:
            yield from client.render_chess(message.channel, result['message'])
        return
    if cnt.startswith('!gameend'):
        client.game = None
        return
    mlines = LINES.get('on_message', [])
    for mitem in mlines:
        if any(map(lambda x: check_condition(cnt.lower(), x), mitem.get('conditions'))):
            answer = randomize(mitem.get('answers'))
            keys = mitem.get('keys')
            if keys:
                answer = answer.format(**reduce_keys(keys))
            yield from asyncio.sleep(0.5)
            yield from client.send_message(message.channel, answer)


@client.event
@asyncio.coroutine
def on_member_update(before, after):
    # Get online
    if before.status == discord.Status("offline") and after.status != discord.Status("offline"):
        on_presence = LINES.get('on_presence_update')
        if on_presence:
            name = id2user(CONFIG.get('USERS'), before.id)
            reactions = on_presence.get(name)['messages']
            for react in reactions:
                channels = react.get('channels')
                keys = react.get('keys')
                channels = [channels] if not isinstance(channels, (list, tuple)) else channels
                answer = randomize(react.get('answers'))
                if keys:
                    answer = answer.format(**reduce_keys(keys))
                for chan in channels:
                    channel = CONFIG.get('CHANNELS').get(chan)
                    if channel:
                        yield from client.send_message(find_channel(client.server, channel), answer)


def main():
    client.run('NDAxMzg0Mjc4NDg0NzEzNDcz.DTpbpw.8sfhalMvCFPFgnKVrmTC08GhvlA')


if __name__ == '__main__':
    main()
