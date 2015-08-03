#! /usr/bin/python

import requests, sys, os, pytz
from datetime import datetime
import jgtools as jg

def create_course(account, name, sis, term, start, end):
	
	params["account_id"] = account
	params["course[name]"] = name
	params["course[course_code]"] = params["course[name]"]
	params["course[license]"] = "private"
	params["course[term_id]"] = term
	params["course[sis_course_id]"] = sis

	if start != '':
		params["course[start_at]"] = start.isoformat()
	if end != '':
		params["course[end_at]"] = end.isoformat()
	
	print params
	sys.exit()
	
	new_course = requests.post(url + "/api/v1/accounts/%s/courses" % account, params=params)

	if "400" in str(new_course):
		new_course = requests.get(url + "/api/v1/courses/sis_course_id:%s" % sis, params=params)
		try:
			sis = new_course.json()["sis_course_id"]
		except:
			print new_course.json()
		print str(sis) + " retrieved."

	else:
		print str(sis) + " created."

	return sis

def copy_course(account, new_sis, source_sis):

	params["account_id"] = account
	source_course = requests.get(url + "/api/v1/courses/sis_course_id:%s" \
		% source_sis, params=params)
	
	try:
		source_course_code = source_course.json()['id']
	except KeyError:
		print "\n\nSource course issue!"
		print source_course.json()
		if "does not exist" in str(source_course.json()):
			print "\nSource course incorrect or in wrong account.\n"
		sys.exit()

	params["migration_type"] = "course_copy_importer"	
	params["settings[source_course_id]"] = source_course_code
#	params["date_shift_options[remove_dates]"] = False
	
	copy_response = requests.post(url + "/api/v1/courses/sis_course_id:%s/content_migrations" \
		% new_sis, params=params).json()
	print "Migration of " + copy_response['settings']['source_course_name'] + \
		" to %s in progress.\n" % new_sis


def main():

	print "1: Use root account\n2: Type account ID"
	account_choice = int(raw_input(">>> "))
	if account_choice == 1:
		account = 86563
	elif account_choice == 2:
		account = int(raw_input("Please type the Account ID: "))
	else:
		print "Fail."
		sys.exit()

	print "\nCSV Format: | New Course Name | New Course SIS |"\
		" Source Course SIS | Start Date/Time | End Date/Time | Time Zone |"\
		"\nDate/time format: 'DD-MM-YYYYTHH:MM', timezone = 'UTC'"\
		"\nE.g.: '17-02-1991T07:35', timezone = 'EST'"
	courses = jg.dragfile()
	root_account = 86563
	term = jg.terms(root_account, url, params).choose()
	
	for line in courses:
	
		# [New name, New SIS, Source SIS, Start Date, End Date, Time Zone]
		# Datetime format: "17-02-1991T07:35", timezone = "EST"


		newcoursename = line[0]
		newcoursesis = line[1]
		sourcecoursesis = line[2]
		startdate, starttime = line[3].split('T')[0], line[3].split('T')[1]
		enddate, endtime = line[4].split('T')[0], line[4].split('T')[1]
		if line[5] == '':
			localtz = None
		else:
			localtz = line[5]
		
		if startdate != '':
			start = jg.canvasdate(startdate, starttime, localtz).get()
		
		if enddate != '':
			end = jg.canvasdate(startdate, starttime, localtz).get()

		new_sis = create_course(account, newcoursename, newcoursesis, \
			term, start, end)
	
		copy_course(account, new_sis, sourcecoursesis)
