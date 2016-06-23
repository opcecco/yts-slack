#!/usr/bin/env python

import json, re, os, urllib, urllib2, random
import config


class YTSBot:

	def __init__(self):
		self.user = None
		self.awaiting_choice = {}


	def respond(self, userid, message):
		if self.user in message:
			message = message.lower()
			if 'find ' in message:
				title = message.split('find ', 1)[1]
				return self.find_movie(userid, title)
			if userid in self.awaiting_choice.keys():
				if 'no' in message:
					del(self.awaiting_choice[userid])
					return random.choice(config.friendly_responses) + '<@' + userid + '>. I won\'t download any of them.'
				match = re.findall('\d+', message)[-1]
				if match is not None:
					if 'about' in message:
						return 'Note: This is a debug feature...\n' + str(self.awaiting_choice[userid][int(match) -1])
					else:
						return self.select_movie(userid, int(match) - 1)
		return None


	def select_movie(self, userid, selection):
		if selection >= len(self.awaiting_choice[userid]):
			return 'That movie is not on the list.'
		
		movie = self.awaiting_choice[userid][selection]
		del(self.awaiting_choice[userid])

		url = [torrent['url'] for torrent in movie['torrents'] if torrent['quality'] == config.search_values['quality']][0]
		self.download(url)
		return random.choice(config.friendly_responses) + '<@' + userid + '>. I\'ll download ' + movie['title'] + ' (' + str(movie['year']) + ')!'


	def find_movie(self, userid, movie_title):
		data = self.query(movie_title)['data']

		if data['movie_count'] == 0:
			return 'I couldn\'t find that movie, <@' + userid + '>.'

		self.awaiting_choice[userid] = data['movies']
		outstring = 'Which movie did you mean, <@' + userid + '>?\n'

		outstring += '\n'.join(['[' + str(data['movies'].index(movie) + 1) + '] ' + movie['title'] + ' (' + str(movie['year']) + ')\n' + movie['medium_cover_image'] for movie in data['movies']])
		return outstring


	def download(self, url):
		print 'Downloading ' + url
		filename = url.split('/')[-1]
		request = urllib2.Request(url, headers = {'User-Agent': config.browser_spoof})
		infile = urllib2.urlopen(request)
		
		with open(os.path.expanduser(config.download_folder + '/' + filename), 'wb') as outfile:
			outfile.write(infile.read())
		return


	def query(self, search_term):
		search_values = config.search_values
		search_values['query_term'] = search_term

		data = urllib.urlencode(search_values)
		url = 'https://yts.ag/api/v2/list_movies.json?' + data
		print 'Querying ' + url

		request = urllib2.Request(url, headers = {'User-Agent': config.browser_spoof})
		result = urllib2.urlopen(request)
		return json.loads(result.read())
