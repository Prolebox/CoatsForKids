#!python3.10
#Ethan Suhr 2022
#This file is for all the database queries needed to populate the application
import sqlite3 as sql

###################### View Inventory Window ######################
def Total_Item_Count(item):
	values = item+'_Inventory'
	with sql.connect('CoatsDB') as con:
		cur = con.cursor()
		cur.execute("""
			select count(*) as count from %s;
		""" % values)
		return cur.fetchall()
	con.close()

###################### Return each subitem and the amount of that item ######################
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

###################### Remove Inventory Window ######################
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

###################### Add Inventory Window ######################
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

###################### Items Window ######################
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

###################### Schools Window ######################
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

###################### Add Record Window ######################
def Add_Record(CFirst, CLast, CAge, Gender, School, PFirst, PLast, Phone, Street, City, Zip, Hat, Coat, Gloves, Socks, Boots):
	##### Add Record to Database #####
	#Combine entry boxes to test for empty values
	required_info = (CFirst, CLast, CAge, Gender, School, PFirst, PLast, Phone, Street, City, Zip)

    #Return empty to display notification window if required info missing
	if '' in required_info:
		return 'empty'
	else:
		with sql.connect('CoatsDB') as con:
			cur = con.cursor()
			cur.execute("""
				insert into Records (Child_First, Child_Last, Child_Age, Child_Gender, Child_School,
								Parent_First, Parent_Last, Parent_Phone, Parent_Street, Parent_City, Parent_Zip,
								Hat, Coat, Gloves, Socks, Boots)
				values (?, ?, ?, ?, ?,
						?, ?, ?, ?, ?, ?,
						?, ?, ?, ?, ?);
			""", (CFirst, CLast, CAge, Gender, School, PFirst, PLast, Phone, Street, City, Zip, Hat, Coat, Gloves, Socks, Boots))
	con.close()

	##### Delete corresponding items from inventory tables #####
    #List of items to split the type and size out of string, flter out empty items
	#type, size order: COAT, GLOVES, BOOTS
	type_size_items = [Coat, Gloves, Boots]

	#list of split types and sizes
	split_items = []
	#list of split item names to be used in table and variable names for deletion query
	split_items_names = []
	#Keep track of what item has been checked for already
	#This is to prevent all checks matching the first if statement if the types and sizes are the same between items
	i = 0

	for each in range(len(type_size_items)):
		if type_size_items[each] == Coat and type_size_items[each] != '' and i < 1:
			split_items.append(type_size_items[each])
			split_items_names.append('Coats')
			i  += 1
		elif type_size_items[each] == Gloves and type_size_items[each] != '' and i < 2:
			split_items.append(type_size_items[each])
			split_items_names.append('Gloves')
			i  += 1
		elif type_size_items[each] == Boots and type_size_items[each] != ''and i < 3:
			split_items.append(type_size_items[each])
			split_items_names.append('Boots')
			i += 1

	#Reset for next query
	i = 0

    #Split the type and size from concatanated string
	#Combine the type and size into a tuple to be iterated through in deletion query
	for each in range(len(split_items)):
		if split_items[each] != '':
			print(split_items[each])
			split_items[each] = split_items[each].split()

	#Remove the comma from the type
	for each in range(len(split_items)):
		if split_items[each] != '':
			split_items[each][0] = split_items[each][0].rstrip(",")
			split_items[each] = split_items[each][0],split_items[each][1]


	#Delete the corresponding items submitted from the inventory tables
	for each in range(len(split_items_names)):
		type = split_items[each][0]
		size = split_items[each][1]

		with sql.connect('CoatsDB') as con:
			cur = con.cursor()
			cur.execute("""
				delete from %s
				where %s = (?) and %s = (?)
				limit (?);
			""" % (split_items_names[each]+'_Inventory', split_items_names[each]+'_Type',split_items_names[each]+'_Size'), (type,size, 1))
		con.close()

	#Delete Hat and Socks
	type_item_names = ['Hats','Socks']
	type_items = [Hat, Socks]
	for each in range(len(type_items)):
		with sql.connect('CoatsDB') as con:
			cur = con.cursor()
			cur.execute("""
				delete from %s
				where %s = (?)
				limit ?;
			""" % (type_item_names[each]+'_Inventory', type_item_names[each]+'_Type'), (type_items[each], 1))

def Remove_Record(record):
	record = record.split()

	with sql.connect('CoatsDB') as con:
		cur = con.cursor()
		cur.execute("""
			delete from Records
			where Child_First = (?) and Child_Last = (?) and Record_Id = (?);
		""", (record[0],record[1],record[2]))

	con.close()

def View_Record():
	pass
###################### Queries to update comboboxes #######################
def Grab_Schools():
	with sql.connect('CoatsDB') as con:
		cur = con.cursor()
		cur.execute("select School_Name from Schools;")
		return cur.fetchall()
	con.close()

#Grab all unique values from type column, as the same type may have multiple sizes
def Grab_Item_Types(name):
    item_type = name+'_Type'


    with sql.connect('CoatsDB') as con:
        cur = con.cursor()
        cur.execute("""
            select distinct %s
            from %s;
        """ % (item_type, name))
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

def Grab_Records(record):
	record = record.split()
	Child_First = str(record[0]).rstrip(",")
	Child_Last = str(record[1]).rstrip(",")
	Record_Id = str(record[2]).lstrip("#")

	print(Child_First,Child_Last,Record_Id)
	with sql.connect('CoatsDB') as con:
		cur = con.cursor()
		cur.execute("""
			select *
			from Records
			where Child_First = (?) and Child_Last = (?) and Record_Id = (?);
		""", (Child_First, Child_Last, Record_Id))
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

			#concat type and size into 1 string bc comboboxes take 1 string per entry listing
			combobox_values = []

			subitems = cur.fetchall()

			#Merge the type and size into one string
			for i in range(len(subitems)):
				type, size = subitems[i]
				combobox_values.append(type+', '+size)
			return combobox_values


	elif name in ['Socks','Hats']:
		with sql.connect('CoatsDB') as con:
			cur = con.cursor()
			cur.execute("""
				select distinct %s
				from %s;
			""" % (item_type, table_name))

			#concat type and size into 1 string bc comboboxes take 1 string per entry listing
			combobox_values = []

			subitems = cur.fetchall()

			#Merge the type and size into one string
			for i in range(len(subitems)):
				type = subitems[i]
				combobox_values.append(type)
			return combobox_values

#Populate comboboxes on remove record window
def Populate_Record_CName_Id():
	with sql.connect('CoatsDB') as con:
		cur = con.cursor()
		cur.execute("select Child_First, Child_Last, Record_Id from Records;")

		#Take the 3 values and combine them into a list to display
		listed_values = cur.fetchall()
		for each in range(len(listed_values)):
			listed_values[each] = list(listed_values[each])
			listed_values[each] = str(listed_values[each][0])+', '+str(listed_values[each][1])+', #'+str(listed_values[each][2])

		return listed_values
	con.close()
