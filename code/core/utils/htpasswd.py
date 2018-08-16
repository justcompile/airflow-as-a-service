from base64 import b64encode
from passlib.apache import HtpasswdFile


class HTPasswd(object):
    @classmethod
    def generate(cls, username, password, encode=True):
        ht = HtpasswdFile()
        ht.set_password(username, password)
        value = ht.to_string().strip()
        if encode:
            return b64encode(value).decode()
        return value.decode()
