import hashlib
import time


def create_group_id(prefix=''):
    if prefix:
        prefix += '-'

    microseconds = int(time.time() * 100000)
    microseconds = str(microseconds)
    microseconds = microseconds.encode('utf-8')

    digest = hashlib.md5()
    digest.update(microseconds)
    group_id = digest.hexdigest()
    return prefix + group_id.upper()
