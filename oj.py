#!/usr/bin/env python3
from datetime import date
from os import getenv, chdir
from pathlib import Path
import subprocess
import sys

from configurator import EXTENSION, DESTINATION, DATE_FORMAT, TEMPLATE
from configurator import Configurator
from cli import Parser


EDITOR = 'EDITOR'  # environment variable

DEFAULT_MODE = 'default'
REWRITE_MODE = 'rewrite'


class Application:
    '''Controls scripts commands flow'''

    def __init__(self):
        self.cli = Parser(self, prog='oj',
                description='Daily note manager for Console Dwellers')
        self.configurator = Configurator()
        self.destination: Path = None
        self.template: str = ''
        self.mode = DEFAULT_MODE

    def get_mode(self) -> str:
        return self.mode

    def parse_system_arguments(self):
        self.cli = self.cli.parse_args(sys.argv[1:])

    def read_config_file(self):
        self.configurator.read(
                cli_options=self.cli.option, skip=self.cli.skip)

    def build_filename(self):
        date_format = self.configurator.get_in_filename(DATE_FORMAT)
        extension   = self.configurator.get_in_filename(EXTENSION)
        destination = self.configurator.get_path(DESTINATION)
        filename    = date.today().strftime(date_format) + extension

        self.destination = destination.joinpath(filename)

    def read_template_file(self):
        self.template = ''
        path = self.configurator.get_path(TEMPLATE)
        if path.is_file():
            self.template = path.read_text()

            holiday_on = self.configurator.getboolean('STAFF_ONLY', 
                    'holiday_feature') == True
            holiday_template = self.configurator.get_path('holiday')
            today_is_holiday = date.today().weekday() in (5, 6)
            if holiday_on and holiday_template.is_file() and today_is_holiday:
                self.template += '\n' + holiday_template.read_text()

    def create_file_on_destination(self):
        if self.get_mode() == REWRITE_MODE or not self.destination.exists():
            self.destination.write_text(self.template)

    def open_destination(self):
        editor = getenv(EDITOR)
        if not editor:
            raise AttributeError('EDITOR environment variable is unset')
        chdir(self.destination.parent)
        subprocess.run([editor, self.destination])

    def config_run(self):
        '''Destination is a config, template is the default config text'''
        self.destination = self.configurator._get_config_path(skip=True)

        if self.destination.is_file():
            self.open_destination()
        else:
            message = 'You have not config file.\n\n' \
                      'Do you want to create new one no path: ' \
                     f'{self.destination}'
            with YesNoPrompt(message) as user_is_agree:
                if user_is_agree:
                    self.template = self.configurator.get_default_config()
                    self.create_file_on_destination()
                    self.open_destination()

    def default_run(self):
        '''Destination is a note, template is a template file body'''
        self.read_config_file()
        self.build_filename()
        self.read_template_file()
        self.create_file_on_destination()
        self.open_destination()

    def run(self):
        self.parse_system_arguments()
        if self.cli.config is True:
            self.config_run()
        else:
            self.default_run()


class YesNoPrompt:
    """Returns user's input as users agreement or disagreement with message"""
    def __init__(self, message: str = ''):
        self.message = message or 'Do not type y'

    def __enter__(self) -> bool:
        print(self.message)
        user_input = 'required'
        while user_input not in ('y', 'n'):
            user_input = input('[y/n] > ')
        return user_input == 'y'

    def __exit__(self, exc_type, exc_value, exc_tb): pass


if __name__ == '__main__':
    # TODO REAMDE > usage without config with args
    Application().run()
