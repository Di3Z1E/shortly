import json

from nicegui import ui
import requests
import random
import string


class ShortlyWebsite:
    def __init__(self):
        self.ui = ui

    def create_website(self):
        def submit_callback():
            url = user_input.value
            status, user_url = validate_url(url)

            if status == "True":
                ui.notify('Valid URL!')
                short_url = generate_short_url()
                add_key_value_to_json(user_url, short_url)
            else:
                ui.notify('ERROR: Invalid URL!')

        self.ui.markdown('# Welcome to Shortly!')
        self.ui.markdown('## An easy & secure way to shorten your URLs!')

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
    filename = "users_urls.json"
    with open(filename, 'r') as json_file:
        try:
            data = json.load(json_file)
        except json.decoder.JSONDecodeError:
            print("Seems like the JSON file is empty, continue without reading.")

    try:
        data[key] = value
    except UnboundLocalError:
        data = {key: value}

    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)


if __name__ in {"__main__", "__mp_main__"}:
    shortly = ShortlyWebsite()
    shortly.create_website()
    shortly.run_website()
