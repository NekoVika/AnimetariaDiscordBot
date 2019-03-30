import asyncio
import asgiref

def _teardown():
    print('!!!teadown!!!')


class MusicPlayer:
    mplayer = None
    current_song = None
    commands = ('!join', '!leave', '!add', '!play', '!next', '!pause', '!stop', '!resume')
    voice = None

    def __init__(self, client, *args, **kwargs):
        self.parent = client
        self.current_playlist = []

    def validate(self, message):
        if not any(map(message.startswith, self.commands)):
            return False
        return True

    def validate_url(self, link):
        return True

    def _join_bot(self, channel):
        self.voice = yield from self.parent.join_voice_channel(channel)

    def _leave_bot(self):
        self.voice.disconnect()
        self.voice = None

    @asyncio.coroutine
    def _create_ytpl(self):
        self.mplayer = yield from self.voice.create_ytdl_player(self.current_song)

    @asyncio.coroutine
    def _destroy_ytpl(self):
        self.mplayer = None

    @asyncio.coroutine
    def _start(self):
        self.mplayer.start()

    @asyncio.coroutine
    def _stop(self):
        self.mplayer.stop()

    @asyncio.coroutine
    def _pause(self):
        self.mplayer.pause()

    @asyncio.coroutine
    def _resume(self):
        self.mplayer.resume()

    def add(self, link):
        self.current_playlist.append(link)

    def teardown(self):
        pass
        ## yield from self._next()

    @asyncio.coroutine
    def _next(self):
        print('=== next',)
        if not self.current_playlist:
            return
        self.current_song = self.current_playlist.pop(0)
        if self.mplayer is not None:
            yield from self._stop()
            yield from self._destroy_ytpl()
        yield from self._create_ytpl()
        yield from self._start()

    @asyncio.coroutine
    def handle(self, message, channel):
        if not self.validate(message):
            return
        # TODO: this command not belong to music client
        if message.startswith('!join'):
            yield from self._join_bot(channel)
        # TODO: this command not belong to music client
        elif message.startswith('!leave') and self.parent.is_voice_connected(self.parent.server):
            # voice = self.parent.voice_client_in(self.parent.server)
            yield from self._leave_bot()
        elif message.startswith('!play'):
            url = message.split(' ')[1]
            if not self.validate_url(url):
                return
            if self.current_song is not None:
                self._destroy_ytpl()
            self.current_song = url
            yield from self._create_ytpl()
            yield from self._start()
        elif message.startswith('!add'):
            url = message.split(' ')[1]
            if not self.validate_url(url):
                return
            self.add(url)
        elif message.startswith('!stop'):
            yield from self._stop()
            yield from self._destroy_ytpl()
            self.current_song = None
        elif message.startswith('!pause'):
            yield from self._pause()
        elif message.startswith('!resume'):
            yield from self._resume()
        elif message.startswith('!next'):
            yield from self._next()
        # if message.startswith('!join'):
        #     yield from self.parent.join_voice_channel(channel)
        # elif message.startswith('!play'):
        #     contents = message.split(' ')
        #     if len(contents) != 2:
        #         raise IndexError('Wrong command')
        #     _, url = contents
        #     yield from _play_music(url, user_channel)
        # elif message.startswith('!pause') and client.mplayer:
        #     yield from client.mplayer.pause()
        # elif message.startswith('!resume') and client.mplayer:
        #     yield from client.mplayer.resume()
        # elif message.startswith('!stop') and client.mplayer:
        #     yield from client.mplayer.stop()
        #     #_mplayer_teardown()
        # elif message == '!queue' and client.mplayer:
        #     yield from client.send_message(message.channel, "Youtube links:\n"+'\n'.join(client.music_queue))
        # elif message.startswith('!leave') and client.is_voice_connected(client.server):
        #     voice = client.voice_client_in(client.server)
        #     yield from voice.disconnect()

