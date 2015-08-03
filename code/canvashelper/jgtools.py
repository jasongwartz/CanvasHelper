#! /usr/bin/python

# My modules/classes used in other scripts

import requests, os, csv, json, sys, webbrowser, time, pytz, oauthlib, datetime
from requests_oauthlib import OAuth2Session


## Files and folders

class dragfile():
	def __init__(self):
		while True:
			print "Please drag in the CSV file:"
			self.filename = raw_input(">>> ").replace("\\", "")[:-1] # Strips the slash and trailing space
			if os.path.exists(self.filename):
				break
			else:
				print "Error loading file. Try again."

	def get(self):
		with open(self.filename, "r") as fp:
			data = [line for line in csv.reader(fp)]
		return data

class filedir():	
	def get(self):
		return os.path.dirname(os.path.realpath(__file__))

class fileout:
	def get(self):
		return os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, os.pardir,
			'output')

## Canvas Data retrieval

class api_list():
	def __init__(self, url, params):
		self.url = url + "?page=1"
		self.params = params
	
	def call(self):
		results = []
		counter = 0
		print "\nResults across multiple API pages. Please wait..."
		while True:
			counter += 1
			r = requests.get(self.url, params = self.params)
			for i in r.json():
				if len(results) > 0 and i == results[-1]:
					print ""
					return results
				else:
					results.append(i)
			print "Retrieved page " + str(counter)
			if 'next' in r.links.keys():
				self.url = r.links['next']['url']
			else:
				print ""
				return results

class terms():
	def __init__(self, accountid, url, params):
		self.url = url
		self.params = params
		self.id = accountid

	def choose(self):
	# Retrieves terms based on all courses in a given account	
		all_terms = {}

		self.params["per_page"] = 50
		self.params["include[]"] = "term"
		
		all_courses = api_list(self.url + "/api/v1/accounts/%s/courses" \
			% self.id, self.params)
		all_courses = all_courses.call()
		for i in all_courses:
			term_id = i['term']['id']
			term_name = i['term']['name']
			if term_name not in all_terms.keys():
				all_terms[term_name] = term_id
		 
 		for index, item in enumerate(all_terms.keys()):
			print str(index) + ": " + item

		choice = int(raw_input(">>> "))
		chosen_term_name = all_terms.keys()[choice]
		print "\nSelected Term ID: " + chosen_term_name
		chosen_term_id = all_terms[chosen_term_name]
		return chosen_term_id


	def deprecated_choose(self):
	# Only works if the user has permission to the account with all terms
		terms = requests.get(self.url + "/api/v1/accounts/%s/terms" % self.id, params=self.params)
		
		if '401' in str(terms):
			print "\nError report from Canvas:"
			print terms.json()['errors'][0]['message']
			print "\n\n"
			sys.exit()
		terms = terms.json()['enrollment_terms']

		for index, items in enumerate(terms):
			print str(index) + ": " + items['name']
	
		choice = int(raw_input(">>> "))
		print "\nSelected Term ID: " + str(terms[choice]['id'])
		termchoice = terms[choice]['id']
		return termchoice

class courseid():
	def __init__(self, url, params, sis):
		self.url = url
		self.params = params
		self.sis = sis
	def get(self):
		response = requests.get(self.url + '/api/v1/courses/sis_course_id:%s' % self.sis,
			 params=self.params)
		response = response.json()
		try:
			return response['id']
		except KeyError:
			if "exist" in str(response):
				print "\nERROR: This course does not exist.\n\n"
				sys.exit()
			else:
				raise

class canvasdate():
	# Datetime format: "17-02-1991", "07:35", timezone = "EST"
	def __init__(self, date, time, tz):
		self.date = date
		self.time = time
		self.tz = tz
	
	def convert_tz(self):
		try:
			self.localtz = pytz.timezone(self.tz)
		except pytz.exceptions.UnknownTimeZoneError as error:
			print "\n\n\nIncorrect date/time formatting!\n\n\n"
			print "Unknown Time Zone: " + error
			print "For a list of supported time zones, use the TZ column from: \n"\
				"https://en.wikipedia.org/wiki/List_of_tz_database_time_zones \n"
			sys.exit()

	def convert_datetime(self):		
		self.date_and_time = datetime.datetime.strptime(
			self.date + "T" + self.time, "%d-%m-%YT%H:%M")	

	def localize(self):			
		try:
			self.date_and_time = self.localtz.localize(self.date_and_time)
		except AttributeError as err:
			if "localtz" in str(err):
				self.convert_tz()
				self.localize()
			elif "date_and_time" in str(err):
				self.convert_datetime()
				self.localize()
			else:
				raise

	def get(self):
		self.convert_datetime()
		if self.tz != None:
			self.localize()
		return self.date_and_time
		

