import datetime
from pathlib import Path

from constants import (DEFAULT_MODE, REWRITE_MODE,
                       EXTENSION, DESTINATION, DATE_FORMAT, TEMPLATE,
                      )

from configurator import Configurator


class Application:
    DEFAULT_MODE = DEFAULT_MODE
    REWRITE_MODE = REWRITE_MODE

    def __init__(self):
        self.configurations = dict()
        self.destination:Path = None
        self.template = ''
        self.mode = self.DEFAULT_MODE

    def get_mode(self) -> str:
        return self.mode

    def read_config_file(self):
        self.configurations = Configurator().read_config()

    def build_filename(self):
        self.read_config_file()

        today = datetime.date.today()
        date_format = self.configurations[DATE_FORMAT]
        extension = self.configurations[EXTENSION]
        filename = f'{today.strftime(date_format)}{extension}'
        
        self.destination = self.configurations[DESTINATION].joinpath(filename)

    def read_template_file(self):
        self.read_config_file()

        self.template = self.configurations[TEMPLATE].read_text()

    def create_note(self):
        if self.get_mode() == self.REWRITE_MODE \
                            or not self.destination.exists():
            self.destination.write_text(self.template)
