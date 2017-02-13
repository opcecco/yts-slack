## Config file for YTS Movie Slack Bot

# Token so your bot can connect to your slack channel
slack_token = 'xoxb-00000000000-XXXXXXXXXXXXXXXXXXXXXXXX' ### INSERT YOUR OWN SLACK TOKEN HERE

# Delay for main listen loop
listen_delay = 1.0

# Folder to download torrent files to
download_folder = '~/watch'

# URL for the YTS movie restful API
yts_url = 'https://yts.ag/api/v2/list_movies.json'

# Parameters for the YTS.ag search, please refer to their API
search_values = {
	'quality': '720p',
	'limit': '3',
	'sort_by': 'date_added',
}

# Make him a little more personable
friendly_responses = (
	'Alright, ',
	'OK, ',
	'Sounds good, ',
	'Sure thing, ',
	'You got it, ',
	'Good choice, ',
	'Good to go, ',
	'Glad I could help, ',
	'Nice choice, ',
	'You have good taste, ',
	'Great selection, ',
	'Fine with me, ',
	'That\'s a good one, ',
	':wink: Let\'s watch it together, ',
	'Huh really? Whatever you say, ',
)
