# pylint: skip-file
from .settings import *
import os


INSTALLED_APPS.append('django_nose')

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '-s',
    '--nologcapture',
]

try:
    DATABASES['default']['NAME'] = os.environ.get('PGDBNAME', 'test')
    DATABASES['default']['USER'] = os.environ['PGUSER']
    DATABASES['default']['PASSWORD'] = os.environ['PGPASSWORD']
except KeyError:
    pass
