#!python3.10
#Ethan Suhr 2022
import sqlite3 as sql

##### Inventory Menubar #####
#Add the allowed type and size of inventory items to be used
#in populating the comboboxes in the add inventory window.
def Add_Item(name, type='', size=''):
	#Check which item is being added and set variables for the sql query
	if name in ['Boots','Coat','Gloves']:
		values = (name+'_Type',name+'_Size')
		with sql.connect('CoatsDB') as con:
			cur = con.cursor()
			cur.execute("""
				insert into %s %s
				values (?,?);
			""" % (name, values), (type, size))
		con.close()
	#Separate because no size column in these tables
	#type must be passed as a tuple
	elif name in ['Socks','Hat']:
		values = (name+'_Type')
		print(name, values, type)
		with sql.connect('CoatsDB') as con:
			cur = con.cursor()
			cur.execute("""
				insert into %s (%s)
				values (?);
			""" % (name, values), (type,))
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
def Grab_Item_Sizes(name):
	with sql.connect('CoatsDB') as con:
		cur = con.cursor()
		cur.execute("""
			select distinct %s
			from %s;
		""" % (name+'_Size',name))
		sizes = cur.fetchall()
		return sizes
	con.close()





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
