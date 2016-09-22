#!/usr/bin/env python


###############################
##    YTS Movie Slack Bot    ##
## Author: Oliver Ceccopieri ##
##   Designed for Python 2   ##
###############################


import slackclient, time, socket
import ytsbot, config


# Connect to Slack
client = slackclient.SlackClient(config.slack_token)
if not client.rtm_connect():
	print 'Connection Failed'
	exit()

# Create the bot and find it's user ID (the first user it sees in the channel)
bot = ytsbot.YTSBot()
while bot.user == None:
	stream = client.rtm_read()
	for event in stream:
		if 'type' in event and event['type'] == 'presence_change':
			bot.user = event['user']
			break
print 'Bot ID is: ' + bot.user

# Main listen loop
while True:
	try:
		stream = client.rtm_read()
		for event in stream:
			if 'type' in event and 'channel' in event and 'text' in event and 'user' in event and event['type'] == 'message':
				uchannel = event['channel']
				text = event['text'].encode('utf8', 'ignore')
				userid = event['user'].encode('utf8', 'ignore')

				# Get a response from the bot
				response = bot.respond(userid, text)
				if response is not None:
					client.rtm_send_message(uchannel, response)

	# Catch any and all exceptions and print them for debug
	except UnicodeDecodeError:
		print '! --> Unicode Decode Error'

	except socket.error:
		print '! --> Socket closed'
		exit()

	except Exception as e:
		print '!!! --> Uncaught exception: ' + e.__class__.__name__
		print str(type(e))
		print str(e)

	# Wait so we don't eat CPU time
	time.sleep(config.listen_delay)
