from nicegui import ui
from shortly_tools import *
import pyperclip
import time


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
                time.sleep(3)
                with self.ui.row():
                    print('Generating copy button')
                    self.ui.button("Copy Short URL", on_click=lambda: pyperclip.copy(f'{short_url}'))
            else:
                if not check_duplicated_results:
                    ui.notify('ERROR: URL already in database.')
                elif status == "False":
                    ui.notify('ERROR: Invalid URL!')

        self.ui.markdown('# Welcome to Shortly!')
        self.ui.markdown('## An easy & secure way to shorten your URLs!')

        self.ui.page_title("Shortly")

        with self.ui.row():
            user_input = self.ui.input(label='URL').props('square outlined dense').classes('shadow-lg')
            self.ui.button('Submit').on('click', submit_callback)

        with self.ui.header(elevated=True).style('background-color: rgb(71, 71, 71)').classes('items-center justify-between'):
            self.ui.label('Shortly!').classes('text-black-600 text-2xl')

        ui.separator()

        self.ui.markdown('### Latest shorted out URLS')

        with self.ui.footer().style('background-color: rgb(71, 71, 71)'):
            self.ui.label('Shortly by Di3Z1E')
            self.ui.link('Github', 'https://github.com/Di3Z1E').classes('text-black-600')

    def run_website(self):
        self.ui.run()


if __name__ in {"__main__", "__mp_main__"}:
    shortly = ShortlyWebsite()
    shortly.create_website()
    shortly.run_website()
