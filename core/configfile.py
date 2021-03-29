import os
import configparser
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class ConfigData:

    def __init__(self, connection_name=None):
        self.CONFIG = configparser.ConfigParser()
        self.CONNECTION_NAME = connection_name

    def _create_default_config(self):
        config = self.CONFIG
        config.add_section("SETTINGS")
        config.set("SETTINGS", "read_from", "0")
        self.CONFIG = config
        return self.CONFIG

    def _check_dir(self):
        if os.path.isdir(f"{BASE_DIR}/{self.CONNECTION_NAME}"):
            return True
        else:
            return False

    def _check_file(self):
        if os.path.isfile(f"{BASE_DIR}/{self.CONNECTION_NAME}/work.cnf"):
            return True
        return False

    def _create_dir(self):
        os.mkdir(f"{BASE_DIR}/{self.CONNECTION_NAME}")

    def _create_file(self):
        with open(f"{BASE_DIR}/{self.CONNECTION_NAME}/work.cnf", "w") as config_file:
            self.CONFIG = self._create_default_config()
            self.CONFIG.write(config_file)

    def check_config_file_exists(self):
        if self._check_dir() is False:
            self._create_dir()

        if self._check_file() is False:
            self._create_file()

    def get_last_pos(self):
        self.CONFIG.read(f"{BASE_DIR}/{self.CONNECTION_NAME}/work.cnf")
        return self.CONFIG.getint("SETTINGS", 'read_from')
