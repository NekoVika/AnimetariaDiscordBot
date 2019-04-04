__version__ = '0.1'
import argparse
from animebot.client import AnimeClient

def main():
    parser = argparse.ArgumentParser(description='Run animetardia bot')
    parser.add_argument('--config-path', metavar='path', type=str, dest='config_path',
                        help='relative path to config file', default=None)

    args = parser.parse_args()
    current_client = create_client(args)
    current_client.run('NDAxMzg0Mjc4NDg0NzEzNDcz.DTpbpw.8sfhalMvCFPFgnKVrmTC08GhvlA')


def create_client(args):
    client = AnimeClient(config_path=args.config_path)
    return client


if __name__ == '__main__':
    main()
