import json
import fileinput
import requests

class Loader(object):
	def __init__(self):
		self.name = "Ahmad"
		self.api_key = "sdhufuserhfhrjf"
		self.api = "http://127.0.0.1:5000/super_url"
		self.machine_name = "Terminator"
		self.results = []

	def do_it():
		for line in fileinput.input():
			d = {"username": self.name, 
				"api_key": self.api_key, 
				"machine_name": self.machine_name, 
				"line": line, 
				"line_number": fileinput.filelineno()}
			result = requests.post(self.api, data=json.dumps(d))
			self.results.append(result)
		fileinput.close()

if __name__ == "__main__":
	load = Loader()
	load.do_it()
