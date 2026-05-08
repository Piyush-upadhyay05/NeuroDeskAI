import json
import hashlib

FILE = "Data/security.json"


def load_data():
    with open(FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


def hash_password(password):
    return hashlib.sha256(
        password.encode()
    ).hexdigest()


def set_password(password):
    data = load_data()
    data["password"] = hash_password(password)
    save_data(data)


def verify_password(password):
    data = load_data()
    return data["password"] == hash_password(password)