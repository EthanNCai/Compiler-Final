import json
import requests


class TableConstructer:
    def __init__(self, url):
        with open('Back-End/parser/temp/specfamily.json') as file:
            self.specfamily_json = json.load(file)
        print(self.specfamily_json)


def main():
    table_constructer = TableConstructer(
        'Back-End/parser/temp/specfamily.json')


main()
