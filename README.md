**CanvasHelper README.md**
======

About
------

CanvasHelper is a Python application which uses the Instructure Canvas LMS API to automate several functions in the Canvas LMS which are not included in the web app by default.

Current and future abilities of CanvasHelper include (italics for unstable/in development):

- Adding a user to a course without sending an invitation email
- Getting enrollment reports for individual classes or every class in a term 
- Creating groups and group categories, and allocating students into the groups.
- Creating Scheduler blocks of appointment groups for student self-signup
- Changing the time zone or other settings on behalf of a group of students (for campus rotation)
- *Creating copies of courses from a course shell template*
- *Changing notification preferences for students' communcation channels*
- *Getting a per-student list of enrolled courses*

CanvasHelper has been developed for and on OS X. That's not to say that other platforms won't work - just that I haven't tried them.


Installation
------
*Note: This will install pip (the python package management system) and run the setup.py 
script to install the required python packages and create the executable, as well 
as creating a shortcut in `/Applications`.*

### Automator installer:

1.	Move the CanvasHelper code folder to the directory in which you'd like to store it.
2.	Double-click the setup.app application to launch the installer.
3.	Click OK to confirm, then navigate to the directory where you put the code files.
4.	Wait for the install process to complete.
5.	Launch the script from `/Applications` (app name `CanvasHelper.command`)

### Command Line installer:

1.	Move the CanvasHelper code folder to the directory in which you'd like to store it.
2.	cd into that directory.
3.	Type `sudo -H ./setup.sh` and hit return. Enter your password at the prompt.




Authentication
------

### Users

