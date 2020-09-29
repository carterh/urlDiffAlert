#!/usr/bin/env python3

from url_diff import url_diff
import json
import pickle
from collections import defaultdict
from time import sleep
from email_alert import send_alert
import logging

#TO-DO: swap print statements over to log messages to a file
class config:
    def __init__(self, rules, recipients, interval):
        self.rules = rules
        self.recipients = recipients
        self.check_interval = interval*60

    @staticmethod
    def load_config(path):
        config_file = open(path)
        config_map = json.load(config_file)
        config_file.close()
        return config(config_map['rules'], config_map['recipients'], config_map['check_interval'])

default_cache = './temp/url_cache.bin'
default_config = './config.json'

class url_cache:
    def __init__(self):
        self.cache = defaultdict(str)

class daemon:
    def __init__(self, config, state):
        self.config = config
        self.state = state

    def start(self):
        print('Starting daemon')
        while True:
            for rule in self.config.rules:
                url = rule['url']
                regex = rule['regex']
                try:
                    result = url_diff(rule['url'], rule['regex'], self.state.cache[(url,regex)], include_diff=True)
                    if result:
                        if result[0]:
                            subject_line = 'Url diff for ' + url + ' : ' + regex
                            print('Emailing: ' + subject_line)
                            send_alert(result[0], self.config.recipients, subject_line)
                        self.state.cache[(url,regex)] = result[1]
                except BaseException as e:
                    print(str(e))
            
            #write the cache, sleep
            print('Writing cache')
            try:
                cache_file = open(default_cache, 'wb')
                pickle.dump(self.state,cache_file)
                cache_file.close()
            except BaseException as e:
                print(str(e))
            sleep(self.config.check_interval)

def main():
    conf = config.load_config(default_config) 

    try:
        cache_file = open(default_cache, 'rb')
        cache = pickle.load(cache_file)
        cache_file.close()
    except:
        cache = url_cache()

    proc = daemon(conf, cache)
    proc.start()

if __name__ == '__main__':
    main()
