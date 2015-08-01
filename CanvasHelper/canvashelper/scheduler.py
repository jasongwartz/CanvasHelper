# Scheduler

import requests, json, csv
import jgtools as jg


def sort_courses(data):
	
	# Title | Date | Start Time | End Time | TimeZone | Course SIS |
	# Datetime format: "17-02-1991T07:35", timezone = "EST"

	courses = {}

	for line in data:
		title, date, starttime, endtime, timezone, coursesis = \
			line[0], line[1].replace("/", "-"), line[2], line[3], line[4], line[5]

		if coursesis in courses.keys():
			courses[coursesis].append([title, date, starttime, endtime, timezone])
		else:
			courses[coursesis] = [[title, date, starttime, endtime, timezone]]

	return courses

def sort_titles(appointments):
	# [[title, date, starttime, endtime, timezone], [title, date, starttime, endtime, timezone]]
	
	groups = {}
	# 'my cool event':[[date, starttime, endtime, timezone], [date, starttime, endtime, timezone]]

	for i in appointments:
		title, date, starttime, endtime, timezone = i[0], i[1], i[2], i[3], i[4]
		if title in groups.keys():
			groups[title].append([date, starttime, endtime, timezone])
		else:
			groups[title] = [[date, starttime, endtime, timezone]]
	return groups


def create_appointment_group(course, title, appointments):

	# Remove any leftover appointments from previous iteration
	global params
	params = {key:value for key, value in params.items()
		if "new_appointments" not in str(key)}

	params["appointment_group[title]"] = title
	
	course_id = jg.courseid(url, params, course).get()
	params["appointment_group[context_codes][]"] = "course_%s" % course_id
	
	params["appointment_group[participants_per_appointment]"] = int(raw_input(
		"\nHow many participants per slot for %s: " % title))
	
	params["appointment_group[min_appointments_per_participant]"] = int(raw_input(
		"Minimum appointments each student must register for: "))
	params["appointment_group[max_appointments_per_participant]"] = int(raw_input(
		"Maximum appointments each student can register for: "))
	publish = raw_input("Publish automatically? 0 for no, 1 for yes: ")
	params["appointment_group[publish]"] = bool(publish)
	
	for index, time in enumerate(appointments):
		# time = [date, starttime, endtime, timezone]
		starttime = jg.canvasdate(time[0], time[1], time[3]).get()
		endtime = jg.canvasdate(time[0], time[2], time[3]).get()
		params["appointment_group[new_appointments][%d][]" % index] = \
			 [starttime.isoformat(), endtime.isoformat()]

	response = requests.post(url + "/api/v1/appointment_groups", params=params)
	response = response.json()
	print "\nCreated appointments for event: " + response['title']
	for i in response['new_appointments']:
		print "Created slot: " + i['start_at'] + " to " + i['end_at']

def main():

	data = jg.dragfile().get()
	sorted_by_course = sort_courses(data)

	for course, appointments in sorted_by_course.items():
		sorted_by_title = sort_titles(appointments)

		for title, appgroups in sorted_by_title.items():
			create_appointment_group(course, title, appgroups)

	print "\nScheduler complete.\n\n"
