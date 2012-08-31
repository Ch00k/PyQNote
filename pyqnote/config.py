import os
import ConfigParser


# For now it's in .config root.
# Perhaps consider it to be in it's own directory in future
CONFIG_FILE = os.path.expanduser('~/.config/pyqnote.conf')


class Config(object):
    def __init__(self):
        self.config = ConfigParser.ConfigParser()

    def read_config(self):
        self.config.read(CONFIG_FILE)
        config_dict = dict()
        for section_name in self.config.sections():
            for option in self.config.options(section_name):
                for name, value in self.config.items(section_name):
                    config_dict[section_name] = dict(name = value)
        print config_dict

        return config_dict

    def write_config(self, **kwargs):
        self.config.add_section('dropbox')
        self.config.set('dropbox', 'use', kwargs['use_dropbox'])
        if kwargs['use_dropbox']:
            self.config.set('dropbox', 'path', kwargs['dropbox_path'])
        with open(CONFIG_FILE, 'w+') as config_file:
            self.config.write(config_file)