import hashlib
import json


def hash_sum(obj):
    dhash = hashlib.md5()
    encoded = json.dumps(obj, sort_keys=True).encode()
    dhash.update(encoded)
    return dhash.hexdigest()
