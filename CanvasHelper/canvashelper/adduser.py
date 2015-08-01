# Register TA

import requests
import json


def main():
	
	print "\n\nEnter the SIS ID of the course:"
	course_sis = raw_input(">>> ")
	print "Enter the SIS ID of the user to enroll:"
	user_sis = raw_input(">>> ")


	params["enrollment[user_id]"] = "sis_user_id:%s" % user_sis

	enrollment_types = [
		"StudentEnrollment",
		"TeacherEnrollment",
		"TaEnrollment",
		"ObserverEnrollment",
		"DesignerEnrollment"
		]

	for i, x in enumerate(enrollment_types):
		print str(i) + ": " + x

	
	params["enrollment[type]"] = enrollment_types[int(raw_input(">>> "))]
	params["enrollment[enrollment_state]"]="active"

	enroll = requests.post(url + \
		"/api/v1/courses/sis_course_id:%s/enrollments" % course_sis, params = params)
	enrolldata = enroll.json()

	if "200" in str(enroll):
		print "\n\nUser ID " + str(enrolldata['id']) + " successfully added to Course ID " \
			+ str(enrolldata['course_id']) + " with role " + enrolldata['type'] \
			+ ", current status: " + enrolldata['enrollment_state'] + "\n"
	else:
		print "\n\nAn error occured! Error code: " + str(enroll)
		print enrolldata
		print "\n"
