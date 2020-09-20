import logging.config
from os.path import join, dirname

import yaml

BASE_DIR = dirname(__file__)

with open(join(dirname(__file__), '../conf/app.yml'), 'r') as f:
    Conf = yaml.safe_load(f)

logging.config.fileConfig(join(BASE_DIR, '../conf/logging.ini'))
