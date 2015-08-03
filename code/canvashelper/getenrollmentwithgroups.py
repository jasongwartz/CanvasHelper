# Create groups

import json, requests, csv, os
import jgtools as jg

def main():
	print "Enter the SIS IDs of each course, seperated by a comma and a space.\n" \
		"Eg. 7482, 4728, 5472"
	coursesisid = raw_input(">>> ").split(", ")
	
	params['per_page'] = 100
	
	for course in coursesisid:

		print "Processing..."

		request = jg.api_list(url + "/api/v1/courses/" \
			"sis_course_id:%s/groups" % course, params = params)
		group = request.call()

		headers = ["Name", "SIS ID", "Email", "Group"]

		filename = os.path.join(jg.fileout().get(), "enrollmentlistswithgroups/%s.csv" % course)

		with open(filename, "a") as fp:
			writer = csv.writer(fp)
			writer.writerow(headers)
		
		
		for items in group:

			print items[u'name']
		
			students = requests.get(url + "/api/v1/groups/%s/users" \
				% items[u'id'], params = params).json()

			for student in students:
	
		
				print student[u'name']
					
				# pulls each student's primary contact email
			
				studentdata = requests.get(url + "/api/v1/" \
					"users/sis_user_id:%s/profile" % student[u'sis_user_id'], params = params).json()

				row = [student[u'name'].encode('utf-8', 'ignore'), student[u'sis_user_id'], \
					studentdata[u'primary_email'], items[u'name']]

	
				with open(filename, "a") as fp:
					writer = csv.writer(fp)
					writer.writerow(row)

			### ADDS A BLANK LINE BETWEEN EACH GROUP
			with open(filename, "a") as fp:
					writer = csv.writer(fp)
					writer.writerow([""])
