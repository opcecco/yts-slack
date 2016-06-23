#!/usr/bin/env python

import json, re, os
from urllib import urlencode
from urllib2 import Request, urlopen
from random import choice

import config


class YTSBot:

	def __init__(self):
		self.awaiting_choice = {}


	def respond(self, userid, message):
		if 'find ' in message:
			title = message.split('find ', 1)[1]
			return self.find_movie(userid, title)
		if userid in self.awaiting_choice.keys():
			match = re.search('\d+', message)
			if match is not None:
				if 'about' in message:
					return str(self.awaiting_choice[userid])
				else:
					return self.select_movie(userid, int(match.group()) - 1)
		return None


	def select_movie(self, userid, selection):
		if selection >= len(self.awaiting_choice[userid]):
			return 'That movie is not on the list.'
		
		movie = self.awaiting_choice[userid][selection]
		del(self.awaiting_choice[userid])

		url = [torrent['url'] for torrent in movie['torrents'] if torrent['quality'] == config.search_values['quality']][0]
		self.download(url)
		return choice(config.friendly_responses) + '<@' + userid + '>. I\'ll download ' + movie['title'] + ' (' + str(movie['year']) + ')!'


	def find_movie(self, userid, movie_title):
		data = self.query(movie_title)['data']

		if data['movie_count'] == 0:
			return 'I couldn\'t find that movie, <@' + userid + '>.'

		self.awaiting_choice[userid] = data['movies']
		outstring = 'Which movie did you mean, <@' + userid + '>?\n'

		outstring += '\n'.join(['[' + str(data['movies'].index(movie) + 1) + '] ' + movie['title'] + ' (' + str(movie['year']) + ') ' + movie['medium_cover_image'] for movie in data['movies']])
		return outstring


	def download(self, url):
		filename = url.split('/')[-1]
		request = Request(url, headers = {'User-Agent': config.browser_spoof})
		infile = urlopen(request)
		
		with open(os.path.expanduser(config.download_folder + '/' + filename), 'wb') as outfile:
			outfile.write(infile.read())
		return


	def query(self, search_term):
		search_values = config.search_values
		search_values['query_term'] = search_term

		data = urlencode(search_values)
		url = 'https://yts.ag/api/v2/list_movies.json?' + data

		request = Request(url, headers = {'User-Agent': config.browser_spoof})
		result = urlopen(request)
		return json.loads(result.read())
