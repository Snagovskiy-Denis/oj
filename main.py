from pathlib import Path

from configurator import Configurator


class Application:
    DEFAULT = 'DEFAULT'

    def __init__(self):
        self.path = Path().absolute()

    def get_mode(self):
        return self.DEFAULT

    def read_config_file(self):
        return Configurator().read_config()

