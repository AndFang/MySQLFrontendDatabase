# python -m pip install mysql-connector-python

import mysql.connector

# runs main control for database options
def main():
	# connects to the database using given creditals
	cnx = mysql.connector.connect(user='root', password='',
	                              host='localhost',
	                              database='project1')
	cursor = cnx.cursor()
	# successfully connects to the database
	print("Welcome to the company database!")
	
	# opt is current input choice of user
	opt = ""
	# opts is a list of function pointers to each option
	opts = [opt0, opt1, opt2, opt3, opt4, opt5, opt6, opt7, opt8, opt9, opt10, opt11]

	# while the input != 0 meaning they don't exit
	while (opt != "0"):
		# prints out the avaliable options
		options()
		# gets the input of the user
		opt = input("Number for desired option: ")
		# makes sure that the input is valid. If not makes them put in a valid input
		while (not (opt.isnumeric() and (0 <= int(opt) <= 11))):
			opt = input("ERROR! Enter valid option: ")
		# line 30 and 33 used to provide readability
		print("-" * 50)
		# calls the function that corresponds to the users input
		opts[int(opt)](cnx, cursor)
		print("-" * 50)
	# terminates the program
	print("Goodbye")

# prints the options avaliable to the user
def options():
	print()
	print("OPTIONS")
	print("(1) Add new employee")
	print("(2) View employee")
	print("(3) Modify employee")
	print("(4) Remove employee")
	print("(5) Add new dependent")
	print("(6) Remove dependent")
	print("(7) Add new department")
	print("(8) View department")
	print("(9) Remove department")
	print("(10) Add department location")
	print("(11) Remove department location")
	print("(0) Exit")
	print()

# message displayed after each option terminates
def finish():
	print("Finished operation!")
	exit = input("Press ENTER to return to OPTIONS")

# option for exiting the database
def opt0(cnx, cursor):
	print("Saving and exiting the database")
	cursor.close()
	cnx.close()

