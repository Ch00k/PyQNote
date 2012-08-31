import base64
import os


HOST_DB = '~/.dropbox/host.db'


class DropboxActor(object):
    @classmethod
    def is_installed(cls):
        try:
            with open(os.path.expanduser(HOST_DB)):
                return True
        except IOError:
            return False

    @classmethod
    def get_path(cls):
        if cls.is_installed():
            with open(os.path.expanduser(HOST_DB)) as f:
                content = f.readlines()
            b64_path = content[1]
            path = base64.b64decode(b64_path)

            return path
        else:
            raise IOError('Dropbox is not installed')



