from os import listdir, rename
from os.path import isfile, join
import json

def read_bookings(directory='./'):
	onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]
	bookings = []
	for file in onlyfiles:
		if not file.endswith('.json'):
			continue
		path=directory+('\\' if not directory.endswith('\\') else '')+file	
		file = open(path)
		booking = json.loads(file.read().strip())
		bookings+=[booking]
	for file in onlyfiles:
		path=directory+('\\' if not directory.endswith('\\') else '')+file
		rename(path,path+'.scheduled')
	return bookings

