#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""

Multi Tab Opener : Open in the default browser a new tab for each entries

Usage:
    mto open | o <keyword_list> [<delimiter>] [<search_engine>]
    mto list | l
    mto -h | --help
    mto --version

Options:
    -h --help           Show this screen
    --version           Show version
    [keyword_list]      List of keywords to search, see [delimiter]
    [search_engine]     Use this engine to make the search try 'google',
                        default 'qwant'
    [delimiter]             Specify the delimiter between each search,
                            default = '\\n'
"""

__author__ = "Pierre Fitoussi"
__version__ = "0.1.0"
__license__ = "MIT"

import webbrowser
import urllib.parse
from docopt import docopt
from functools import reduce

arguments = None
urlBySearchEngine = {
    'google': 'https://www.google.com/search?q=',
    'qwant': 'https://www.qwant.com/?q=',
    'bing': 'https://www.bing.com/search?q='
}

# User settings
defaultEngine = 'google'


def main():
    global arguments

    # Parse argument
    arguments = docopt(__doc__, version=__version__)

    # Show available search engine
    if arguments['l'] or arguments['list']:
        print('Available search engines:')
        list(map(print, urlBySearchEngine.keys()))

    # Open tab(s)
    if arguments['o'] or arguments['open']:
        searchEngine = defaultEngine
        usrSearchEngine = arguments['<search_engine>']

        if usrSearchEngine is not None:
            if usrSearchEngine in urlBySearchEngine:
                searchEngine = usrSearchEngine
            else:
                print(
                    f'{usrSearchEngine} not exists, \
                        Use "mto list" to see available search engine')

        usrDelimiter = arguments['<delimiter>']
        delimiter = usrDelimiter if usrDelimiter is not None else '\n'

        print(f'Searching with {searchEngine}...')

        keywordList = arguments['<keyword_list>']
        list(map(compose(
            urllib.parse.quote,
            lambda x: f'{urlBySearchEngine[searchEngine]}{x}',
            webbrowser.open_new_tab),
            filter(
                lambda x: not not x.strip(),
                map(lambda x: x.strip(),
                    keywordList.split(delimiter)))))


def compose(*func):
    return reduce(lambda f, g: lambda x: g(f(x)), func, lambda x: x)


if __name__ == '__main__':
    main()
