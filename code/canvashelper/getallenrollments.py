# Get enrolment for all courses in a term

import requests
import getstudentlist as g
import jgtools as jg

def get_all_courses():
	coursesid = int(raw_input("Please type the account ID of the account in which the courses are found: "))


	params["per_page"] = 100
	
	term = jg.terms(coursesid, url, params).choose()

	courses_url = url + "/api/v1/accounts/%s/courses" % coursesid

	all_courses = {}
	
	data = jg.api_list(courses_url, params).call()
	
	for course in data:
		if course['enrollment_term_id'] == term:
			all_courses[course['name']] = course['sis_course_id']

	return all_courses


def main():

	all_courses = get_all_courses()
	
	header = raw_input("Enter the module or term for the header: ")
	
	g.url = url		
	g.params = params
	for name, sis in all_courses.items():
		print "Pulling report for: " + name
		g.get_list(sis, header)
