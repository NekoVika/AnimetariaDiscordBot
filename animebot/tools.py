import re
import random


def check_condition(m, c):
    rc = re.compile(c)
    return bool(rc.search(m))


def reduce_keys(keys):
    result = {}
    for k, v in keys.items():
        result[k] = randomize(v)
    return result


def randomize(inst):
    return inst if not isinstance(inst, (list, tuple)) else random.choice(inst)


def user2id(obj, user):
    return obj.get(user, None)


def id2user(obj, id_):
    for key, value in obj.items():
        if value == id_:
            return key


# temporary solution
def find_channel(server, name):
    for ch in server.channels:
        if ch.name == name:
            return ch
