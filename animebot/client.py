import discord
import asyncio
import yaml
import traceback
import logging

from pathlib import Path
from sqlite3 import dbapi2 as sqlite
from sqlalchemy import create_engine

from animebot.tools import randomize, check_condition, reduce_keys, id2user, find_channel
from animebot.chess.main import ChessGame
from animebot.japanese.main import HiraganaQ
from animebot.voice.main import MusicPlayer

logger = logging.getLogger(__name__)


class AnimeClient(discord.Client):
    game = None
    quiz = None
    mplayer = None
    server = None

    def __init__(self, *args, **kwargs):
        config_path = kwargs.get("config_path")
        pwd = Path(__file__).parent  # FIXME
        if config_path is None:
            config_path = pwd / "etc/config.yaml"
        self.config = yaml.safe_load(config_path.open(mode='r', encoding='utf-8'))
        lines_path = config_path.parent / self.config.get('LINES_PATH', "lines.yaml")
        self.lines = yaml.safe_load(lines_path.open(mode='r', encoding='utf-8'))
        self.music_player = MusicPlayer(self)
        # self.db = create_engine('sqlite+pysqlite:///.animebot.db', module=sqlite)
        super(AnimeClient, self).__init__(*args, **kwargs)

    @asyncio.coroutine
    def render_chess(self, channel, field):
        message = ''
        for x, col in enumerate(field):
            message += '|'
            for y, pos in enumerate(col):
                message += pos
            message += '|\n'
        yield from self.send_message(channel, message)

    @asyncio.coroutine
    def on_ready(self):
        logger.info('Logged in as {}'.format(self.user.name))
        self.server = self.get_server(self.config.get('GUILD_ID'))
        yield from self.change_presence(game=discord.Game(name=self.config.get('DEFAULT_GAME')))

    @asyncio.coroutine
    def _mplayer_teardown(self):
        logger.debug('teardown')
        mqueue = self.music_queue
        if mqueue:
            yield from self._play_music(mqueue.pop(0))
        else:
            self.mplayer = None

    @asyncio.coroutine
    def _play_music(self, url, channel=None):
        if url.startswith('https://www.youtube.com/watch?v='):
            if not self.is_voice_connected(self.server) and channel:
                voice = yield from self.join_voice_channel(channel)
            else:
                voice = self.voice_client_in(self.server)
            if self.mplayer is None:
                self.mplayer = yield from voice.create_ytdl_player(url)
                self.mplayer.start()
            else:
                self.music_queue.append(url)

    @asyncio.coroutine
    def handle_music(self, message):
        cnt = message.content
        user_channel = message.author.voice.voice_channel
        try:
            yield from self.music_player.handle(cnt, user_channel)
        except Exception as E:
            logger.error('Error in music handling: {}'.format(E))
            traceback.print_exc()
            # yield from client.send_message(message.channel, "Error: {}".format(E))

    @asyncio.coroutine
    def on_message(self, message):
        cnt = message.content
        if message.author == self.user:  # FIXME
            return
        if message.channel.name == self.config.get('CHANNELS')['music']:
            yield from self.handle_music(message)
        if message.channel.name == self.config.get('CHANNELS')['jap']:
            if cnt.startswith('!hiragana'):
                self.quiz = HiraganaQ()
                new_s = self.quiz.get_new()[0]
                yield from self.send_message(message.channel, " -  {}  - ".format(new_s))
            elif cnt.startswith('!stop'):
                self.quiz = None
                yield from self.send_message(message.channel, "Quiz stopped")
            elif self.quiz is not None:
                answer = self.quiz.check_lat(cnt)
                new_s, end = self.quiz.get_new()
                mess = "Right\n\n -  {}  -".format(new_s) if answer == 0 \
                    else "Wrong. It is '{}'\n\n -  {}  -".format(answer, new_s)
                yield from self.send_message(message.channel, mess)
                if end == 0:
                    self.quiz = None
        if cnt.startswith('!chess'):
            self.game = ChessGame()
            return
        if isinstance(self.game, ChessGame) and message.content.startswith('!move'):
            move = cnt[6:].split(' ')
            result = self.game.make_move(move)
            if result['code'] == 1:
                yield from self.send_message(message.channel, result['message'])
            else:
                yield from self.render_chess(message.channel, result['message'])
            return
        if cnt.startswith('!gameend'):
            self.game = None
            return
        mlines = self.lines.get('on_message', [])
        for mitem in mlines:
            if any(map(lambda x: check_condition(cnt.lower(), x), mitem.get('conditions'))):
                answer = randomize(mitem.get('answers'))
                keys = mitem.get('keys')
                if keys:
                    answer = answer.format(**reduce_keys(keys))
                yield from asyncio.sleep(0.5)
                yield from self.send_message(message.channel, answer)

    @asyncio.coroutine
    def on_member_update(self, before, after):
        # Get online
        try:
            if before.status == discord.Status("offline") and after.status != discord.Status("offline"):
                on_presence = self.lines.get('on_presence_update')
                if on_presence:
                    name = id2user(self.config.get('USERS'), before.id)
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
                            channel = self.config.get('CHANNELS').get(chan)
                            if channel:
                                yield from self.send_message(find_channel(self.server, channel), answer)
        except Exception as E:
            logger.error('Error on_member_update: {}'.format(E))
            traceback.print_exc()