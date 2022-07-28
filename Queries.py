#!python3.10
#Ethan Suhr 2022
import sqlite3 as sql

#Add inventory item(s) to the inventory tables.
def Add_Inventory_Record(name, type, size=''):

	con = sql.connect('CoatsDB')
	cur = con.cursor()
	try:
		cur.execute("""
			insert into Boots (boot_type, boot_size)
			values (?,?);
			""", (type, size))
		con.commit()
	except:
		print('ERROR: Failure adding item to database')
		quit()

	con.close()


def Add_Item(name, type='', size=''):
	#Set respective table values for the sql query.
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
	elif name in ['Socks','Hat']:
		values = (name+'_Type')
		with sql.connect('CoatsDB') as con:
			cur = con.cursor()
			cur.execute("""
				insert into %s (%s)
				values (?);
			""" % (name, values), (type))
		con.close()
