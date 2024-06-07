#------------------------------------------------------------------------------
#pip install pyyaml
#pip install feedparser
#pip install colorama
#pip install lxml
#------------------------------------------------------------------------------

#----------------------------------------------------------------------- import
import os
import re
import time
from datetime import datetime, timedelta

#libs
import feedparser
import yaml
from lxml import html
import colorama
from colorama import Fore, Back, Style, ansi

#----------------------------------------------------------------------- screen
def clear_console():
	"""Função para limpar o console."""
	if os.name == 'nt':  # Para Windows
		os.system('cls')
	else:  # Para Unix/Linux/macOS
		os.system('clear')

def type_out(text, delay=0.05):

	if delay == 0.05:
		delay = config['delay']

	for char in text:
		print(char, end='', flush=True)
		time.sleep(delay)
	print()  # Para adicionar uma nova linha após o texto

#------------------------------------------------------------------------- feed
def load_config(config_file):
	"""Função para carregar configurações de um arquivo YAML."""
	with open(config_file, 'r') as file:
		config = yaml.safe_load(file)
	return config

def get_entry_color(entry):
	"""Função para carregar configurações de um arquivo YAML."""
	
	published_date = None
	if getattr(entry, 'published', None) != None:
		published_date = entry.published
	else:
		return int(config['colors']['entry']['default'])

	#Mon, 20 May 2024 15:16:59 GM
	if re.match( r'^[A-Z][a-z]{2}, \d{2} [A-Z][a-z]{2} \d{4} \d{2}:\d{2}:\d{2} GMT$', published_date):
		data_evento = datetime.strptime(published_date, "%a, %d %b %Y %H:%M:%S %Z")
	#2024-05-22 16:39:21
	elif re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', published_date):
		# Converter a string para um objeto datetime
		data_evento = datetime.strptime(published_date, "%Y-%m-%d %H:%M:%S")
	else:
		return int(config['colors']['entry']['default'])

	# now
	agora = datetime.now()

	# last 15 minutes
	if agora - data_evento <= timedelta(minutes=15): 
		return int(config['colors']['entry']['last_15min'])
	# last hour
	elif agora - data_evento <= timedelta(hours=1):
		return int(config['colors']['entry']['last_hour'])
	# today
	elif data_evento.date() == agora.date():
		return int(config['colors']['entry']['today'])
	# old
	else:
		return int(config['colors']['entry']['old'])

def validade_feed(rss_url, feed):
	property_title_color = int(config['colors']['feed']['property_title'])
	title = getattr(feed.feed, 'title', '')
	if len(title) > 0:
		title = html.fromstring(title).text_content()
	
	description = getattr(feed.feed, 'description', '')
	if len(description) > 0:
		description = html.fromstring(description).text_content()

	type_out(f"{ansi.code_to_chars(property_title_color)}feed.url:{Style.RESET_ALL} {rss_url}", 0.01)
	type_out(f"{ansi.code_to_chars(property_title_color)}feed.title:{Style.RESET_ALL} {title}", 0.01)
	type_out(f"{ansi.code_to_chars(property_title_color)}feed.description:{Style.RESET_ALL} {description}", 0.01)
	type_out(f"{ansi.code_to_chars(property_title_color)}feed.entries:{Style.RESET_ALL} {len(getattr(feed, 'entries', 0))}", 0.01)

	totalEntries = len(feed.entries)

	#remove invalid entry
	removeList = []
	for entry in feed.entries:
		if (getattr(entry, 'published', None) is None) or (getattr(entry, 'title', None) is None):
			removeList.append(entry)
	
	feed.entries = [elem for elem in feed.entries if elem not in removeList]

	#entries != valid_entries
	if len(feed.entries) < totalEntries:
		type_out(f"{ansi.code_to_chars(property_title_color)}feed.entries.valid:{Style.RESET_ALL} {len(feed.entries)}", 0.01)

#------------------------------------------------------------------------- main
countTotalEntry=0
config=None
def main():
	global countTotalEntry
	global config

	#clear screen
	clear_console()

	# load configuration
	config = load_config('config.yaml')

	# init colorama
	colorama.init()

	#load some config properties
	feed_count_color = int(config['colors']['feed']['count'])
	link_color = int(config['colors']['feed']['link'])

	#to console-> {len(rss_url)} RSS feeds found!
	type_out(f"{ansi.code_to_chars(feed_count_color)}{len(config['rss_url'])}{Style.RESET_ALL} RSS feeds found!")

	try:
		while True:
			for rss_url in config['rss_url']:

				countEntry=0

				#to console-> Loading news from: {RSS_URL}
				type_out(f"\nLoading news from: {ansi.code_to_chars(link_color)}{rss_url}{Style.RESET_ALL}")

				# RSS feed parsing
				feed = feedparser.parse(rss_url)

				# remove invalid entry
				validade_feed(rss_url, feed)

				countTotalEntry += len(feed.entries)

				# show feed entries
				for entry in feed.entries:
					countEntry += 1
					type_out(f"\n{ansi.code_to_chars(get_entry_color(entry))}{Style.BRIGHT}->{Style.RESET_ALL} {str(countEntry).zfill(len(str(len(feed.entries))))}/{len(feed.entries)}|{countTotalEntry} [{getattr(entry, 'published', None)}] {entry.title}")
										
					if (getattr(entry, 'summary', None) is not None) and (len(entry.summary) > 0):
						type_out(html.fromstring(entry.summary).text_content())

	except KeyboardInterrupt:
		colorama.deinit()

if __name__ == "__main__":
	main()
