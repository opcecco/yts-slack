#!/usr/bin/env python


# Local test script for YTS Movie Slack Bot
# Author: Oliver Ceccopieri
# Designed for Python 2


import ytsbot


bot = ytsbot.YTSBot()
bot.user = 'bot'
userid = 'tester'

print 'Local bot tester. He will respond to "@bot"'

while True:
	message = raw_input('>')
	response = bot.respond(userid, message)
	if response is not None:
		print response
