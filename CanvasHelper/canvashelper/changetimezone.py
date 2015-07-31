# Batch Change Time Zone

import requests
import getallenrollments as g

def get_student_list(courseid):	

	datalist = requests.get(url + "/api/v1/courses" \
		"/sis_course_id:%s/students" % courseid, params = params).json()

	studentlist = []
	for i in datalist:
		try:
			studentlist.append(i[u'sis_user_id'])
		except KeyError:
			pass
	return studentlist

def changetime(students): # students is a list of SIS IDs

	params["user[time_zone]"] = "London"
	for sis in students:
		requests.put(url + "/api/v1/users/sis_user_id:%s" \
			% sis, params = params)
		print "Student " + str(sis) + " completed."

def main():

	g.params = params
	g.url = url
	courses = g.get_all_courses()

	for name, sis in courses.items():
		print "\n\nWorking on: " + name
		students = get_student_list(sis)
		changetime(students)

