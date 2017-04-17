#!/usr/bin/env python3


###############################
##    YTS Movie Slack Bot    ##
## Author: Oliver Ceccopieri ##
##   Designed for Python 3   ##
###############################


import slackclient, time, socket
import ytsbot, config


'''
Return only ASCII text of a string
'''
def ascii_only(string):
	return ''.join([c for c in string if 32 <= ord(c) <= 126])


'''
Connect to the slack channel
'''
def slack_connect():
	global client
	client = slackclient.SlackClient(config.slack_token)
	if not client.rtm_connect():
		print('Connection Failed')
		exit()

	# Create the bot and find it's user ID (the first user it sees in the channel)
	bot = ytsbot.YTSBot()
	while bot.user == None:
		stream = client.rtm_read()
		for event in stream:
			if 'type' in event and event['type'] == 'presence_change':
				bot.user = event['user']
				break
	print('Bot ID is: ' + bot.user)


# Main script
slack_connect()
while True:
	try:
		stream = client.rtm_read()
		for event in stream:
			if 'type' in event and 'channel' in event and 'text' in event and 'user' in event and event['type'] == 'message':
				uchannel = event['channel']
				text = ascii_only(event['text'])
				userid = ascii_only(event['user'])

				# Get a response from the bot
				response = bot.respond(userid, text)
				if response is not None:
					client.rtm_send_message(uchannel, response)

	# Catch any and all exceptions and print them for debug
	except UnicodeDecodeError:
		print('! --> Unicode Decode Error')

	except websocket._exceptions.WebSocketConnectionClosedException:
		print('! --> Connection closed')
		print('Attempting reconnect...')
		slack_connect()

	except Exception as e:
		print('!!! --> Uncaught exception: ' + e.__class__.__name__)
		print(str(type(e)))
		print(str(e))

	# Wait so we don't eat CPU time
	time.sleep(config.listen_delay)