The first time it is launched, CanvasHelper will prompt you to create and save your
API access tokens. When you provide the website endpoint (which must be HTTPS, 
e.g. https://example.test.instructure.com), a browser page will launch and ask for authorisation.
After authorisation is approved, you will be redirected back to your Canvas main page, but
with a long 'code' string in the URL. Copy this entire URL back into CanvasHelper, and
your API token will be retrieved and saved for future use.

API access only needs to be authorised once, unless the tokens are revoked from the Canvas
settings page. If you need to delete your saved tokens
from CanvasHelper, or need to add new tokens, simply delete the file titled `sensitive.json`
from the code folder, and upon next launch, CanvasHelper will prompt you to enter API tokens.

### Developer Key
If you're an institution that wants to use this software and don't have access to a devkey, feel free to send me a message to ask for use of mine. Developers will need to request a devkey from Instructure. 
You'll need to create a `devkey.json` file in the `code/canvashelper` folder, with the following data:
```json
{"client_id":YOUR_CLIENT_ID, "client_secret":YOUR_CLIENT_SECRET}
```


Usage
-----

Double-click CanvasHelper.command in `/Applications` to launch the script.

The script can also be launched from the command line by changing into the 
`CanvasHelper/CanvasHelper/` directory and running

	python canvashelper.py

Any scripts that output data, usually in .csv spreadsheet format, will be saved in the
`CanvasHelper/output` folder.


----------------------------

Functionality
-----

<table border = 1, style="width:100%">
	<tr>
		<th>Function</th>
		<th>Description</th>
	<tr>
		<td>Add a Single User Enrollment</td>
		<td>Add a single student, TA, etc. to a single course without sending an invitation.</td>
	</tr>
	<tr>
		<td>Get Printable Course Groups Report</td>
		<td>Pulls a printable, easy to read report for all groups in a course in a spreadsheet.</td>
	</tr>
	<tr>
		<td>Get Enrollment Report for Single Course</td>
		<td>Pulls an list of all students in a course, with an empty column (for adding group name/number).</td>
	</tr>
	<tr>
		<td>Create and Assign Groups from CSV</td>
		<td>Using a CSV input in the same format as the Get Enrollment Report, creates a group category, creates all the groups, and assigns students into groups.</td>
	</tr>
	<tr>
		<td>Get Enrollment Report for Single Course with Groups</td>
		<td>Using the same format as the Enrollment Report (not as easy to read when printed), pulls a report but with the Group column already filled in.</td>
	</tr>
	<tr>
		<td>Get Enrollment Reports for All Courses in a Term</td>
		<td>Provides a list of terms and asks for a choice, then performs the "Get Enrollment Report" operation for all courses in the chosen term.</td>
	</tr>
	<tr>
		<td>Create Appointment Group (Scheduler)</td>
		<td>Allows easy creation of Scheduler time slots based on CSV input, which makes it possible to include breaks in the Scheduler.</td>
	</tr>
</table>

Example CSV Layouts
-----

*Note: The CSV layouts for input are inflexible. Notably, some must include headers and some cannot include them. __If you're using Excel on a Mac, you must format the files as 'Windows Comma Seperated', otherwise you'll encounter a 'newline' error.__ Many/most of the existing bugs are related to formatting of the CSV inputs. If you find any, let me know about them!*

### Enrollment Report  
>	*Includes and requires a header*

<table border = 1, style="width:100%">
	<tr>
		<th>Name</th>
		<th>SIS User ID</th>
		<th><em>Group/Module</em></th>
	</tr>
	<tr>
		<td>James Bond</td>
		<td>007007</td>
		<td>Group 6</td>
	</tr>
	<tr>
		<td>Alec Trevelyan</td>
		<td>006006</td>
		<td>Group 6</td>
	</tr>
</table>

Note: __*Group/Module*__ header will be generated when pulling an enrollment report. When pulling an Enrollment Report with Groups, the header will be labelled __Group__.  
For uploading, the __Create and Assign Groups from CSV__ script will ask for the header of the column which represents SIS ID and the header of the column which represents the group name or number. These must be typed exactly as they appear in the CSV.

### Printable Course Group Report
>	*Does not include a header*

<table border = 1, style="width:100%">
	<tr>
		<td>Group 1</td>
		<td>James Bond</td>
		<td>Alec Trevelyan</td>
	</tr>
	<tr>
		<td></td>
		<td>007007</td>
		<td>006006</td>
	</tr>
	<tr>
		<td></td>
		<td>james.bond@instructure.com</td>
		<td>alec.trevelyan@instructure.com</td>
	</tr>
	<tr></tr>
	<tr>
		<td>Group 2</td>
		<td>Indiana Jones</td>
		<td>Henry Jones, Sr.</td>
	</tr>
	<tr>
		<td></td>
		<td>0010001</td>
		<td>191919</td>
	</tr>
	<tr>
		<td></td>
		<td>indiana.jones@instructure.com</td>
		<td>henry.jones@instructure.com</td>
	</tr>		
</table>

Note: As you can see, the formatting is not ideally suited for a script to parse through, but is much easier to see visually. This makes it suited for printing reports for instructors if they prefer a printed copy over viewing the groups from within Canvas.

### Scheduler
>	*Does not include a header*

<table border = 1, style="width:100%">
	<tr>
	<tr>
		<td>Scheduler Event 1</td>
		<td>25/07/2015</td>
		<td>9:00</td>
		<td>9:45</td>
		<td>EST</td>
		<td>course_sis_id</td>
	</tr>
	<tr>
		<td>Scheduler Event 2</td>
		<td>25/07/2015</td>
		<td>10:00</td>
		<td>10:45</td>
		<td>EST</td>
		<td>course_sis_id</td>
	</tr>
	<tr>
		<td>Scheduler Event 2</td>
		<td>25/07/2015</td>
		<td>13:00</td>
		<td>13:45</td>
		<td>EST</td>
		<td>course_sis_id</td>
	</tr>
	<tr>
		<td>Scheduler Event 2</td>
		<td>25/07/2015</td>
		<td>14:00</td>
		<td>14:45</td>
		<td>EST</td>
		<td>course_sis_id</td>
	</tr>
</table>

The row layout is as follows:  
> Event Title | Date | Start Time | End Time | Time Zone | Course SIS ID |

Note: The script will sort the events by title, assigning them into one Scheduler group. It will prompt you for max participants per slot, and the max and min slots a student may sign up for. It will also ask whether or not to publish the events immediately.

----------------------------

Development Details
------

### Folder Structure

	├── root
	|   ├── CanvasHelper
		|	├── canvashelper
				├── python script files
			├── get-pip.py
			├── main.py
			├── setup.py
			└── setup.sh
		├── README.md
		├── logs
		├── output
		└── setup.app

The main script files are kept in the `/CanvasHelper/canvashelper` folder. Diagnostic or troubleshooting 
logs can be found in `/logs`, and any scripts that output data will put 
their files (usually CSV format) in `/output`.


### Credits
Designed and developed by [Jason Gwartz](https://www.github.com/jasongwartz) while at [Hult International Business School](http://www.hult.edu).
The Canvas API documentation can be found [here](https://canvas.instructure.com/doc/api/).

------------


README Changelog:
-	31/07/2015: Adjusted folder structure to match new folder setup. Moved readme to root directory so it shows on Github preview.
-	29/07/2015: Added Functionality list and example CSV layouts. Added better formatting for code.
-	29/07/2015: Version 1
