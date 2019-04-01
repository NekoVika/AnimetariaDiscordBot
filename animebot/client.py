import discord
import asyncio
from sqlite3 import dbapi2 as sqlite
from sqlalchemy import create_engine

from animebot.voice.main import MusicPlayer

class AnimeClient(discord.Client):
    game = None
    quiz = None
    mplayer = None

    def __init__(self, *args, **kwargs):
        self.config = kwargs.pop("config", {})
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
