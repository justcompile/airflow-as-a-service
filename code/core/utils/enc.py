from base64 import b64encode
from cryptography.fernet import Fernet, MultiFernet

from django.utils.functional import cached_property

from .files import load_yaml


class EncManager(object):
    def __init__(self):
        self._fernet = None
        self._keys = None

    @cached_property
    def fernet(self):
        if not self._fernet:
            self._fernet = MultiFernet([Fernet(key) for key in self.keys])

        return self._fernet

    @cached_property
    def keys(self):
        if not self._keys:
            self._keys = load_yaml(file_path=False)['field_enc_keys']

        return self._keys

    def decrypt(self, token):
        if not isinstance(token, bytes):
            token = token.encode()

        return self.fernet.decrypt(token)

    def encrypt(self, value):
        if not isinstance(value, bytes):
            value = value.encode()

        return self.fernet.encrypt(value)


def b64encode_str(value):
    return b64encode(value.encode()).decode()
