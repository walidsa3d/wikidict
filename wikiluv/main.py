import sys
import time
import click
import requests
import threading
import os
from rich.console import Console
from rich.spinner import Spinner
from rich.text import Text
from wikiluv.lancodes import codes
from wikiluv.utils import justify

console = Console()
BASE_URL = "https://{lang}.wikipedia.org/w/api.php?continue=&action=query&titles={query}&prop=extracts&exintro=&explaintext=&format=json&redirects&formatversion=2"
class Info:
    SUMMARY = "Not Found"

def get_summary(query, lang):
    url = BASE_URL.format(lang=lang,query=query)
    try:
        response = requests.get(url).json()
        pages = response['query']['pages']
    except Exception as e:
        print("Failed to get page")
    extract = pages[0].get('extract', None)
    if extract is not None:
        Info.SUMMARY = extract

def typewrite(text, delay=0.07):
    """Simulate ChatGPT-style typewriting effect."""
    for char in text:
        console.print(char, end='', style="bold green")
        time.sleep(delay)
    console.print()

@click.command()
@click.argument('query', nargs=-1)
@click.option('--lang', '-l', default='en', help="Wikipedia's language code")
@click.option('--color/--no-color', default=True, help="Enable or disable colored output")
def main(query, lang, color):
    if lang not in codes.keys():
        lang = 'en'
    query = ' '.join(query).strip()

    # Start a spinner thread while loading
    worker = threading.Thread(target=get_summary, args=(query, lang))
    worker.start()
    # Create a spinner using rich
    spinner = Spinner('dots', text='Fetching summary...')
    with console.status(spinner, spinner_style="green") as status:
        while worker.is_alive():
            worker.join(0.1) 
    terminal_width = os.get_terminal_size().columns
    text_width = int(0.8 * terminal_width)
    summary_text = Info.SUMMARY

    # Justify the text
    justified_summary = justify(summary_text, text_width)

    if color:
        justified_summary = Text(justified_summary, style="bold green")
    typewrite(justified_summary)

if __name__ == "__main__":
    main()