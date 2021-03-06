import discord
import asyncio
import yaml
import traceback
import logging

from pathlib import Path
from animebot.tools import randomize, check_condition, reduce_keys, id2user, find_channel
from animebot.chess.main import ChessGame
from animebot.client import AnimeClient
from animebot.japanese.main import HiraganaQ

logger = logging.getLogger(__name__)


PWD = Path(__file__).parent
ETC_PATH = PWD / 'etc'
LINES = yaml.safe_load((ETC_PATH / 'lines.yaml').open(mode='r', encoding='utf-8'))
CONFIG = yaml.safe_load((ETC_PATH / 'config.yaml').open(mode='r', encoding='utf-8'))

client = AnimeClient(config=CONFIG)


@client.event
@asyncio.coroutine
def on_ready():
    logger.info('Logged in as {}'.format(client.user.name))
    client.server = client.get_server(CONFIG.get('GUILD_ID'))
    yield from client.change_presence(game=discord.Game(name=CONFIG.get('DEFAULT_GAME')))


@asyncio.coroutine
def _mplayer_teardown():
    logger.debug('teardown')
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
        yield from client.music_player.handle(cnt, user_channel)
    except Exception as E:
        logger.error('Error in music handling: {}'.format(E))
        traceback.print_exc()
        # yield from client.send_message(message.channel, "Error: {}".format(E))


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
                if not name:
                    return
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
        logger.error('Error on_member_update: {}'.format(E))
        traceback.print_exc()


def main():
    client.run('NDAxMzg0Mjc4NDg0NzEzNDcz.DTpbpw.8sfhalMvCFPFgnKVrmTC08GhvlA')


if __name__ == '__main__':
    main()
