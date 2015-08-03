
import csv, requests, datetime, os
import jgtools as jg

def readfile():

	inputdata = jg.dragfile().get()

	header = raw_input("Type the header that denotes which campus: ")
	header_place = data[0].index(header)
	campus = raw_input("Type which campus is selected: ")
				
	campuslist = []
	
	for row in data:
		try:
			if row[header_place] == "London":
				campuslist.append(row)
		except:
			pass
	return campuslist

def get_courses(campuslist):
	today = datetime.datetime.now().strftime("%d-%y") 
	
	filename = os.path.join(jg.fileout().get(), 
		"studentenrollment/enrollmentreport_%s.csv" % today)
	with open(filename, "w") as fp:
		for students in campuslist:
			#header denote name/sis id
			params["as_user_id"] = "sis_user_id:%s" % students[3]
			user_courses = requests.get(url + "/api/v1/courses", \
				params=params).json()

			student_data = [students[0], students[1], students[3]]
			print "\n" + str(student_data)
			for i in user_courses:
				if i[u'enrollment_term_id'] == 6163: ##### CHANGE TO CORRECT TERM ID
					print i['name']
					student_data.append(i['name'])
			writer = csv.writer(fp)
			writer.writerow(student_data)

	print "\nFile saved to %s.\n" % filename

def main():
	campuslist = readfile()
	get_courses(campuslist)
