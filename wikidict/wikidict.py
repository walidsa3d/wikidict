#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools

import threading

import os
import requests

from sys import argv
from sys import stdout
summary = ""


def get_summary(query):
    global summary
    url = "https://en.wikipedia.org/w/api.php?continue=&action=query&titles=%s&prop=extracts&exintro=&explaintext=&format=json&redirects" % query
    response = requests.get(url).json()
    pages = response['query']['pages']
    extract = pages[pages.keys()[0]].get('extract', None)
    if extract is not None:
        summary = extract
    else:
        summary = "Not Found"


def main():
    script, query = argv
    spinner = itertools.cycle(['-', '/', '\\'])
    w = threading.Thread(name='worker', target=get_summary, args=(query,))
    w.start()
    os.system('setterm -cursor off')

    while w.isAlive():
        stdout.write(spinner.next())  # write the next character
        stdout.flush()                # flush stdout buffer
        stdout.write('\b')

    print summary
    os.system('setterm -cursor on')
