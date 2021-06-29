import argparse


class Parser(argparse.ArgumentParser):
    def __init__(self, app, **kwargs):
        super().__init__(kwargs)
        self.add_arguments()

    def parse_args(self, arg_list: list[str]):
        return super().parse_args(arg_list)

    def add_arguments(self):
        self.add_argument('--skip', action='store_true',
                help='skip default options warning message')
