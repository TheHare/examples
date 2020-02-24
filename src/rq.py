import requests
import os
import logging
import json

level = {
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG
}.get(os.environ.get('LOG_LEVEL', 'INFO'))

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - sample_lib[%(process)s]: %(message)s',
    level=level,
    filename="./log.log"
)

def get_url_kwargs(**kwargs):
    try:
        r = requests.get(**kwargs)
        return r
    except Exception as e:
        return e

def get_url_args(*args):
    try:
        r = requests.get(*args)
        return r
    except Exception as e:
        return e

def put_url_args(*args):
    try:
        r = requests.put(*args)
        return r
    except Exception as e:
        return e

def put_url_kwargs(**kwargs):
    try:
        r = requests.put(**kwargs)
        return r
    except Exception as e:
        return e