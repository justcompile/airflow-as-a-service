from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def load_yaml(file_path=None, data=None):
    assert file_path is not None or data is not None, "You must specify either a file_path or data parameter"
    if data:
        return load(data, Loader=Loader)

    with open(file_path) as fp:
        return load(fp, Loader=Loader)