# option for adding a new employee
def opt1(cnx, cursor):
	print("ADD NEW EMPLOYEE\n")

	# takes in input for each of the field values of new employee
	fname = input("Enter first name: ")
	minit = input("Enter middle name: ")
	lname = input("Enter last name: ")
	ssn = input("Enter SSN: ")
	bdate = input("Enter birthday (YYYY-MM-DD): ")
	addr = input("Enter address: ")
	sex = input("Enter sex: ")
	sal = input("Enter salary: ")
	sssn = input("Enter supervisor's SSN: ")
	dno = input("Enter department number: ")
	print()
	# sql query to add new employee
	query = ("INSERT INTO EMPLOYEE "
		"(Fname, Minit, Lname, Ssn, Bdate, Address, Sex, Salary, Super_ssn, Dno) " 
		"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
	# tries to add employee
	try:
		# if successfully adds employee
		cursor.execute(query, [fname, minit, lname, ssn, bdate, addr, sex, sal, sssn, dno])
		print("Successfully added employee!\n")
	except mysql.connector.errors.DataError:
		# if error with input
		print("ERROR! Input invalid. Cannot create new employee.\n")
	except mysql.connector.errors.IntegrityError:
		# if error in regard to keys 
		print("ERROR! Input violates uniquess and minimality. Cannot create new employee.\n")

	# saves changes to database
	cnx.commit()

	# exits the option
	finish()

# option for viewing employee
def opt2(cnx, cursor):
	print("VIEW EMPLOYEE\n")

	# takes in ssn of employee to be viewed
	ssn = input("Enter SSN of employee: ")
	# sql query to view employee
	query = ("SELECT E.Fname, E.Minit, E.Lname, E.Ssn, E.Bdate, E.Address, E.Sex, E.Salary, E.Super_ssn, E.Dno, "
		"S.Fname, S.Minit, S.Lname, D.Dname, COUNT(L.Dependent_name) FROM (((EMPLOYEE AS E JOIN EMPLOYEE AS S ON E.Super_ssn = S.Ssn) "
		"JOIN DEPARTMENT AS D ON E.Dno = D.Dnumber) JOIN DEPENDENT AS L ON E.Ssn = L.Essn) WHERE E.Ssn = %s")
	# executes the query
	cursor.execute(query, [ssn])
	results = cursor.fetchall()
	# employee with given ssn cannot be found
	if (len(results) == 0 or results[0][0] == None):
		print("ERROR! Employee with SSN of", ssn, "cannot be found.\n")
		finish()
		return
	# prints out data of employee
	results = results[0]
	print()
	print("Name: \t\t\t{} {} {}".format(results[0], results[1], results[2]))
	print("SSN: \t\t\t{}". format(results[3]));
	print("Birthday: \t\t{:%d %b %Y}".format(results[4]))
	print("Address: \t\t{}".format(results[5]))
	print("Sex: \t\t\t{}".format(results[6]))
	print("Salary: \t\t{}".format(results[7]))
	print("Super SSN: \t\t{}".format(results[8]))
	print("Department Number: \t{}".format(results[9]))
	print("Supervisor Name: \t{} {} {}".format(results[10], results[11], results[12]))
	print("Department Name: \t{}".format(results[13]))
	print("Number of Dependents: \t{}".format(results[14]))
	print()

	# exits the option
	finish()

# option for modifying employee
def opt3(cnx, cursor):
	print("MODIFY EMPLOYEE\n")

	# takes in ssn of employee to be modified
	ssn = input("Enter SSN of employee: ")
	# sql query to view employee
	query = ("SELECT Fname, Minit, Lname, Ssn, Bdate, Address, Sex, Salary, Super_ssn, Dno "
		"FROM EMPLOYEE WHERE Ssn = %s FOR SHARE")
	# executes the query
	cursor.execute(query, [ssn])
	results = cursor.fetchall()
	# employee with given ssn cannot be found
	if (len(results) == 0):
		print("ERROR! Employee with SSN of", ssn, "cannot be found.\n")
		finish()
		return
	# prints out data of employee
	results = results[0]
	print()
	print("Name: \t\t\t{} {} {}".format(results[0], results[1], results[2]))
	print("SSN: \t\t\t{}". format(results[3]));
	print("Birthday: \t\t{:%d %b %Y}".format(results[4]))
	print("Address: \t\t{}".format(results[5]))
	print("Sex: \t\t\t{}".format(results[6]))
	print("Salary: \t\t{}".format(results[7]))
	print("Super SSN: \t\t{}".format(results[8]))
	print("Department Number: \t{}".format(results[9]))
	print()
	# prints out fileds to modify
	print("Select field to update")
	print("(1) Address")
	print("(2) Sex")
	print("(3) Salary")
	print("(4) Super SSN")
	print("(5) Department Number")
	print()

	# list of function pointers to each option
	opts = [opt3a, opt3b, opt3c, opt3d, opt3e]
	# gets input option of the user
	opt = input("Number for desired option: ")
	# makes sure that the input is valid. If not makes them put in a valid input
	while (not (opt.isnumeric() and (1 <= int(opt) <= 5))):
		opt = input("ERROR! Enter valid option: ")
	# calls the function that corresponds to the users input
	opts[int(opt) - 1](cnx, cursor, ssn)

	# saves changes to database
	cnx.commit()

	# exits the option
	finish()

# option to update address
def opt3a(cnx, cursor, ssn):
	addr = input("Enter new address: ")
	query = ("UPDATE EMPLOYEE SET Address = %s WHERE Ssn = %s")
	try:
		cursor.execute(query, [addr, ssn])
		print("Successfully updated employee!\n")
	except mysql.connector.errors.DatabaseError:
		print("ERROR! Invalid input.\n")

# option to update sex
def opt3b(cnx, cursor, ssn):
	sex = input("Enter new sex: ")
	query = ("UPDATE EMPLOYEE SET Sex = %s WHERE Ssn = %s")
	try:
		cursor.execute(query, [sex, ssn])
		print("Successfully updated employee!\n")
	except mysql.connector.errors.DatabaseError:
		print("ERROR! Invalid input.\n")

# option to update salary
def opt3c(cnx, cursor, ssn):
	sal = input("Enter new salary: ")
	query = ("UPDATE EMPLOYEE SET Salary = %s WHERE Ssn = %s")
	try:
		cursor.execute(query, [sal, ssn])
		print("Successfully updated employee!\n")
	except mysql.connector.errors.DatabaseError:
		print("ERROR! Invalid input.\n")

# option to update supervisor ssn
def opt3d(cnx, cursor, ssn):
	sssn = input("Enter new supper SSN: ")
	query = ("UPDATE EMPLOYEE SET Super_ssn = %s WHERE Ssn = %s")
	try:
		cursor.execute(query, [sssn, ssn])
		print("Successfully updated employee!\n")
	except mysql.connector.errors.DatabaseError:
		print("ERROR! Invalid input.\n")
	except mysql.connector.errors.IntegrityError:
		print("ERROR! Integrity error.\n")

# option to update department number
def opt3e(cnx, cursor, ssn):
	dno = input("Enter new department number: ")
	query = ("UPDATE EMPLOYEE SET Dno = %s WHERE Ssn = %s")
	try:
		cursor.execute(query, [dno, ssn])
		print("Successfully updated employee!\n")
	except mysql.connector.errors.DatabaseError:
		print("ERROR! Invalid input.\n")
	except mysql.connector.errors.IntegrityError:
		print("ERROR! Integrity error.\n")

# option to remove employee
def opt4(cnx, cursor):
	print("REMOVE EMPLOYEE\n")

	# takes in ssn of employee to be removed
	ssn = input("Enter SSN of employee: ")
	# sql query to view employee
	query = ("SELECT * FROM EMPLOYEE WHERE Ssn = %s FOR SHARE")
	# executes the query
	cursor.execute(query, [ssn])
	results = cursor.fetchall()
	# employee with given ssn cannot be found
	if (len(results) == 0):
		print("ERROR! Employee with SSN of", ssn, "cannot be found.\n")
		finish()
		return
	# printes out data of employee
	results = results[0]
	print()
	print("Name: \t\t\t{} {} {}".format(results[0], results[1], results[2]))
	print("SSN: \t\t\t{}". format(results[3]))
	print("Birthday: \t\t{:%d %b %Y}".format(results[4]))
	print("Address: \t\t{}".format(results[5]))
	print("Sex: \t\t\t{}".format(results[6]))
	print("Salary: \t\t{}".format(results[7]))
	print("Super SSN: \t\t{}".format(results[8]))
	print("Department Number: \t{}".format(results[9]))
	print()
	# makes sure that user wants to delete employee
	ans = input("Are you sure you want to delete this employee? (Y/N): ")
	while (ans != "Y" and ans != "N"):
		ans = input("ERROR! Invalid input. Plese try again (Y/N): ")
	
	# actions depending on input
	if (ans == "Y"):
		query = ("DELETE FROM EMPLOYEE WHERE Ssn = %s")
		try:
			cursor.execute(query,[ssn])
			print("Successfully removed employee!\n")
		except:
			print("ERROR! Employee cannot be removed due to dependencies.\n")
	else:
		print("Option aborted.\n")

	# saves changes to database
	cnx.commit()

	# exits the option
	finish()

# option to add new dependent
def opt5(cnx, cursor):
	print("ADD NEW DEPENDENT\n")

	# takes in ssn of employee to add dependent to
	ssn = input("Enter SSN of employee: ")
	# sql query to view dependents
	query = ("SELECT * FROM DEPENDENT WHERE Essn = (SELECT Ssn FROM EMPLOYEE WHERE Ssn = %s FOR SHARE) FOR SHARE")
	# executs the query
	cursor.execute(query, [ssn])
	results = cursor.fetchall()
	# prints out dependent data for employee with given ssn
	print("Dependents for employee with SSN", ssn)
	for i in results:
		print("- {} {} ({}) with birthday {:%d %b %Y}".format(i[4], i[1], i[2], i[3]))
	print()

	# takes in data for new dependent
	name = input("Enter name of new dependent: ")
	sex = input("Enter sex of new dependent: ")
	bdate = input("Enter birthday of new dependent (YYYY-MM-DD): ")
	ship = input("Enter relationship of new dependent: ")
	# sql query to add dependent
	query = ("INSERT INTO DEPENDENT (Essn, Dependent_name, Sex, Bdate, Relationship) VALUES (%s, %s, %s, %s, %s)")
	try:
		# if succesffully adds new dependent
		cursor.execute(query, [ssn, name, sex, bdate, ship])
		print("Successfully added new dependent!\n")
	except mysql.connector.errors.IntegrityError:
		# if error with input
		print("ERROR! Input already in use. Cannot add new dependent.\n")
	except mysql.connector.errors.DataError:
		# if error with input
		print("ERROR! Input invalid.\n")

	# saves changes to database
	cnx.commit()

	# exits the option
	finish()

# option for removing dependent
def opt6(cnx, cursor):
	print("REMOVE DEPENDENT\n")

	# takes in ssn of employee to remove dependent from
	ssn = input("Enter SSN of employee: ")
	# sql query to view dependents
	query = ("SELECT * FROM DEPENDENT WHERE Essn = (SELECT Ssn FROM EMPLOYEE WHERE Ssn = %s FOR SHARE) FOR SHARE")
	# executs the query
	cursor.execute(query, [ssn])
	results = cursor.fetchall()
	# no dependents for employee with given ssn
	if (len(results) == 0):
		print("ERROR! Dependents for employee with SSN of", ssn, "cannot be found.\n")
		finish()
		return
	# prints out dependent data for employee with given ssn
	print("Dependents for employee with SSN", results[0][0])
	for i in results:
		print("- {} {} ({}) with birthday {:%d %b %Y}".format(i[4], i[1], i[2], i[3]))
	print()

	# takes in name of dependent to remove
	name = input("Enter name of dependent to be removed: ")
	query = ("SELECT * FROM DEPENDENT WHERE Dependent_name = %s")
	cursor.execute(query, [name])
	results = cursor.fetchall()
	if (len(results) == 0):
		# if name of dependent is invalid
		print("ERROR! No dependent with given input.\n")
	else:
		# removes dependent with given name
		query = ("DELETE FROM DEPENDENT WHERE Dependent_name = %s")
		cursor.execute(query, [name])
		print("Successfully removed dependenet!\n")

	# saves changes to database
	cnx.commit()

	# exits the option
	finish()

# option to add new department
def opt7(cnx, cursor):
	print("ADD NEW DEPARTMENT\n")

	# takes in input for each of the field values of new department
	dname = input("Enter department name: ")
	dnum = input("Enter department number: ")
	mgrssn = input("Enter manager SSN: ")
	mgrsd = input("Enter manager start date (YYYY-MM-DD): ")
	print()
	# sql query to add new department
	query = ("INSERT INTO DEPARTMENT "
		"(Dname, Dnumber, Mgr_ssn, Mgr_start_date) " 
		"VALUES (%s, %s, %s, %s)")

	try:
		# if succesfully adds department
		cursor.execute(query, [dname, dnum, mgrssn, mgrsd])
		print("Successfully added department!\n")
	except mysql.connector.errors.DataError:
		# if error with input
		print("ERROR! Input invalid. Cannot create new department.\n")
	except mysql.connector.errors.IntegrityError:
		# if error in regard to keys
		print("ERROR! Input violates uniquess and minimality. Cannot create new department.\n")
	except mysql.connector.errors.DatabaseError:
		print("ERROR! Invalid input.\n")

	# saves changes to database
	cnx.commit()

	# exits the option
	finish()

# option for viewing department
def opt8(cnx, cursor):
	print("VIEW DEPARTMENT\n")

	# takes in department number 
	dno = input("Enter department number: ")
	# sql query to view department
	query = ("SELECT D.Dname, D.Dnumber, D.Mgr_ssn, D.Mgr_start_date, E.Fname, E.Minit , E.Lname, L.Dlocation "
		"FROM ((DEPARTMENT AS D LEFT JOIN EMPLOYEE AS E ON D.Mgr_ssn = E.Ssn) LEFT JOIN DEPT_LOCATIONS AS L ON D.Dnumber = L.Dnumber) "
		"WHERE D.Dnumber = %s")
	# executes the query
	cursor.execute(query, [dno])
	results = cursor.fetchall()
	# department with given number cannot be found
	if (len(results) == 0):
		print("ERROR! Department with number", dno, "cannot be found.\n")
		finish()
		return
	print()
	# prints out data of department
	print("Name: \t\t\t{}".format(results[0][0]))
	print("Number: \t\t{}". format(results[0][1]));
	print("Manager SSN: \t\t{}".format(results[0][2]))
	print("Manager Start Date: \t{:%d %b %Y}".format(results[0][3]))
	print("Manager Name: \t\t{} {} {}".format(results[0][4], results[0][5], results[0][6]))
	locs = ""
	for i in results:
		if (i[7]):
			locs += i[7] + ", "
	print("Location: \t\t{}".format(locs[:-2]))
	print()

	# exits the option
	finish()

# option to remove department
def opt9(cnx, cursor):
	print("REMOVE DEPARTMENT\n")

	# takes in department number
	dno = input("Enter department number: ")
	# sql query to view department
	query = ("SELECT * FROM DEPARTMENT WHERE Dnumber = %s FOR SHARE")
	# executes the query
	cursor.execute(query, [dno])
	# department with given number cannot be found
	results = cursor.fetchall()
	if (len(results) == 0):
		print("ERROR! Department with number", dno, "cannot be found.\n")
		finish()
		return
	# prints out data of department 
	results = results[0]
	print()
	print("Name: \t\t\t{}".format(results[0]))
	print("Number: \t\t{}". format(results[1]));
	print("Manager SSN: \t\t{}".format(results[2]))
	print("Manager Start Date: \t{:%d %b %Y}".format(results[3]))
	print()
	
	# makes sure that user wants to delete department
	ans = input("Are you sure you want to delete this department? (Y/N): ")
	while (ans != "Y" and ans != "N"):
		ans = input("ERROR! Invalid input. Plese try again (Y/N): ")

	# actions depending on input
	if (ans == "Y"):
		query = ("DELETE FROM DEPARTMENT WHERE Dnumber = %s")
		try:
			cursor.execute(query,[dno])
			print("Successfully removed department!\n")
		except:
			print("ERROR! Department cannot be removed due to dependencies.\n")
	else:
		print("Option aborted.\n")

	# saves changes to database
	cnx.commit()

	# exits the option
	finish()

# option to add department location
def opt10(cnx, cursor):
	print("ADD DEPARTMENT LOCATION\n")

	# takes in department number
	dno = input("Enter department number: ")
	# sql query to view department locations
	query = ("SELECT * FROM DEPT_LOCATIONS WHERE Dnumber = (SELECT Dnumber FROM DEPARTMENT WHERE Dnumber = %s FOR SHARE) FOR SHARE")
	# executes the query
	cursor.execute(query, [dno])
	results = cursor.fetchall()
	# prints out department locations
	print("Locations for department number", dno)
	for i in results:
		print("- {}".format(i[1]))
	print()

	# takes in values for new department location
	loc = input("Enter new department location: ")
	query = ("INSERT INTO DEPT_LOCATIONS (Dnumber, Dlocation) VALUES (%s, %s)")
	try:
		# if successfully adds department location
		cursor.execute(query, [dno, loc])
		print("Successfully added new department location!\n")
	except mysql.connector.errors.IntegrityError:
		# if error with input
		print("ERROR! Input location already in use.\n")
	except mysql.connector.errors.DataError:
		# if error with input
		print("ERROR! Input invalid.\n")

	# saves changes to database
	cnx.commit()

	# exits the option
	finish()

# option to remove department location
def opt11(cnx, cursor):
	print("REMOVE DEPARTMENT LOCATION\n")

	# takes in department number
	dno = input("Enter department number: ")
	# sql query to view department locations
	query = ("SELECT * FROM DEPT_LOCATIONS WHERE Dnumber = (SELECT Dnumber FROM DEPARTMENT WHERE Dnumber = %s FOR SHARE) FOR SHARE")
	# executes the query
	cursor.execute(query, [dno])
	results = cursor.fetchall()
	# no department locations with given department number
	if (len(results) == 0):
		print("ERROR! Department with number", dno, "cannot be found.\n")
		finish()
		return
	# prints out department locations
	print("Locations for department number", results[0][0])
	for i in results:
		print("- {}".format(i[1]))
	print()

	# takes in location of department location to remove
	loc = input("Enter department location to be removed: ")
	query = ("SELECT * FROM DEPT_LOCATIONS WHERE Dlocation = %s")
	cursor.execute(query, [loc])
	results = cursor.fetchall()
	if (len(results) == 0):
		# if location is invalid
		print("ERROR! No department location with given input.\n")
	else:
		# removes department location with given input
		query = ("DELETE FROM DEPT_LOCATIONS WHERE Dlocation = %s")
		cursor.execute(query, [loc])
		print("Successfully removed department location!\n")

	# saves changes to database
	cnx.commit()

	# exits the option
	finish()

# runs project
main()