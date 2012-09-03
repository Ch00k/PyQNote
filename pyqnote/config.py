import os
from ConfigParser import ConfigParser


# For now it's in .config root.
# Perhaps consider it to be in it's own directory in future
CONFIG_FILE = os.path.expanduser('~/.config/pyqnote.conf')
DEFAULTS = {'general': {'program_dir': os.path.expanduser('~/PyQNote'),
                        'global_hotkey': '<Alt>B',
                        'save_on_enter': 'yes'}}


class Config(object):
    def __init__(self):
        self.config = ConfigParser()

    def read_config(self):
        if self.config.read(CONFIG_FILE):
            config_dict = self.config.__dict__['_sections'].copy()
            for section in config_dict:
                config_dict[section].pop('__name__', None)
        else:
            config_dict = DEFAULTS.copy()
            self.write_config(config_dict)

        return config_dict

    def write_config(self, config_dict):
        for section, config in config_dict.iteritems():
            self.config.add_section(section)
            for key, value in config_dict[section].iteritems():
                self.config.set(section, key, value)
        with open(CONFIG_FILE, 'w+') as config_file:
            self.config.write(config_file)