from io import StringIO
from paramiko import RSAKey


def generate_keys():
    private_key = RSAKey.generate(bits=4096)
    key_stream = StringIO()
    private_key.write_private_key(key_stream)
    key_stream.seek(0)

    public_key = RSAKey(file_obj=key_stream)
    key_stream.seek(0)

    return key_stream.read(), f'{public_key.get_name()} {public_key.get_base64()} git@airflow-aas'
