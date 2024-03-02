import json
import random
from urllib import request
import string

def generate_email():
    # Generates a random email with the domain '@blondmail.com'
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return username + '@blondmail.com'

class User:
	def __init__(self, email, first_name, last_name, password):
		self.email = email
		self.first_name = first_name
		self.last_name = last_name
		self.password = password

		self.name = self.first_name.capitalize() + ' ' + self.last_name.capitalize()

	@staticmethod
	def create(handlers=[]):
		opener = request.build_opener(*handlers)

		url = 'https://randomuser.me/api'
		req = request.Request(url)
		res = opener.open(req)
		text = res.read().decode()
		info = json.loads(text)

		first_name = info['results'][0]['name']['first']
		last_name = info['results'][0]['name']['last']
		password = info['results'][0]['login']['password'] + str(random.randint(100, 999))

		if not all([len(s.encode()) == len(s) for s in (first_name, last_name, password)]):
			return User.create()

		email = generate_email()

		return User(email, first_name, last_name, password)
