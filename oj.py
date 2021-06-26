#!/usr/bin/env python3
from os import getenv, chdir
from pathlib import Path
from datetime import date
import subprocess

from constants import (DEFAULT_MODE, REWRITE_MODE, EDITOR,
                       EXTENSION, DESTINATION, DATE_FORMAT, TEMPLATE,
                      )

from configurator import Configurator


class Application:
    '''Controls scripts commands flow'''

    DEFAULT_MODE = DEFAULT_MODE
    REWRITE_MODE = REWRITE_MODE

    def __init__(self):
        self.configurations = dict()
        self.destination: Path = None
        self.template = ''
        self.mode = self.DEFAULT_MODE

    def get_mode(self) -> str:
        return self.mode

    def read_config_file(self):
        self.configurations = Configurator().read_config()

    def build_filename(self):
        self.read_config_file()

        today = date.today()
        date_format = self.configurations[DATE_FORMAT]
        extension = self.configurations[EXTENSION]

        filename = today.strftime(date_format) + extension
        self.destination = self.configurations[DESTINATION].joinpath(filename)

    def read_template_file(self):
        self.read_config_file()

        self.template = self.configurations[TEMPLATE].read_text()

    def create_note(self):
        if self.get_mode() == self.REWRITE_MODE \
                            or not self.destination.exists():
            self.destination.write_text(self.template)

    def open_note(self):
        editor = getenv(EDITOR)
        if not editor:
            raise AttributeError('EDITOR environment variable is unset')
        chdir(self.destination.parent)
        subprocess.run([editor, self.destination])

    def run(self):
        # TODO import argparse
        # create default config file (from Configurator.__doc__) if sys args
        self.read_config_file()
        self.build_filename()
        self.read_template_file()
        self.create_note()
        self.open_note()


if __name__ == '__main__':
    Application().run()
