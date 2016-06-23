#!/usr/bin/env python

from time import sleep
#from slackclient import SlackClient

from ytsbot import YTSBot
import config


# Hijack it here for testing

bot = YTSBot()
while True:
	userid = 'opcecco'
	message = raw_input().lower()
	response = bot.respond(userid, message)
	if response is not None:
		print response

exit()


# Here's the real code

client = SlackClient(config.slack_token)

if not client.rtm_connect():
	print 'Connection Failed'
	exit()

while True:
	try:
		stream = client.rtm_read()
		
		for event in stream:
			
			if 'type' in event and 'channel' in event and 'text' in event and 'user' in event and event['type'] == 'message':
				
				uchannel = event['channel']
				text = event['text'].encode('utf8', 'ignore')
				userid = event['user'].encode('utf8', 'ignore')
				
				response = bot.respond(userid, text)
				
				if response is not None:
					client.rtm_send_message(uchannel, response)
				
	except:
		pass
	
	sleep(config.listen_delay)
