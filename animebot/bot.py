import discord
import asyncio
import yaml
import re
import random

from pathlib import Path
from animebot.tools import randomize, check_condition, reduce_keys, id2user, find_channel

client = discord.Client()

PWD = Path('.')
ETC_PATH = PWD / 'etc'
LINES = yaml.safe_load((ETC_PATH / 'lines.yaml').open(mode='r', encoding='utf-8'))
CONFIG = yaml.safe_load((ETC_PATH / 'config.yaml').open(mode='r', encoding='utf-8'))
SERVER = None


@client.event
@asyncio.coroutine
def on_ready():
    global SERVER
    print('Logged in as')
    print(client.user.name)
    SERVER = client.get_server(CONFIG.get('GUILD_ID'))
    yield from client.change_presence(game=discord.Game(name=CONFIG.get('DEFAULT_GAME')))
    print('------')


@client.event
@asyncio.coroutine
def on_message(message):
    if message.author == client.user:  # FIXME
        return
    mlines = LINES.get('on_message', [])
    for mitem in mlines:
        if any(map(lambda x: check_condition(message.content.lower(), x), mitem.get('conditions'))):
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
                        yield from client.send_message(find_channel(SERVER, channel), answer)




    # if message.content.startswith('!test'):
    #     tmp = yield from client.send_message(message.channel, 'wolera')
    #     print('###', tmp)
    #     counter = 0
    #     tmp = yield from client.send_message(message.channel, 'Calculating messages...')
    #     for log in client.logs_from(message.channel, limit=100):
    #         if log.author == message.author:
    #             counter += 1
    #
    #     yield from client.edit_message(tmp, 'You have {} messages.'.format(counter))
    # elif message.content.startswith('!sleep'):
    #     yield from asyncio.sleep(5)
    #     yield from client.send_message(message.channel, 'Done sleeping')


def main():
    client.run('NDAxMzg0Mjc4NDg0NzEzNDcz.DTpbpw.8sfhalMvCFPFgnKVrmTC08GhvlA')


if __name__ == '__main__':
    main()
