# Make groups

# &&& Make better comments/docstrings about each function!

import json, requests, csv, time, os
import jgtools as jg


def parse_teamdata(teamdata):
	all_students = []	
	for student in range(1, len(teamdata)):
	# Creates a dict of data for each student
	# eg. {"First Name":"Alfred", "Last Name":"Hitchcock"}, etc etc all fields	
		if teamdata[student][0] == '': continue # skips blank lines
		this_student = {}
		for x in range(0, len(teamdata[0])): # len(teamdata[0]) == # of columns in the sheet
			# Key = column's header		 :  value = cell value (column at student's line)
			this_student[teamdata[0][x]] = teamdata[student][x].replace("Group ", '')
		all_students.append(this_student)
	return all_students

def sort_groups(parsed_data):
	group_names = []
	
	print "Please type the header representing the chosen module:"
	header = raw_input(">>> ")
	print "Please type the header representing the SIS ID:"
	sis_header = raw_input(">>> ")
	
	for student in parsed_data:
		try:
			groupname = "Group %s" % int(student[header]) # evaluate if student[header] can be int
			if groupname not in group_names:
				group_names.append(groupname)
			student[header] = groupname

		except ValueError:
			if student[header] not in group_names:
				group_names.append(student[header])

	number_of_groups = len(group_names)

	# Creates a dict like ----- {"1": [], "2": []}
	groups = {i:[] for i in group_names if i != ''}
	for student in parsed_data:
		if student[header] != '' and student[sis_header] != '':
			groups[str(student[header])].append(student[sis_header])
				# groups dict looks like ---     {group #:[sisid, sisid, sisid]}
				# MAKE SURE that the field "SIS USER ID" matches the column header
		#except KeyError:
		#	print "Incorrect headers."
		#	sys.exit()
	return groups


def get_group_category(coursesis, params):
	
	while True:
		print "\nChoose the Group Category Name."
		print "1. Use the Course Name as the Group Category Name."
		print "2. Specify a Group Category Name.\n"
		choice = raw_input(">>> ")
		if choice == "1":
			params["name"] = requests.get(url + "/api/v1/courses/sis_course_id:%s" \
				% coursesis, params = params).json()[u'name'].split(" - ")[0] # Strips eg. LEM2
			break
		elif choice == "2":
			params["name"] = raw_input("Type the Group Category Name: ")
			break
		else:
			print "\nError!"
	try:
	# Attempts to create a group category with the correctly formatted name, returns ID.
		category_id = requests.post(url + "/api/v1/courses/sis_course_id:%s/group_categories" \
			% coursesis, params = params).json()['id']
		print "Created Group Category: " + params['name']
		return category_id
	except:
	# If a group category already exists with that name, returns the existing ID.
		all_categories = requests.get(url + "/api/v1/courses/sis_course_id:%s/group_categories" \
			% coursesis, params = params).json()
		print "Retrieved Group Category: " + params['name']

		for items in all_categories:
			if items[u'name'] == params['name']:
				category_id = items[u'id']
				return category_id

def create_groups(groupcategory, groups, params):
	# For each group category, loops through and creates the groups with given titles

	params["is_public"] = False
	params["join_level"] = "invitation_only"
	
	groupids = []
	
	for key in groups.keys():
		params["name"] = key

		print "Creating group: " + params['name']

		group_object = requests.post(url + "/api/v1/group_categories/%s/groups" \
			% groupcategory, params = params) ######.json()[u'id']
		
		print group_object
			
			## ESCALATE TO CANVAS - Error 504 every time ###########
			## ONCE RESOLVED, insert here: return groupids		
		
def assign_groups(groupcategory, groups, params):
	groupids = jg.api_list(url +"/api/v1/group_categories/%s/groups" \
		% groupcategory, params = params).call()
	groupids = {items['name'] : items['id'] for items in groupids}

	for name, group_id in groupids.items():
		for student in groups[name]:
			params["user_id"] = requests.get(url + "/api/v1/users" \
				"/sis_user_id:%s/profile" % student, params = params).json()['id']
			membership = requests.post(url + "/api/v1/groups/%s/memberships" \
				% group_id, params = params).json()
			print "\nStudent SIS ID " + str(student) + " added to Group " + name + \
				"/Group ID " + str(membership['group_id'])
			print "Membership ID: " + str(membership['id']) + ", status: " + membership['workflow_state']

def main():
	sis = raw_input("Enter the course SIS ID: ")
	
	teamlist = jg.dragfile().get()			# Reads the file, returns list of lines
	parsed_data = parse_teamdata(teamlist)	# Returns list of dicts of student data
	groups = sort_groups(parsed_data) 		# Returns dict {group names : [list of SIS IDs]}
	
	group_categories = get_group_category(sis, params)

	print "Group Category ID: " + str(group_categories)

	create_groups(group_categories, groups, params)
	time.sleep(30)
	assign_groups(group_categories, groups, params)

