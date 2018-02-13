## Config file for YTS Movie Slack Bot

# Delay for main listen loop
listen_delay = 1.0

# Folder to download torrent files to
download_folder = '~'

# URL for the YTS movie restful API
yts_url = 'https://yts.am/api/v2/list_movies.json'

# Parameters for the search, please refer to their API
search_values = {
	'quality': '720p',
	'limit': '3',
	'sort_by': 'date_added',
}

# Responses when downloading
positive_responses = (
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

# Responses when cancelling a download
negative_responses = (
	'Alright, ',
	'OK, ',
	'Fine, ',
	'Nevermind then, ',
	'If you say so, ',
	'Less work for me, ',
	'Cool beans, ',
)
