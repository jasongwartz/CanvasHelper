# Retrieve enrollment list of one class

import requests, csv, os
import jgtools as jg
requests.packages.urllib3.disable_warnings()

def get_list(course, header):

	coursedetails = requests.get(url + "/api/v1/courses/sis_course_id:%s" % course, \
		params = params).json()
	
	coursename = coursedetails['name']
	term = coursedetails['enrollment_term_id']
	students = requests.get(url + "/api/v1/courses/sis_course_id:%s/students" \
		% course, params = params)
	students = students.json()

	outputlocation = jg.fileout().get()

	filename = os.path.join(outputlocation, "enrollmentlists/%s/%s-%s.csv" \
		 % ("TermID-"+str(term), coursename, course))
	dir = os.path.dirname(filename)

	if not os.path.isdir(dir):
		os.makedirs(dir)
	else:
		pass
	
	try:	
		with open(filename, "w") as fp:
				writer = csv.writer(fp)
				writer.writerow(["Name", "SIS User ID", header])
				for i in students:
					try:
						writer.writerow([i['name'].encode('utf-8', 'ignore'), \
							 i['sis_user_id'], ""])
					except KeyError:
						writer.writerow([i['name'].encode('utf-8', 'ignore'), \
							 "", ""])
				print "\nSuccessfully saved Course %s student list to %s.\n" % (course, filename)
	
	except TypeError:
		print students
		print "\nAn error occured, unable to retrieve student list.\n"	

def main():

	course = raw_input("Enter the course SIS ID: ")
	
	header = raw_input("Enter the module or term for the header: ")
	
	get_list(course, header)
	
