"""Module config providing paths, logging and config."""

import logging
from pathlib import Path
from dotenv import dotenv_values

PROJ_ROOT = Path(__file__).parent.parent

logging.basicConfig(filename=PROJ_ROOT / 'logs/main_app.log', level=logging.ERROR, filemode='a',
                    format=u'%(asctime)s #%(levelname)s (%(filename)s:%(lineno)d):\n%(message)s\n', datefmt="%H:%M %d.%m.%Y")

logger = logging.getLogger('app_logger')
logger.setLevel(level=logging.INFO)

fh = logging.StreamHandler()
fh = logging.FileHandler(PROJ_ROOT / 'logs/app.log', 'a')
fh_formatter = logging.Formatter(
    u'%(asctime)s #%(levelname)s (%(filename)s:%(lineno)d):\n%(message)s\n',  "%H:%M %d.%m.%Y")

fh.setFormatter(fh_formatter)
logger.addHandler(fh)

config = dotenv_values(PROJ_ROOT.parent / ".env")
