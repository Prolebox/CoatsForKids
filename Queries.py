#!python3.10
#Ethan Suhr 2022
import sqlite3 as sql
##### Inventory Menubar #####
#Add the allowed type and size of inventory items to be used
#in populating the comboboxes in the add inventory window.


def Add_School(school):
	if school != '':
		with sql.connect('CoatsDB') as con:
			cur = con.cursor()
			#cur.execute("insert into Schools (School_Name) values ('test');")
			cur.execute('select School_Name from Schools where School_Name = (?);', (school,))
			if cur.fetchall() == []:
				cur.execute("""
					insert into Schools (School_Name)
					values(?);
				""", (school,))
			else:
				return 'school exists'
		con.close()
	else:
		return 'empty'

def Add_Item(name, type='', size=''):
	#Check which item is being added and set variables for the sql query
	if name in ['Boots','Coat','Gloves'] and type and size != '':
		item_type = name+'_Type'
		item_size = name+'_Size'
		values = (name+'_Type',name+'_Size')
		with sql.connect('CoatsDB') as con:
			cur = con.cursor()
			#Using %s substitution because table and column names cannot be parameterized
			#Check if the item exists, if not add it to the database
			cur.execute('select %s, %s from %s where %s = (?) and %s = (?);' % (item_type, item_size, name, item_type, item_size), (type, size))
			if cur.fetchall() == []:
				cur.execute("""
					insert into %s %s
					values (?,?);
				""" % (name, values), (type, size))
			else:
				return 'item exists'
		con.close()
	#Separate because no size column in these tables
	#type must be passed as a tuple
	elif name in ['Socks','Hat'] and type != '':
		item_type = (name+'_Type')
		with sql.connect('CoatsDB') as con:
			cur = con.cursor()
			cur.execute('select %s from %s where %s = (?);' % (item_type, name, item_type), (type,))
			#If the result is an empty list then the item doesn't exist. Go ahead and add it
			if cur.fetchall() == []:
				cur.execute("""
					insert into %s (%s)
					values (?);
				""" % (name, item_type), (type,))
			else:
				return 'item exists'
		con.close()
	else:
		return 'empty'



#Remove Items from the database
def Remove_Item(name, type='', size=''):
	#Check which item is being added and set variables for the sql query
	if name in ['Boots','Coat','Gloves']:
		item_type = name+'_Type'
		item_size = name+'_Size'
		with sql.connect('CoatsDB') as con:
			cur = con.cursor()
			cur.execute("""
				delete from %s
				where %s = (?) and %s = (?);
			""" % (name, item_type, item_size), (type, size))
		con.close()
	elif name in ['Socks','Hat']:
		item_type = name+'_Type'
		with sql.connect('CoatsDB') as con:
			cur = con.cursor()
			cur.execute("""
				delete from %s
				where %s = (?);
			""" % (name, item_type), (type,))
		con.close()

def Remove_School(school):
	with sql.connect('CoatsDB') as con:
		cur = con.cursor()
		cur.execute("""
			delete from Schools
			where School_Name = (?);
		""", (school,))
	con.close()


def Grab_Schools():
	with sql.connect('CoatsDB') as con:
		cur = con.cursor()
		cur.execute("select School_Name from Schools;")
		schools = cur.fetchall()
		return schools
	con.close()

#Grab all unique values from type column
def Grab_Item_Types(name):
	with sql.connect('CoatsDB') as con:
		cur = con.cursor()
		cur.execute("""
			select distinct %s
			from %s;
		""" % (name+'_Type',name))
		types = cur.fetchall()
		return types
	con.close()

#Grab all unique values from size column
def Grab_Item_Sizes(name, type):
	with sql.connect('CoatsDB') as con:
		cur = con.cursor()
		cur.execute("""
			select %s
			from %s where %s = (?);
		""" % (name+'_Size', name, name+'_Type'), (type,))
		sizes = cur.fetchall()
		return sizes
	con.close()

#cur.execute('Select Coat_Size from Coat where Coat_Type = "A";')


#Add inventory item(s) to the inventory tables.
#Needs to be redone
def Add_Inventory_Record(name, type, size=''):

	try:
		con = sql.connect('CoatsDB')
		cur = con.cursor()
		cur.execute("""
			insert into Boots (boot_type, boot_size)
			values (?,?);
			""", (type, size))
		con.commit()
		con.close()
	except:
		print('ERROR: Failure adding item to database')
		quit()
