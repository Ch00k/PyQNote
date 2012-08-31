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
        config_dict = self.config.__dict__['_sections'].copy()
        for section in config_dict:
            config_dict[section].pop('__name__', None)
        print config_dict

        return config_dict

    def write_config(self, **kwargs):
        self.config.add_section('dropbox')
        self.config.set('dropbox', 'use', kwargs['use_dropbox'])
        if kwargs['use_dropbox']:
            self.config.set('dropbox', 'path', kwargs['dropbox_path'])
        with open(CONFIG_FILE, 'w+') as config_file:
            self.config.write(config_file)

