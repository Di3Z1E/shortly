from shortly_tools import *
from nicegui import ui
import pyperclip


USERS_URL_JSON = "users_urls.json"


class ShortlyWebsite:
    def __init__(self):
        self.ui = ui

    def create_website(self):
        def submit_callback():
            url = user_input.value
            status, user_url = validate_url(url)
            check_duplicated_results = check_dups(USERS_URL_JSON, user_url)

            if status == "True" and check_duplicated_results:
                ui.notify('Valid URL!')
                short_url = generate_short_url()
                add_key_value_to_json(user_url, short_url)
                with self.ui.row():
                    print('Generating copy button')
                    add(user_url, short_url)
                    self.ui.button("Copy Short URL", on_click=lambda: pyperclip.copy(f'{short_url}'))
            else:
                if not check_duplicated_results:
                    ui.notify('ERROR: URL already in database.')
                elif status == "False":
                    ui.notify('ERROR: Invalid URL!')

        self.ui.markdown('# Welcome to Shortly!')
        self.ui.markdown('## Amazingly way to generate a short URL!')

        self.ui.page_title("Shortly")

        with self.ui.row():
            user_input = self.ui.input(label='Insert URL Here').props('square outlined dense').classes('shadow-lg')
            user_input.props("size=80")
            self.ui.button('Submit').on('click', submit_callback)

        with self.ui.header(elevated=True).style('background-color: rgb(71, 71, 71)').classes('items-center justify-between'):
            self.ui.label('Shortly!').classes('text-black-600 text-2xl')

        ui.separator()

        self.ui.markdown('### Latest shorted out URLS by users')

        def add(src_url, shorten_url):
            table.add_rows({'id': src_url, 'count': shorten_url})

        columns = [
            {'name': 'id', 'label': 'Source URL', 'field': 'id', 'align': 'middle'},
            {'name': 'count', 'label': 'Shorten URL', 'field': 'count', 'align': 'middle'},
        ]

        table = ui.table(columns=columns, rows=[], row_key='id')

        try:
            with open(USERS_URL_JSON, "r") as file:
                content = json.load(file)

                for name, link in content.items():
                    table.add_rows({'id': name, 'count': link})

        except FileNotFoundError:
            print("No JSON file found")
            content = {}

        with self.ui.footer().style('background-color: rgb(71, 71, 71)'):
            self.ui.label('Shortly by Di3Z1E')
            self.ui.link('Github', 'https://github.com/Di3Z1E').classes('text-black-600')

    def run_website(self):
        self.ui.run()


if __name__ in {"__main__", "__mp_main__"}:
    shortly = ShortlyWebsite()
    shortly.create_website()
    shortly.run_website()
