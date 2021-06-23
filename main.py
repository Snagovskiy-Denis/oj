from pathlib import Path

from configurator import Configurator


class Application:
    DEFAULT = 'DEFAULT'

    def __init__(self):
        self.path = Path().absolute()
        self.configurations = dict()

    def get_mode(self):
        return self.DEFAULT

    def read_config_file(self):
        self.configurations = Configurator().read_config()

