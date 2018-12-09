import discord
import asyncio
import yaml


from pathlib import Path
from animebot.tools import randomize, check_condition, reduce_keys, id2user, find_channel
from animebot.chess.main import ChessGame
from animebot.client import AnimeClient
from animebot.japanese.main import HiraganaQ

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

@asyncio.coroutine
def _mplayer_teardown():
    print('teardown')
    mqueue = client.music_queue
    if mqueue:
        yield from _play_music(mqueue.pop(0))
    else:
        client.mplayer = None


@asyncio.coroutine
def _play_music(url, channel=None):
    if url.startswith('https://www.youtube.com/watch?v='):
        if not client.is_voice_connected(client.server) and channel:
            voice = yield from client.join_voice_channel(channel)
        else:
            voice = client.voice_client_in(client.server)
        if client.mplayer is None:
            client.mplayer = yield from voice.create_ytdl_player(url)
            client.mplayer.start()
        else:
            client.music_queue.append(url)


@asyncio.coroutine
def handle_music(message):
    cnt = message.content
    user_channel = message.author.voice.voice_channel
    try:
        if cnt.startswith('!join'):
            yield from client.join_voice_channel(user_channel)
        elif cnt.startswith('!play'):
            contents = cnt.split(' ')
            if len(contents) != 2:
                raise IndexError('Wrong command')
            _, url = contents
            yield from _play_music(url, user_channel)
        elif cnt.startswith('!pause') and client.mplayer:
            yield from client.mplayer.pause()
        elif cnt.startswith('!resume') and client.mplayer:
            yield from client.mplayer.resume()
        elif cnt.startswith('!stop') and client.mplayer:
            yield from client.mplayer.stop()
            #_mplayer_teardown()
        elif cnt == '!queue' and client.mplayer:
            yield from client.send_message(message.channel, "Youtube links:\n"+'\n'.join(client.music_queue))
        elif cnt.startswith('!leave') and client.is_voice_connected(client.server):
            voice = client.voice_client_in(client.server)
            yield from voice.disconnect()
    except Exception as E:
        yield from client.send_message(message.channel, "Error: {}".format(E))


@client.event
@asyncio.coroutine
def on_message(message):
    cnt = message.content
    if message.author == client.user:  # FIXME
        return
    if message.channel.name == CONFIG.get('CHANNELS')['music']:
        yield from handle_music(message)
    if message.channel.name == CONFIG.get('CHANNELS')['jap']:
        if cnt.startswith('!hiragana'):
            client.quiz = HiraganaQ()
            new_s = client.quiz.get_new()[0]
            yield from client.send_message(message.channel, " -  {}  - ".format(new_s))
        elif cnt.startswith('!stop'):
            client.quiz = None
            yield from client.send_message(message.channel, "Quiz stopped")
        elif client.quiz is not None:
            answer = client.quiz.check_lat(cnt)
            new_s, end = client.quiz.get_new()
            mess = "Right\n\n -  {}  -".format(new_s) if answer == 0 \
                else "Wrong. It is '{}'\n\n -  {}  -".format(answer, new_s)
            yield from client.send_message(message.channel, mess)
            if end == 0:
                client.quiz = None
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
    try:
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
    except Exception as E:
        print('Error on_member_update, {}'.format(E))


def main():
    client.run('NDAxMzg0Mjc4NDg0NzEzNDcz.DTpbpw.8sfhalMvCFPFgnKVrmTC08GhvlA')


if __name__ == '__main__':
    main()
