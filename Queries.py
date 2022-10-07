#!python3.10
#Ethan Suhr 2022
#This file is for all the database queries needed to populate the application
import sqlite3 as sql

## View Inventory Window ##
def Total_Item_Count(item):
	values = item+'_Inventory'
	with sql.connect('CoatsDB') as con:
		cur = con.cursor()
		cur.execute("""
			select count(*) as count from %s;
		""" % values)
		return cur.fetchall()
	con.close()

#Return each subitem and the amount of that item
def Total_Subitems_Count(name):
	#Dictionary to be returned containing item : count
	items_with_count = {}
	item_type = name+'_Type'
	item_size = name+'_Size'
	table_name = name+'_Inventory'

	with sql.connect('CoatsDB') as con:
		if name in ['Boots','Coats','Gloves']:
			cur = con.cursor()
			cur.execute("""
				select distinct %s, %s
				from %s;
			""" % (item_type, item_size, table_name))
			#Grab distinct items added to inventory table to then grab count
			subitems = cur.fetchall()

			#Grab the inventory count for each subitem
			for i in range(len(subitems)):
				type, size = subitems[i]
				cur.execute("""
					select %s, %s
					from %s
					where %s = (?) and %s = (?);
				""" % (item_type, item_size, table_name, item_type, item_size), (type, size))

				subitem_count = len(cur.fetchall())
				items_with_count[type,size] = subitem_count

		elif name in ['Socks','Hats']:
			cur = con.cursor()
			cur.execute("""
				select distinct %s
				from %s;
			""" % (item_type, table_name))
			#Grab distinct items added to inventory table to then grab count
			subitems = cur.fetchall()

			for type in subitems:
				cur.execute("""
					select %s
					from %s
					where %s = (?);
				""" % (item_type, table_name, item_type), (type))

				subitem_count = len(cur.fetchall())
				items_with_count[type] = subitem_count

		return items_with_count
	con.close()

## Remove Inventory Window ##
def Remove_Inventory_Record(name, type, size='', amount=''):
	item_type = name+'_Type'
	item_size = name+'_Size'
	table_name = name+'_Inventory'

	if name in ['Boots','Coats','Gloves']:
		with sql.connect('CoatsDB') as con:
			cur = con.cursor()
			cur.execute("""
				delete from %s
				where %s = (?) and %s = (?)
				limit ?;
			""" % (table_name, item_type, item_size), (type, size, amount))
		con.close()

	elif name in ['Socks','Hats'] and type != '':
		with sql.connect('CoatsDB') as con:
			cur = con.cursor()
			cur.execute("""
					delete from %s
					where %s = (?)
					limit ?;
			""" % (table_name, item_type), (type, amount))
		con.close()

## Add Inventory Window##
def Add_Inventory_Record(name, type, size='', amount=''):
	item_type = name+'_Type'
	item_size = name+'_Size'
	table_name = name+'_Inventory'
	i = 0

	if name in ['Boots','Coats','Gloves']:
		with sql.connect('CoatsDB') as con:
			cur = con.cursor()
			while(i < int(amount)):
				cur.execute("""
					insert into %s (%s, %s)
					values (?,?);
				""" % (table_name, item_type, item_size), (type, size))
				i += 1
		con.close()

	elif name in ['Socks','Hats'] and type != '':
		with sql.connect('CoatsDB') as con:
			cur = con.cursor()
			while(i < int(amount)):
				cur.execute("""
					insert into %s (%s)
					values (?);
				""" % (table_name, item_type), (type,))
				i += 1
		con.close()


## Items Window ##
def Remove_Item(name, type='', size=''):
	item_type = name+'_Type'
	item_size = name+'_Size'
	#Check which item is being added and set variables for the sql query
	if name in ['Boots','Coats','Gloves']:
		with sql.connect('CoatsDB') as con:
			cur = con.cursor()
			cur.execute("""
				delete from %s
				where %s = (?) and %s = (?);
			""" % (name, item_type, item_size), (type, size))
		con.close()
	elif name in ['Socks','Hats']:
		with sql.connect('CoatsDB') as con:
			cur = con.cursor()
			cur.execute("""
				delete from %s
				where %s = (?);
			""" % (name, item_type), (type,))
		con.close()

def Add_Item(name, type='', size=''):
	item_type = name+'_Type'
	item_size = name+'_Size'
	#Check which item is being added and set variables for the sql query
	if name in ['Boots','Coats','Gloves'] and type and size != '':
		with sql.connect('CoatsDB') as con:
			cur = con.cursor()
			#Using %s substitution because table and column names cannot be parameterized
			#Check if the item exists, if not add it to the database
			cur.execute('select %s, %s from %s where %s = (?) and %s = (?);' % (item_type, item_size, name, item_type, item_size), (type, size))
			if cur.fetchall() == []:
				cur.execute("""
					insert into %s (%s, %s)
					values (?,?);
				""" % (name, item_type, item_size), (type, size))
			else:
				return 'item exists'
		con.close()
	#Separate because no size column in these tables
	#type must be passed as a tuple
	elif name in ['Socks','Hats'] and type != '':
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


## Schools Window ##
def Remove_School(school):
	with sql.connect('CoatsDB') as con:
		cur = con.cursor()
		cur.execute("""
			delete from Schools
			where School_Name = (?);
		""", (school,))
	con.close()

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


## Queries to update comboboxes ##
def Grab_Schools():
	with sql.connect('CoatsDB') as con:
		cur = con.cursor()
		cur.execute("select School_Name from Schools;")
		return cur.fetchall()
	con.close()

#Grab all unique values from type column, as the same type may have multiple sizes
def Grab_Item_Types(name):
	item_type = name+'_Type'
	table = name+'_Inventory'

	with sql.connect('CoatsDB') as con:
		cur = con.cursor()
		cur.execute("""
			select distinct %s
			from %s;
		""" % (item_type, table))
		types = cur.fetchall()
		return types
	con.close()

#Grab item size based upon preselected type
def Grab_Item_Sizes(name, type):
	item_type = name+'_Type'
	item_size = name+'_Size'

	with sql.connect('CoatsDB') as con:
		cur = con.cursor()
		cur.execute("""
			select %s
			from %s where %s = (?);
		""" % (item_size, name, item_type), (type,))
		return cur.fetchall()
	con.close()

#Used to populate comboboxes on Add Record window
def Populate_Add_Record_CBs(name):
	table_name = name+'_Inventory'
	item_type = name+'_Type'
	item_size = name+'_Size'

	if name in ['Boots','Coats','Gloves']:
		with sql.connect('CoatsDB') as con:
			cur = con.cursor()
			cur.execute("""
				select distinct %s, %s
				from %s;
			""" % (item_type, item_size, table_name))

			#Grab distinct items added to inventory table to then merge into one string
			subitems = cur.fetchall()
			inventory = []

			#Merge the type and size into one string
			for i in range(len(subitems)):
				type, size = subitems[i]
				inventory.append(type+', '+size)
			return inventory


	elif name in ['Socks','Hats']:
		with sql.connect('CoatsDB') as con:
			cur = con.cursor()
			cur.execute("""
				select distinct %s
				from %s;
			""" % (item_type, table_name))

			#Grab distinct items added to inventory table to then merge into one string
			subitems = cur.fetchall()
			inventory = []

			#Merge the type and size into one string
			for i in range(len(subitems)):
				type = subitems[i]
				inventory.append(type)
			return inventory
