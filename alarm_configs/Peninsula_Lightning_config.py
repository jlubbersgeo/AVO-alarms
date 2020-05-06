alarm_type = 'Lightning_old'
alarm_name = 'Peninsula Lightning' 

# Volcano names in question
volcanoes=['Veniaminof','Shishaldin','Dutton','Pavlof','Kupreanof','Isanotski','Aniakchak','Westdahl']

dist1 = 20			# distance for inner ring (in km)
dist2 = 100			# distance for outer ring (in km)
duration = 60*60	# time limit in seconds for remembering strokes

# Where to write most recent stroke data
outfile='alarm_aux_files/{}.txt'.format(alarm_name.replace(' ','_'))