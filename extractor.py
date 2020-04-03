"""
Get IP frequency distribution
"""

# Standard library imports
import glob
import re
from pathlib import Path

import ipinfo
import pprint

# Local application imports
import config

#----------------------------------------------------------------------

class FrequencyDistribution():

	DEBUG 			= True
	OUT_FILENAME 	= "output.txt"
	regex 			= re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

	def __init__(self):
		# Exctract data 
		self.data = self.extract()
		# Record output
		self.tally = self.get_tally(self.data) 			
		# Record output
		self.record(self.tally) 		

	def extract(self):
		
		# Store found links
		found = []

		# Loop log files
		for idx, file in enumerate( Path('data').glob('*.csv') ):

			# Get contents
			with open(file, 'rb') as f:
				contents = f.read()

				# Covert bytes to string
				content_string =  str(contents)

				# Search using regex
				matches = self.regex.findall(content_string)

				# Record results
				for ip in matches:
					found.append(ip)

		# Return results
		return found

	def get_tally (self, data):
		tally = {}

		for ip in data:
			if ip in tally:				
				count = tally[ip]
				tally[ip] = count + 1
			else:
				tally[ip] =  1

		return tally


	def lookup_ip( self, ip ):
		handler = ipinfo.getHandler(config.access_token)
		details = handler.getDetails( ip  )
		# pprint.pprint(details.all)
		return details.org

	def record(self, tally):

		# sort tally by count 
		sorted_d = sorted(tally.items(), key=lambda x: x[1], reverse=True )

		i = 1

		with open(self.OUT_FILENAME, "w") as txt_file:
			for key, val in sorted_d:

				if i < 20:
					details = self.lookup_ip(key)
					txt_file.write( str(key) + ' : ' + str(val) + ' - ' + str(details) + '\n'  )

					i += 1




# End FrequencyDistribution Class
#----------------------------------------------------------------------		

if __name__ == '__main__':
	FrequencyDistribution()