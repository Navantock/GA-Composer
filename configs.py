import argparse


def parse_command_args():
    parser = argparse.ArgumentParser(description='GAComposer Parameters')
    parser.add_argument('-c', '--config_file', type=str, help='The path of the config file.')
    args = parser.parse_args()
    return args