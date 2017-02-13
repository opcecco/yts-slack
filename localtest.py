#!/usr/bin/env python3


# Local test script for YTS Movie Slack Bot
# Author: Oliver Ceccopieri
# Designed for Python 3


import ytsbot


bot = ytsbot.YTSBot()
bot.user = 'bot'
userid = 'localtest'

print('Local bot tester. He will respond to "@bot"')

while True:
	message = input('>')
	response = bot.respond(userid, message)
	if response is not None:
		print(response)
