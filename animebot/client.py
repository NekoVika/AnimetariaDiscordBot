import discord
import asyncio


class AnimeClient(discord.Client):
    game = None
    quiz = None
    mplayer = None

    def __init__(self, *args, **kwargs):
        self.music_queue = []
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
