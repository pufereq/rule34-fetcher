#!/usr/bin/env python3
"""
Fetches image count from the 'rule34.xxx' site.

Pings https://rule34.xxx for searched keyword and returns the image count
without having to use eyebleach.

Probably works also with Gelbooru, as rule34.xxx uses their search engine.
"""

from clear import clear

import requests
import json


def show_data(processed_data, count):
    """Display data.

    If keyword is empty, display 'Most Popular'
    Displays data in an ordered list (index. 'keyword' - count)

    Args:
        processed_data (list): Data ready for displaying
        count (int): Post count from rule34.xxx
    """
    clear()
    if keyword == '':
        print(f'Searched for Most Popular posts.')
    else:
        print(f'Searched for \'{keyword}\'.')
    print(f'Found {count} results.')
    for index in range(count):
        print(f'{index + 1}. \'{processed_data[index][0]}\' - {processed_data[index][1]} posts')


def process_data(parsed_data):
    """Get data ready for displaying.

    rule34.xxx displays post count in brackets, this function gets rid
    of them and splits strings into double lists.

    Args:
        parsed_data (list): Parsed data from parse_data()
    """
    processed_data = []
    count = 0
    for object in parsed_data:
        count += 1
        processed_data.append(object['label'].replace('(', '').replace(')', '').split())
    # print(processed_data, count)
    show_data(processed_data, count)


def parse_data(fetched_data):
    """Convert json data to python lists.

    Args:
        fetched_data (str): Data fetched from rule34.xxx
    """
    print('Parsing data...', end=' ')
    parsed_data = json.loads(fetched_data)
    # print(parsed_data)
    print('Done.')
    process_data(parsed_data)


def fetch_data_from_site(keyword):
    """Use requests to fetch results using keyword.

    Args:
        keyword (str): Keyword to search for in rule34.xxx
    """
    print('Connecting...', end=' ')
    try:
        fetched_data = requests.get(f'https://rule34.xxx/public/autocomplete.php?q={keyword}')
    except requests.exceptions.ConnectionError as exception:
        print(f'Error.\n\nDetails:\n{exception}')
        exit()
    print('Done.')
    parse_data(fetched_data.text)


def get_keyword():
    """Get input from user and assings it to keyword."""
    global keyword
    print('Leave blank for most popular.')
    keyword = input('Input keyword (separated by spaces or underscores): ')
    keyword = keyword.replace(' ', '_')
    fetch_data_from_site(keyword)


get_keyword()
