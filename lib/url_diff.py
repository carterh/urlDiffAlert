#!/usr/bin/env python3

import requests
import difflib

#Takes a url and optional regex.  If the diff of the cached version with the latest version contains regex, return the HTML diff.  Otherwise return None.
def url_diff(url, regex, cache_page, include_diff=False):
    try: 
        loaded_page = requests.get(url, timeout=1).text
        #TO-DO: add regex check to see if the regex exists in the updated page.  If it does, alert.  Else, update cache with no alert.
        if cache_page != loaded_page:
            if include_diff:
                d = difflib.HtmlDiff()
                return d.make_file(cache_page.splitlines(), loaded_page.splitlines()), loaded_page
            else:
                return 'There was an update for: ' + url + ' : ' + regex, loaded_page
        else:
            return None
    except BaseException as e:
        print(str(e))
        return None

def main():
    while True:
        #query url
        url = input('Enter a url. Enter \'quit\' to exit: ')
        if url == 'quit':
            break

        cache_page = requests.get(url, timeout=1).text
        results = url_diff(url, '', cache_page)
        print(results[0])

if __name__ == '__main__':
    main()
