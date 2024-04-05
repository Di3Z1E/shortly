from nicegui import ui
import pyperclip
import requests
import os.path
import random
import string
import json

users_url_json = "users_urls.json"


class ShortlyWebsite:
    def __init__(self):
        self.ui = ui

    def create_website(self):
        def submit_callback():
            url = user_input.value
            status, user_url = validate_url(url)
            check_duplicated_results = check_dups(users_url_json, user_url)

            if status == "True" and check_duplicated_results:
                ui.notify('Valid URL!')
                short_url = generate_short_url()
                add_key_value_to_json(user_url, short_url)
                with self.ui.row():
                    self.ui.button("Copy Short URL", on_click=lambda: pyperclip.copy(f'{short_url}'))
            else:
                if not check_duplicated_results:
                    ui.notify('ERROR: URL already in database.')
                elif status == "False":
                    ui.notify('ERROR: Invalid URL!')

        self.ui.markdown('# Welcome to Shortly!')
        self.ui.markdown('## An easy & secure way to shorten your URLs!')

        self.ui.page_title("Shortly by Di3Z1E")

        with self.ui.row():
            user_input = self.ui.input(label='URL').props('square outlined dense').classes('shadow-lg')
            self.ui.button('Submit').on('click', submit_callback)

        with self.ui.header(elevated=True).style('background-color: rgb(71, 71, 71)').classes(
                'items-center justify-between'):
            self.ui.label('Shortly!').classes('text-black-600 text-2xl')

        with self.ui.footer().style('background-color: rgb(71, 71, 71)'):
            self.ui.label('Di3Z1E')

    def run_website(self):
        self.ui.run()


def validate_url(user_url):
    if "http" not in user_url or "https" not in user_url:
        user_url = 'https://' + user_url
    try:
        results = requests.get(user_url)
        if results.status_code == 200:
            print("Valid URL")
            return "True", user_url
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        print("Invalid url")
        return "False", "False"


def generate_short_url():
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(8))

    return f"shortly.io/{random_string}"


def add_key_value_to_json(key, value):
    if os.path.isfile(users_url_json):
        print("File exists")
    else:
        print("Creating File")
        with open(users_url_json, "w") as file:
            pass

    with open(users_url_json, 'r') as json_file:
        try:
            data = json.load(json_file)
        except json.decoder.JSONDecodeError:
            print("Seems like the JSON file is empty, continue without reading.")

    try:
        data[key] = value
    except UnboundLocalError:
        data = {key: value}

    with open(users_url_json, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def check_dups(file, url):
    with open(file, "r") as f:
        content = json.load(f)

    for item in content:
        if item == url:
            return False
        else:
            return True


if __name__ in {"__main__", "__mp_main__"}:
    shortly = ShortlyWebsite()
    shortly.create_website()
    shortly.run_website()
