alarm_type = 'Magnitude'
alarm_name = 'Earthquake Magnitude' 

outfile = 'alarm_aux_files/Recent_earthquakes.txt'
volc_file = 'alarm_aux_files/volcano_list.xlsx'

MAGMIN = 2.5
MAXDEP = 40
DISTANCE = 10
DURATION = 2*3600

mattermost_channel_id = '1yxp3dhsjtd55jbbrawddzkk6h'

mm_response_channels = {
	'Aniakchak': 'eoeizwgp8bdnpmqpcicb7tjqbw',
	'Trident': 'd4e8jhmay7rbfe19za1zywwhpe',
	'Katmai': 'd4e8jhmay7rbfe19za1zywwhpe',
	'Martin': 'd4e8jhmay7rbfe19za1zywwhpe',
	'Mageik': 'd4e8jhmay7rbfe19za1zywwhpe',
	'Novarupta': 'd4e8jhmay7rbfe19za1zywwhpe',
	'Bogoslof': '6oppxzqt97bsikjgjxc5i6y3qh',
}