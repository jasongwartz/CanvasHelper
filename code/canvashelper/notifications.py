# Batch change notification preferences

import requests
import json

params = {}

# Dict of all notifications to change
notifications = {
	"on":["new_file_added"], 
	"off":["grade_weight_changed"]
	}

def get_students(courses, params):
# Gets all student IDs from a course
	
	course_and_student_list = []
	sisids = []
	
	for course in courses:
		course_and_student_list.append(requests.get(url + "/api/v1/courses/sis_course_id:%s/students" 
			% course, params = params).json())
	
	for each_course in course_and_student_list:
		for student in each_course:
			try:
				sisids.append(student[u'sis_user_id'])
			except:
				pass		
	return sisids

###	Alternate to above loop using list comprehension
#	sis = [student[u'sis_user_id'] for student in each_course \
		# if u'sis_user_id' in student for each_course in course_and_student_list]

def get_channels(studentid, params):
# Returns a list of all communication IDs for a student's SISID

	channels_data = requests.get(url + "/api/v1/users/"
		"sis_user_id:%s/communication_channels" % studentid, params = params).json()
	return [ch[u'address'] for ch in channels_data]
		
def adjust_notifs(studentid, channel, params, notifications):
# Takes an SISID and channel ID, adjusts preferences

	# Turn on some notifications
	params["notification_preferences[frequency]"] = "weekly"
	for notifs in notifications["on"]:	
		url = url + "/api/v1/users/" \
			"self/communication_channels/%s/notification_preferences/%s" \
			"?as_user_id=sis_user_id:%s" % (channel, notifs, studentid)
		requests.put(url, params = params)
				
	# Turn off some notifications
	params["notification_preferences[frequency]"] = "never"
	for notifs in notifications["off"]:			
		url = url + "/api/v1/users/" \
			"self/communication_channels/%s/notification_preferences/%s" \
			"?as_user_id=sis_user_id:%s" % (channel, notifs, studentid)
		requests.put(url, params = params)
				
def main():

	course = int(raw_input("SIS ID: "))	
	# alternative batch change: courses = [int(x) for x in raw_input("List of SIS IDs: ").split(", ")]
	# and build 'for' loop below
	
	students = get_students(course, params)

	for sisid in students:
		for channel in get_channels(sisid, params):
			print sisid + "   :    " + channel
			adjust_notifs(sisid, channel)

