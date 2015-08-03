# Create groups

import json, requests, csv, os
import jgtools as jg


def main():
	print "Enter the SIS IDs of each course, seperated by a comma and a space.\n" \
		"Eg. 7482, 4728, 5472"
	coursesisid = raw_input(">>> ").split(", ")
	
	params['per_page'] = 50
	
	for course in coursesisid:

		print "Processing..."

		group = requests.get(url + "/api/v1/courses/" \
			"sis_course_id:%s/groups" % course, params = params)
		print group
		group = group.json()
		
		
		for items in group:

			print items[u'name']
		
			students = requests.get(url + "/api/v1/groups/%s/users" \
				% items[u'id'], params = params).json()

			row = [items[u'name']]
			row2 = [""]
			row3 = [""]
			for student in students:
		
				print student[u'name'].encode('utf-8', 'ignore')
		
				row.append(student[u'name'].encode('utf-8', 'ignore'))
				row2.append(student[u'sis_user_id'])

				studentdata = requests.get(url + \
					"/api/v1/users/sis_user_id:%s/profile" % student[u'sis_user_id'], params = params).json()
				row3.append(studentdata[u'primary_email'])
	
			filename = os.path.join(jg.fileout().get(), 
				"groupreports/%s.csv" % course)

			with open(filename, "a") as fp:
				writer = csv.writer(fp)
				writer.writerow(row)
				writer.writerow(row2)
				writer.writerow(row3)
				writer.writerow(["", ""])

