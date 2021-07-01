import argparse


class ParseDict(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        def clear_str(string: str) -> str:
            '''Remove all invalid symbols, lead and end spaces from string'''
            black_list = '\'\"'
            clean_string = ''.join(c for c in string if c not in black_list)
            return clean_string.strip()

        d = getattr(namespace, self.dest) or {}

        if values:
            for item in values:
                split_items = item.split('=', 1)
                if len(split_items) <= 1 or '' in split_items:
                    message = '\nOPTION or VALUE is being missing \n' \
                             f'oj --option {values} >> {split_items}'
                    parser.exit(status=2, message=message)
                key    = clear_str(split_items[0])
                value  = [clear_str(value) for value in split_items[1:]]
                d[key] = ' '.join(value)

        setattr(namespace, self.dest, d)


class Parser(argparse.ArgumentParser):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.add_arguments()

    def exit(self, status=0, message=None):
        if status:
            raise Exception(f'Exiting because of an error: {message}')
        exit(status)

    def parse_args(self, arg_list: list[str]):
        return super().parse_args(arg_list)

    def add_arguments(self):
        # TODO Plan:
        #   * config  = create config file with defaults or open if exist
        #   * rewrite = delete old file 
        #   * append  = if file already exists (e.g. reminder) append to in
        #   * options = print all options and exit
        #   * date    = set today's date to given one
        #               by default parsed in format of date_format option
        self.add_argument('--skip', 
                action='store_true',
                help='skip default options warning message')

        self.add_argument('-o', '--option', 
                metavar='OPTION=VALUE', action=ParseDict, nargs='+', 
                help='Overwrite OPTION value to VALUE for this run. '
                'Multiple option-value pairs might be passed. '
                'Use space as separator beetween option-value pais. ')
        
        self.add_argument('-c', '--config',
                action='store_true',
                help='open config file or create one if it does not exist yet')
