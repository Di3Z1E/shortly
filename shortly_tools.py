import json
import os
import random
import string
import requests

USERS_URL_JSON = "users_urls.json"

# <-- Validate URL Function --> #


def validate_url(user_url):
    """
    Getting the user actual input and checking if it's a valid URL
    :param user_url:
    :return:
    """
    if "http" not in user_url or "https" not in user_url:
        user_url = 'https://' + user_url
        print('Missing protocol at the beginning of the URL')
    try:
        results = requests.get(user_url)
        if results.status_code == 200:
            print("Valid URL")
            return "True", user_url
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        print("Invalid url")
        return "False", "False"


# <-- Generate Short URL Function --> #

def generate_short_url():
    """
    Generates 5 random characters including digits
    :return:
    """
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(4))

    return f"https://www.shortly.io/{random_string}"


# <-- Add Key & Value To JSON file Function --> #

def add_key_value_to_json(key, value):
    """
    Appending into the JSON file the Source URL (user input) and the Shorten URL.
    :param key:
    :param value:
    :return:
    """
    check_json_existence()

    with open(USERS_URL_JSON, 'r') as json_file:
        try:
            data = json.load(json_file)
        except json.decoder.JSONDecodeError:
            print("Seems like the JSON file is empty, continue without reading.")

    try:
        data[key] = value
    except UnboundLocalError:
        data = {key: value}

    with open(USERS_URL_JSON, 'w') as json_file:
        json.dump(data, json_file, indent=4)


# <-- Check Duplicated Key (User URL to JSON Source URL) Function --> #

def check_dups(file, url):
    """
    Checking the JSON file and making sure there are not duplicated Source URL.
    :param file:
    :param url:
    :return:
    """
    check_json_existence()

    try:
        with open(file, "r") as f:
            content = json.load(f)
        if len(content) == 0:
            print("File found without any data inside")
            return True

        for item in content:
            if item == url:
                print('Found duplicated URL')
                return False

        print('No duplicated URL')
        return True
    except json.decoder.JSONDecodeError:
        print("JSON File not exists")
        return True


# <-- Check The Existence of the JSON File Function --> #

def check_json_existence():
    """
    Checks if the JSON file is existing, and if not creating it.
    :return:
    """
    if os.path.isfile(USERS_URL_JSON):
        print("File exists")
    else:
        print("Creating File")
        with open(USERS_URL_JSON, "w"):
            print("created users_urls.json file")
            pass

