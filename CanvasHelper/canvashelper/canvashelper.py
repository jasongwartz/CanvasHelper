#! /usr/bin/python
# Master Canvas API App

"""This app can select and run various other scripts to interact with the Canvas LMS API.
"""

import time, sys, os
import getstudentlist, makegroups, getgroupreport, adduser, notifications, changetimezone, scheduler
import getstudentenrollment, makeactiongroups, getallenrollments, getenrollmentwithgroups
import copycourse
import jgtools as jg

class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message.encode('utf-8', 'ignore'))

logger_filepath = jg.filedir().get()
sys.stdout = Logger(os.path.join(logger_filepath, "../../logs/log.txt"))
sys.stderr = Logger(os.path.join(logger_filepath, "../../logs/log.txt"))

def main():

	os.system("clear")
	print "\n\nWelcome to Jason's Canvas Helper!\nPress Ctrl-C at any time to quit.\n\nLoading...\n",
	time.sleep(1)

	global params 
	params = {}

	global login
	login = jg.oauth()
	params["access_token"] = login.token
	global url 
	url = login.url


	all_apps = {
#		"Settings: Batch Change Time Zone":changetimezone,
		"Course: Get Enrollment Report for Single Course":getstudentlist,
		"Groups: Get Printable Course Groups Report":getgroupreport,
		"Groups: Create and Assign Groups from CSV":makegroups,
		"Enrollment: Add a Single User Enrollment":adduser,
#		"Settings: Change Notification Preferences":notifications,
		"Course: Create Appointment Group (Scheduler)":scheduler,		#
#		"Enrollment: Get Course Enrollments per Student":getstudentenrollment,
#		"Action Project: Assign Groups and Sections for Action Project":makeactiongroups,
		"Course: Get Enrollment Reports for All Courses in a Term":getallenrollments,
		"Course: Get Enrollment Report for Single Course with Groups":getenrollmentwithgroups,
#		"Course: Create Courses and Copy from Template Shell":copycourse,
	}

	group_apps = {
		"Course: Get Enrollment Report for Single Course":getstudentlist,
		"Groups: Get Printable Course Groups Report":getgroupreport,
		"Groups: Create and Assign Groups from CSV":makegroups,
		"Course: Get Enrollment Reports for All Courses in a Term":getallenrollments,
		"Course: Get Enrollment Report for Single Course with Groups":getenrollmentwithgroups,	
	}

	

	print "\n1. Launch Groups tools \n2. Launch all tools"
	num = int(raw_input(">>> "))
	if num == 1:
		apps = group_apps
	elif num == 2:
		apps = all_apps
	else:
		sys.exit()

	print "\nWhich function would you like to perform?\n"
	
	app_list = sorted(apps.keys())
	
	for num, app in enumerate(app_list):
		print str(num) + ": " + app 
	
	choice = app_list[int(raw_input("\n>>> "))]
	
	apps[choice].url = url
	apps[choice].params = params
	apps[choice].main()

if __name__ == "__main__":

	main()

