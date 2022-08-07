import json

BASE_URL = 'https://courses.iiit.ac.in/'
SUBJECTS = {
    'dsa': '3154',
    'dsm': '3013',
    'aad': '3546',
    'at': '3536',
    'osn': '3479',
    'cso': '3149',
    'la': '3200',
    'iot': '3190',
    'iss': '3274',
    'cpro': '3011',
    'ds': '3010',
    'da': '3498',
    'ps': '3497',
    'ra': '3531',
    'iss': '3274',
    've1': '3514',
    'esw': '3566',
    'aad': '3546',
}

COLORS = {
    'red': '\u001b[31m',
    'green': '\u001b[32m',
    'yellow': '\u001b[33m',
    'reset': '\u001b[0m'
}


def get_user():
    return json.load(open('absolute_path_for_user.json'))
