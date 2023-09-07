# keys_check.py
import os

KEY_PATH = os.environ.get("KEY_PATH", os.path.expanduser("~/crypto_fields"))


def key_check():
    if any(file.endswith(".pem") for file in os.listdir(KEY_PATH)):
        return True
    return False
