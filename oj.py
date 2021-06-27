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

    def __init__(self):
        self.configurator = Configurator()
        self.destination: Path = None
        self.template: str = ''
        self.mode = DEFAULT_MODE

    def get_mode(self) -> str:
        # Plan:
        #   * rewrite = delete old file 
        #   * append  = if file already exists (e.g. reminder) append to in
        #   * option  = set option for this run
        #               e.g. 1 template path to run without config file at all
        #               e.g. 2 config path instead of standart one
        #   * 
        return self.mode

    def read_config_file(self):
        self.configurator.read()

    def build_filename(self):
        today = date.today()
        date_format = self.configurator.get('FILENAME', DATE_FORMAT)
        extension = self.configurator.get('FILENAME', EXTENSION)
        filename = today.strftime(date_format) + extension
        destination = self.configurator.getpath(DESTINATION)

        self.destination = destination.joinpath(filename)

    def read_template_file(self):
        self.template = self.configurator.getpath(TEMPLATE).read_text()

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
