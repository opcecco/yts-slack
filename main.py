#!/usr/bin/env python

import slackclient, time
import ytsbot, config


client = slackclient.SlackClient(config.slack_token)

if not client.rtm_connect():
	print 'Connection Failed'
	exit()

bot = ytsbot.YTSBot()

while bot.user == None:
	stream = client.rtm_read()
	for event in stream:
		if 'type' in event and event['type'] == 'presence_change':
			bot.user = event['user']
			break

print 'Bot ID is: ' + bot.user

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

	except Exception as e:
		print '!!! Exception: ' + e

	time.sleep(config.listen_delay)