## Authentication

class oauth():
	def __init__(self):

		self.directory = os.path.dirname(os.path.realpath(__file__))
		self.keys_file = os.path.join(self.directory, "sensitive.json")

		if os.path.exists(self.keys_file):
			self.readfile()
		else:
			self.createfile()

	def check_login(self, check_url, check_token):
		params = {"access_token":check_token}
		response = requests.get(check_url + "/api/v1/users/self", params=params)
		if '200' in str(response):
			print "Validated API token."
			return True
		else:
			print response
			return False

	def choose_data(self, data):
		token_choices = sorted(data, key = lambda x: x['nickname'].lower())
		if len(token_choices) > 1:
			print "Please choose the Canvas instance to access:\n"
			for num, choice in enumerate(token_choices):
				print str(num) + ": " + choice['nickname']
			token_choice =  token_choices[int(raw_input(">>> "))]
			self.url = token_choice['url']
			self.token = token_choice['api_token']
		else:
			self.url = token_choices[0]['url']
			self.token = token_choices[0]['api_token']

	def readfile(self):
		# {username:username, data:[{url:url, nickname:name, api_token:token}, ...]}
		with open(self.keys_file, "r") as fp:
			raw_data = json.loads(fp.read())

		username = raw_data['username']
		print "\nRetrieved API access tokens for %s.\n\n" % username
		self.choose_data(raw_data['data'])
		if not self.check_login(self.url, self.token):
			print "Login error. Check API tokens!\n"
			sys.exit()		

	def createfile(self):	
		print "SETUP: Let's save your API Access Tokens.\n\nPlease type your name:"
		username = raw_input(">>> ")

		print """\n\nHow many API tokens would you like to save?
		(You only have to do this once)"""

		all_data = []				
		num = int(raw_input(">>> "))	

		for i in range(num):
			successful = False
			while not successful:
				data = {}
				print "API Token %d: Type a nickname for this Canvas instance." % (i+1)
				data['nickname'] = raw_input(">>> ")
				print """Type the URL of the Canvas instance, before the API endpoint.
				eg. https://example.test.instructure.com
				"""
				data['url'] = raw_input(">>> ")
				data['api_token'] = self.get_token(data['url'])
				if self.check_login(data['url'], data['api_token']):
					all_data.append(data)
					successful = True

		with open(self.keys_file, "w") as fp:
			fp.write(json.dumps({"username":username, "data":all_data}))
		self.choose_data(all_data)

	def get_token(self, url):
		os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = "1"
		
		# Retrieve dev key details from .json file
		# {client_id:id, client_secret:secret}
		with open(os.path.join(self.directory, "devkey.json"), "r") as fp:
			data = json.loads(fp.read())
		client_id = data["client_id"]
		client_secret = data["client_secret"]
		
		redirect_uri = 'urn:ietf:wg:oauth:2.0:oob' # Out-of-band redirect
		scope = [url, url]
		oauth = OAuth2Session(client_id, redirect_uri=redirect_uri,
			scope=scope)
		authorization_url, state = oauth.authorization_url(
			url + "/login/oauth2/auth")
		
		print "\n\nA web page will now launch and ask for authorization.\n" \
			"Please approve authorization, copy the URL from the browser after authorization,\n" \
			"(the URL after redirect, which includes 'code'), and paste it here."
		time.sleep(3)
		print "\n\nYou can also copy and paste this link into your browser: \n%s\n\n" \
			% authorization_url
		time.sleep(1)
		print "Please wait...\n"
		time.sleep(2)
		webbrowser.open(authorization_url)

		authorization_response = raw_input('\n\nEnter the full callback URL:  ')

		token = oauth.fetch_token(url + "/login/oauth2/token", 
			authorization_response=authorization_response, client_secret=client_secret)
		return token[u'access_token']








