#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools

import threading

import os
import requests

import argparse
import textwrap

import os

from .lancodes import codes
from sys import stdout
from termcolor import colored

SUMMARY = "Not Found"

def get_summary(query, lang):
    global SUMMARY
    url = "https://{lang}.wikipedia.org/w/api.php?continue=&action=query&titles={query}&prop=extracts&exintro=&explaintext=&format=json&redirects&formatversion=2".format(
        lang=lang, query=query)
    response = requests.get(url).json()
    pages = response['query']['pages']
    extract = pages[0].get('extract', None)
    if extract is not None:
        SUMMARY = extract


def loading(spinner):
    stdout.write(spinner.next())
    stdout.flush()
    stdout.write('\b')


def main():
    parser = argparse.ArgumentParser(usage="-h for full usage")
    parser.add_argument('query', help="search string", nargs="+")
    parser.add_argument('-c', '--color', action='store_true')
    parser.add_argument('-l', '--lang', help="wikipedia\'s language")
    args = parser.parse_args()
    lang = args.lang if args.lang in codes.keys() else 'en'
    query = ''.join(args.query).strip()
    worker = threading.Thread(
        name='worker', target=get_summary, args=(query, lang))
    worker.start()
    os.system('setterm -cursor off')
    spinner = itertools.cycle(['-', '/', '\\'])
    while worker.isAlive():
        loading(spinner)
    terminal_width = os.popen('stty size', 'r').read().split()[1]
    text_width = 50*int(terminal_width)/100
    summary = colored(SUMMARY, 'green', attrs=['bold'])
    if args.color:
        print textwrap.fill(summary, text_width, initial_indent='         ')
    else:
        print SUMMARY
    os.system('setterm -cursor on')

