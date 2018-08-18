# flake8: noqa
from .settings import *
import os


INSTALLED_APPS.append('django_nose')

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_COVERAGE_ARGS = [
    '--with-coverage',
    '--cover-branches',
    '--cover-erase',
    '--cover-min-percentage=90',
    '--cover-config-file=../.coveragerc',
    f'--cover-package={",".join([p for p in os.listdir(".") if os.path.isdir(p) and p in INSTALLED_APPS])}',
]

NOSE_ARGS = [
    '-s',
    '--nologcapture',
]

if 'NOCOVER' not in os.environ:
    NOSE_ARGS.extend(NOSE_COVERAGE_ARGS)

try:
    DATABASES['default']['NAME'] = os.environ.get('PGDBNAME', 'test')
    DATABASES['default']['USER'] = os.environ['PGUSER']
    DATABASES['default']['PASSWORD'] = os.environ['PGPASSWORD']
except KeyError:
    pass
