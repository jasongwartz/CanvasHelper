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

		print "\n\nExamining course: " + c[0]
		modules = requests.get(url + "/api/v1/courses/sis_course_id:%s/modules" % c[1], params=params)
		modules = modules.json()

		for module in modules:
			if not module['published']:
				x = "\nModule group: " + module['name']
				to_write_lines.append(x)
				
				if c[1] not in modules_to_publish:
					modules_to_publish[c[1]] = {module['id']:[]}
				else:
					modules_to_publish[c[1]][module['id']] = []
				print x
			
			submodules = requests.get(url + 
					"/api/v1/courses/sis_course_id:%s/modules/%s/items" 
					% (c[1], module["id"]), params=params)
			for m in submodules.json():
				if not m['published']:
					y = "\n" + m['title'] + ": NOT published."
					to_write_lines.append(y)
					if c[1] not in modules_to_publish:
						modules_to_publish[c[1]] = {}
					if module['id'] in modules_to_publish[c[1]]:
						modules_to_publish[c[1]][module['id']].append(m['id'])
					else:
						modules_to_publish[c[1]][module['id']] = [m['id']]
					print y
	
	today = datetime.datetime.today().strftime("%d-%m-%Y")
	
	with open(os.path.join(jg.fileout().get(), 
				"publisher/%s.txt" % today), "w") as fp:
		for i in to_write_lines:
			fp.write(str(i))

	print "\n\nPublish all unpublished modules and sub-items? Y for yes, any other key to quit."
	if raw_input(">>> ").lower() == "y":
		params['module[published]'] = True
		for course, modules in modules_to_publish.items():
			for module in modules.keys():
				r = requests.put(url + "/api/v1/courses/sis_course_id:%s/modules/%s"
					% (course, module), params = params)
				r = r.json()
				print r['name'] + ": published = " + str(r['published'])
			
				for item in modules[module]:
					r = requests.put(url + "/api/v1/courses/sis_course_id:%s/modules/%s/items/%s"
						% (course, module, item), params = params)
					r = r.json()
					try:
						print r['title'] + ": published = " + str(r['published'])
					except KeyError:
						print r