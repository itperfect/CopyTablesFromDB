import os
import configparser
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class ConfigData:

    def __init__(self, connection_name=None):
        self.CONFIG = configparser.ConfigParser(allow_no_value=True)
        self.CONNECTION_NAME = connection_name

    def _create_default_config(self):
        config = self.CONFIG
        config.add_section("SETTINGS")
        config.set("SETTINGS", "reports_read_from", "0")
        config.set("SETTINGS", "sites_read_from", "0")

        self.CONFIG = config
        return self.CONFIG

    def _write_config(self):
        with open(f"{BASE_DIR}/{self.CONNECTION_NAME}/work.cnf", "w") as config_file:
            self.CONFIG.write(config_file)

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
        print(f'Creating directory for config file')
        os.mkdir(f"{BASE_DIR}/{self.CONNECTION_NAME}")

    def _create_file(self):
        with open(f"{BASE_DIR}/{self.CONNECTION_NAME}/work.cnf", "w") as config_file:
            print(f'Creating config file in directory')
            self.CONFIG = self._create_default_config()
            self.CONFIG.write(config_file)

    def check_config_file_exists(self):
        print(f'Checking config file for database')
        if self._check_dir() is False:
            self._create_dir()
        else:
            print(f'Directory for database exists')

        if self._check_file() is False:
            self._create_file()
        else:
            print(f'Config file exists in directory')

    def get_report_position(self):
        self.CONFIG.read(f"{BASE_DIR}/{self.CONNECTION_NAME}/work.cnf")
        return self.CONFIG.getint("SETTINGS", 'reports_read_from')

    def _set_value(self, name=None, value=None):
        self.CONFIG.set("SETTINGS", name, value)
        return None

    def set_report_position(self, name='reports_read_from', val=None):
        if val is None:
            return None
        self._set_value(name=name, value=str(val))
        self._write_config()
        # with open(f"{BASE_DIR}/{self.CONNECTION_NAME}/work.cnf", "w") as config_file:
        #     self.CONFIG.write(config_file)

    def get_sites_position(self):
        self.CONFIG.read(f"{BASE_DIR}/{self.CONNECTION_NAME}/work.cnf")
        return self.CONFIG.getint('SETTINGS', 'sites_read_from')

    def set_sites_position(self, name='sites_read_from', val=None):
        if val is None:
            return None
        self._set_value(name=name, value=str(val))
        self._write_config()

