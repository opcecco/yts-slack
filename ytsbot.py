#!/usr/bin/env python


# YTS bot class for the YTS Movie Slack Bot
# Author: Oliver Ceccopieri
# Designed to be run in Python 2


import json, re, os, urllib, urllib2, random
import config


"""
YTS Bot class, the brain of the bot
"""
class YTSBot:

	"""
	Initialize the bot
	"""
	def __init__(self):
		self.user = None
		self.awaiting_choice = {}

	"""
	Respond to a channel message
	params: userid of user who is talking, message that was sent
	return: the bot's response, can be None
	"""
	def respond(self, userid, message):
		if self.user in message:
			message = message.split(self.user, 1)[1].lower()

			# Check if someone wants the bot to find a movie
			if 'find ' in message:
				title = message.split('find ', 1)[1]
				return self.find_movie(userid, title)

			# Check if someone is selecting a movie from the given list
			if userid in self.awaiting_choice.keys():
				if 'no' in message:
					del(self.awaiting_choice[userid])
					return random.choice(config.friendly_responses) + '<@' + userid + '>. I won\'t download any of them.'

				matches = re.findall('\d+', message)
				if len(matches) > 0:
					if 'about' in message:
						return 'Note: This is a debug feature...\n' + str(self.awaiting_choice[userid][int(matches[-1]) -1])
					else:
						return self.select_movie(userid, int(matches[-1]) - 1)

		# If the message is nothing of interest, just ignore it
		return None

	"""
	Let the user select a movie
	params: userid of user who is talking, selection number of movie
	return: a friendly response from the bot
	"""
	def select_movie(self, userid, selection):
		if selection >= len(self.awaiting_choice[userid]):
			return 'That movie is not on the list.'

		# Grab movie info out of stored dictionary
		movie = self.awaiting_choice[userid][selection]
		del(self.awaiting_choice[userid])

		# Go download the file
		url = [torrent['url'] for torrent in movie['torrents'] if torrent['quality'] == config.search_values['quality']][0]
		self.__download(url)
		return random.choice(config.friendly_responses) + '<@' + userid + '>. I\'ll download ' + movie['title'] + ' (' + str(movie['year']) + ')!'

	"""
	Find a movie for a user
	params: userid of user who is talking, movie title (the search term)
	return: a response letting the user know which movies were found
	"""
	def find_movie(self, userid, movie_title):
		data = self.__query(movie_title)['data']

		if data['movie_count'] == 0:
			return 'I couldn\'t find that movie, <@' + userid + '>.'

		# Ask which movie to grab
		self.awaiting_choice[userid] = data['movies']
		outstring = 'Which movie did you mean, <@' + userid + '>?\n'

		outstring += '\n'.join(['[' + str(data['movies'].index(movie) + 1) + '] ' + movie['title'] + ' (' + str(movie['year']) + ')\n' + movie['medium_cover_image'] for movie in data['movies']])
		return outstring

	"""
	Grab file from url
	params: url of file
	return: None
	"""
	def __download(self, url):
		print 'Downloading ' + url
		filename = url.split('/')[-1]
		request = urllib2.Request(url, headers = {'User-Agent': config.browser_spoof})
		infile = urllib2.urlopen(request)
		
		with open(os.path.expanduser(config.download_folder + '/' + filename), 'wb') as outfile:
			outfile.write(infile.read())
		return

	"""
	Query YTS API for movies
	params: search term
	return: JSON dictionary of search results
	"""
	def __query(self, search_term):
		search_values = config.search_values
		search_values['query_term'] = search_term

		data = urllib.urlencode(search_values)
		url = 'https://yts.ag/api/v2/list_movies.json?' + data
		print 'Querying ' + url

		request = urllib2.Request(url, headers = {'User-Agent': config.browser_spoof})
		result = urllib2.urlopen(request)
		return json.loads(result.read())
