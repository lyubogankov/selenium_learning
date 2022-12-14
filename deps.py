import csv
import glob
import os
from pprint import pprint

if __name__ == '__main__':

	csvlines = list()

	# 1. recursively search through the repo and find all the python files.
	for path in glob.iglob('/home/lyubo/.local/lib/python3.6/site-packages/selenium/**/*.py', recursive=True):
		filepath, filename = os.path.split(path)
		relativepath = filepath.split('selenium')[1]
		relname = relativepath + '\\' + filename

		# 2. look at each python file and find the imports!
		with open(path, 'r') as f:
			for line in f:
				line = line.rstrip().replace('  ', '')
				if 'import' in line and 'from .' not in line:

					if 'selenium' not in line:
						#print(f"{relname:{45}} | {line:{150}}")
						print(line)
						csvlines.append([relname, line])
						

	# 3. write out to csv
	with open(r"/home/lyubo/script/selenium/deps.csv", 'w+', newline='') as o:
		writer = csv.writer(o, delimiter=',')
		writer.writerow([])
		for line in csvlines:
			writer.writerow(line)
