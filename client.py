#!/usr/bin/env python3


###############################
##    YTS Movie Slack Bot    ##
## Author: Oliver Ceccopieri ##
##   Designed for Python 3   ##
###############################


import sys, slackclient, time, websocket
import ytsbot, config


'''
Return only ASCII text of a string
'''
def ascii_only(string):
	return ''.join([c for c in string if 32 <= ord(c) <= 126])


'''
Connect to a Slack team and start the bot
'''
def start_bot(token):

	client = slackclient.SlackClient(token)
	timeout = config.listen_delay

	if not client.rtm_connect():
		print('Connection Failed')
		return

	# Get the bot's user ID to handle mentions
	bot_id = client.api_call('auth.test')['user_id']
	print('Bot ID is: ' + bot_id)

	bot = ytsbot.YTSBot()
	bot.user = bot_id

	# Message listener loop
	while True:

		try:
			stream = client.rtm_read()

			# Read all events in stream, react to user-entered messages only
			for event in stream:
				if 'type' in event and 'channel' in event and 'text' in event and 'user' in event and event['type'] == 'message':

					channel = event['channel']
					userid = ascii_only(event['user'])
					text = ascii_only(event['text'])

					# Respond only if a user mentions the bot
					if bot_id in text:
						response = bot.respond(user_id, text)

						if response is not None:
							client.rtm_send_message(channel, response)

		# Sometimes we get text decode errors
		except UnicodeDecodeError:
			print('! Unicode Decode Error')

		# Attempt to reconnect if our bot loses connection
		except websocket.WebSocketConnectionClosedException:
			print('Attempting reconnect...')

			if not client.rtm_connect():
				print('! Failed')
			else:
				print('Success')

		# Delay the next listen loop
		time.sleep(timeout)


'''
Start a bot
'''
if __name__ == '__main__':
	start_bot(sys.argv[1])
