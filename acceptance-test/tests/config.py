from os.path import join, dirname

import yaml

BASE_DIR = dirname(__file__)

with open(join(dirname(__file__), '../conf/app.yml'), 'r') as f:
	Conf = yaml.safe_load(f)

def get_site_url() -> str:
	return Conf['app']['site']
