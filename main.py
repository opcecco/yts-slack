#!/usr/bin/env python

import json
from urllib import urlencode
from urllib2 import Request, urlopen
from time import sleep
#from slackclient import SlackClient

import config


# client = SlackClient(config.slack_token)

# if !client.rtm_connect():
	# print 'Connection Failed'
	# exit()
	
# awaiting_choice = {}

# while True:
	# try:
		# stream = client.rtm_read()
		
		# for event in stream:
			
			# if 'type' in event and 'channel' in event and 'text' in event and 'user' in event and event['type'] == 'message':
				
				# uchannel = event['channel']
				# text = event['text'].encode('utf8', 'ignore')
				# userid = event['user'].encode('utf8', 'ignore')
				
				# response = bot.respond(userid, text)
				
				# if response is not None:
					# client.rtm_send_message(uchannel, response)
				
	# except:
		# pass
	
	# sleep(config.listen_delay)
	
	
def query_movie(search_term):
	search_values = config.search_values
	search_values['query_term'] = search_term
	data = urlencode(search_values)
	url = 'https://yts.ag/api/v2/list_movies.json?' + data
	request = Request(url, headers = {'User-Agent': config.browser_spoof})
	response = urlopen(request)
	return json.loads(response.read())
	