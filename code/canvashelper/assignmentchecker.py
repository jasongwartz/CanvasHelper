import requests, json, os
import jgtools as jg
import getallenrollments
import datetime


def main():

	getallenrollments.params = params
	getallenrollments.url = url
	courses = getallenrollments.get_all_courses()
	
	to_write_lines = []
	modules_to_publish = {}
		# { course : {module : [item, item] } }
	
	for c in courses.items():

		#print "\n\nExamining course: " + c[0]
		assignments = requests.get(url + "/api/v1/courses/sis_course_id:%s/assignments" % c[1], params=params)
		
		assignments = assignments.json()
		
		for a in assignments:
			
			try:
				if not a['published']:
					x = "\nCourse: " + c[0] + ", Assignment: " + a['name'] + " not published."
					to_write_lines.append(x.encode('utf-8'))
					print x
				#print a['submission_types']
				if "none" in a['submission_types']:
					y = "\nCourse: " + c[0] + ", Assignment: " + a['name'] + " submission type is None."
					print y
					to_write_lines.append(y.encode('utf-8'))
			except KeyError:
				print a
	today = datetime.datetime.today().strftime("%d-%m-%Y")
	
	with open(os.path.join(jg.fileout().get(), 
				"assignmentchecker/%s.txt" % today), "w") as fp:
		for i in to_write_lines:
			fp.write(str(i))
