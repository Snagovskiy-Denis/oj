#!/usr/bin/env python3
from datetime import date
from os import getenv, chdir
from pathlib import Path
import subprocess

from configurator import EXTENSION, DESTINATION, DATE_FORMAT, TEMPLATE
from configurator import Configurator


EDITOR = 'EDITOR'  # environment variable

DEFAULT_MODE = 'default'
REWRITE_MODE = 'rewrite'


class Application:
    '''Controls scripts commands flow'''

    def __init__(self):
        self.configurator = Configurator()
        self.destination: Path = None
        self.template: str = ''
        self.mode = DEFAULT_MODE

    def get_mode(self) -> str:
        # Plan:
        #   * rewrite = delete old file 
        #   * append  = if file already exists (e.g. reminder) append to in
        #   * options = print all options and exit
        #   * option  = set option for this run exclusively
        #               e.g. 1 template path to run without config file at all
        #               e.g. 2 config path instead of standart one
        #   * help    = print help message and exit
        #   * 
        return self.mode

    def read_config_file(self):
        self.configurator.read()

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

    def create_note(self):
        if self.get_mode() == REWRITE_MODE or not self.destination.exists():
            self.destination.write_text(self.template)

    def open_note(self):
        editor = getenv(EDITOR)
        if not editor:
            raise AttributeError('EDITOR environment variable is unset')
        chdir(self.destination.parent)
        subprocess.run([editor, self.destination])

    def run(self):
        # TODO import argparse
        self.read_config_file()
        self.build_filename()
        self.read_template_file()
        self.create_note()
        self.open_note()


if __name__ == '__main__':
    # TODO: default settings + argparse + alter template for holidays = v1.0.0
    Application().run()
