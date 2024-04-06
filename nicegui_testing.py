import json
from nicegui import ui

file_path = "users_urls.json"


def display(data):
    try:
        with open(file_path, "r") as file:
            content = json.load(file)
    except FileNotFoundError:
        print("No JSON file found")
        content = {}

    columns = [
        {'name': 'name', 'label': 'Source URL', 'field': 'name', 'align': 'middle'},
        {'name': 'link', 'label': 'Shorten URL', 'field': 'link', 'align': 'middle'},
    ]

    rows = []

    for name, link in content.items():
        rows.append({'name': name, 'link': link})

    table = ui.table(columns=columns, rows=rows, row_key='name')
    table.add_slot('body-cell-link', '''
        <q-td :props="props">
            <a :href="props.value">{{ props.value }}</a>
        </q-td>
    ''')
