#!python3.9 - Ethan Suhr 2022
from ttkwidgets.autocomplete import AutocompleteEntry
from tkinter import *
from tkinter.ttk import Combobox
import Tables
import sqlite3 as sql

class Application(Tk):
	def __init__(self):
		super().__init__()
		#Will do nothing if tables are already created
		Tables.Create()

		#Declare inventory item type global variables for comboboxes
		self.Boot_Types = []
		self.Sock_Types = []
		self.Hat_Types = []
		self.Coat_Types = []
		self.Glove_Types = []

		self.Boot_Sizes = []
		self.Sock_Sizes = []
		self.Hat_Sizes = []
		self.Coat_Sizes = []
		self.Glove_Sizes = []


		self.Main_Window()
		self.config(menu=self.menubar)
		self.mainloop()

	#To be used as seperator between labels
	def Underscore(self, num):
		underscore = ''
		for i in range(num):
			underscore = underscore + '_'
		return underscore

	#Configure the defaults for child windows of the menu screen
	def Configure_Window_Defaults(self, title='', geometry='1280x720'):
		self.Window = Toplevel(self)
		self.Window.title(title)
		self.Window.geometry(geometry)
		self.Window.resizable(0,0)

		self.Top_Frame = Frame(self.Window, bg='#f1f5f4', relief='groove', bd=3)
		self.Center_Frame = Frame(self.Window, bg='#f5f1f2')
		self.Bottom_Frame = Frame(self.Window, bg='#f5f1f2')

		#Configure grid and frames
		self.Window.grid_rowconfigure(1, weight=1)
		self.Window.grid_columnconfigure(0, weight=1)

		self.Top_Frame.grid(row=0, sticky='ew')
		self.Center_Frame.grid(row=1, sticky='nsew')
		self.Bottom_Frame.grid(row=3, sticky='ew')

	#Add item to the inventory tables - Add_Inventory_Window
	def Add_Inventory_Item_Record(self, name, type, size=''):
		print(name, type, size)

		con = sql.connect('CoatsDB')
		cur = con.cursor()
		try:
			cur.execute("""
				insert into Boots (boot_type, boot_size)
				values (?,?);
				""",
				(type, size))
			con.commit()
		except:
			print('ERROR: Failure adding item to database')
			quit()

		con.close()

	#Match the item type to add to the corresponding combobox
	#So that there are set item types and sizes when adding inventory
	def Populate_Comboboxes(self, name, type='', size=''):
		match name:
			case 'Boots':
				print('Boots')
				self.Boot_Types.append(type)
				self.Boot_Sizes.append(size)
			case 'Socks':
				print('Socks')
				self.Sock_Types.append(type)
				self.Sock_Sizes.append(size)
			case 'Gloves':
				print('Gloves')
				self.Glove_Types.append(type)
			case 'Hat':
				print('Hat')
				self.Hat_Types.append(type)
			case 'Coat':
				print('Coat')
				self.Coat_Types.append(type)
				self.Coat_Sizes.append(size)




	################################## GUI #################################
	#Main application window -- the menu screen
	def Main_Window(self):

		self.title('Coats for Kids - Inventory & Record Tracker')
		self.geometry('1600x900')
		self.Title_Image = PhotoImage(file='Title.png')

		#Define Frames and configure the grids
		Top_Frame = Frame(self, height=175, bg='#f1f5f4', relief='groove', bd=3)
		Center_Frame = Frame(self, bg='#f5f1f2')
		Bottom_Frame = Frame(self, height=75, bg='#f5f1f2')

		Center_Left_Frame = Frame(Center_Frame, bg='#f5f1f2')
		Center_Right_Frame = Frame(Center_Frame, bg='#f5f1f2')

		#Configure grid and frames
		self.grid_rowconfigure(1, weight=1)
		self.grid_columnconfigure(0, weight=1)

		Top_Frame.grid(row=0, sticky='ew')
		Center_Frame.grid(row=1, sticky='nsew')
		Bottom_Frame.grid(row=2, sticky='ew')

		#This allows the left and right child frames to fill up center frame completely
		Center_Frame.columnconfigure(0,weight=1)
		Center_Frame.columnconfigure(1, weight=1)
		Center_Frame.rowconfigure(0, weight=1)

		Center_Left_Frame.grid(row=0, column=0, sticky='nsew')
		Center_Right_Frame.grid(row=0, column=1, sticky='nsew')

		#Define Menu bar
		self.menubar = Menu(self, bg='#f1f5f4', font=("Arial",13), relief=None)
		self.filemenu = Menu(self.menubar, tearoff=0)
		self.filemenu.add_command(label="Inventory", command=self.Inventory_Menubar)
		self.filemenu.add_command(label="Schools", command=self.Schools_Menubar)
		self.filemenu.add_separator()
		self.filemenu.add_command(label='Quit', command=quit)
		self.menubar.add_cascade(label='Database', menu=self.filemenu)

		#~~~ Add Widets ~~~
		#Create Labels
		Title_Image = Label(Top_Frame, image=self.Title_Image, font=("Arial",60), pady=5, bg='#f1f5f4')
		Title_Image.pack(fill=X, pady=12)

		Title_Description = Label(Top_Frame, text='Inventory & Record Tracker',  font=("Arial",20), bg='#f1f5f4')
		Title_Description.pack(fill=X)

		Copyright = Label(Bottom_Frame, text='Copyright Coats for Kids 2022', font=("Arial",10), bg='#f5f1f2')
		Copyright.pack(side=BOTTOM)

		Inventory = Label(Center_Left_Frame, text='Inventory', font=("Arial",50), bg='#f5f1f2')
		Inventory.place(relx=.5, rely=.3,anchor= CENTER)

		Inventory_Underscore = Label(Center_Left_Frame, text=self.Underscore(35), font=("Arial",15), bg='#f5f1f2')
		Inventory_Underscore.place(relx=.5, rely=.38,anchor= CENTER)

		Child = Label(Center_Right_Frame, text='Records', font=("Arial",50), bg='#f5f1f2')
		Child.place(relx=.5, rely=.3, anchor=CENTER)

		Child_Underscore = Label(Center_Right_Frame, text=self.Underscore(35), font=("Arial",15), bg='#f5f1f2')
		Child_Underscore.place(relx=.5, rely=.38,anchor= CENTER)

		#Create buttons

		Add_Inventory = Button(Center_Left_Frame, text="Add Inventory", command=self.Add_Inventory_Window, font=("Arial",20), bd=3)
		Add_Inventory.place(relx=.5, rely=.5,anchor= CENTER, height=55, width=200)

		View_Inventory = Button(Center_Left_Frame, text="View Inventory", command=self.View_Inventory_Window, font=("Arial",20), bd=3)
		View_Inventory.place(relx=.5, rely=.62,anchor= CENTER, height=55, width=200)

		Lookup_Record = Button(Center_Right_Frame, text="Add Record", command=self.Add_Record_Window, font=("Arial",20), bd=3)
		Lookup_Record.place(relx=.5, rely=.5,anchor= CENTER, height=55, width=200)

		Add_Record = Button(Center_Right_Frame, text="View record", command=self.View_Record_Window, font=("Arial",20), bd=3)
		Add_Record.place(relx=.5, rely=.62,anchor= CENTER, height=55, width=200)

	#Add Inventory window
	def Add_Inventory_Window(self):
	#Create Add Inventory Window
		self.Configure_Window_Defaults(title='Add Inventory')

	#~~~ Add Widets ~~~
	#Create Labels
		Title_Image = Label(self.Top_Frame, image=self.Title_Image, font=("Arial",60), pady=5, bg='#f1f5f4')
		Title_Image.pack(fill=X, pady=12)

		Title_Desc = Label(self.Top_Frame, text='Add Inventory',  font=("Arial",25), bg='#f1f5f4')
		Title_Desc.pack(fill=X)

		Item_Name = Label(self.Center_Frame, text='Item Name:', font=("Arial",23), pady=5, bg='#f5f1f2')
		Item_Name.place(relx=.42, rely=.22,anchor= CENTER, height=55, width=200)

		Item_Type = Label(self.Center_Frame, text='Item Type:', font=("Arial",23), pady=5, bg='#f5f1f2')
		Item_Type.place(relx=.42, rely=.4,anchor= CENTER, height=55, width=200)

		Item_Size = Label(self.Center_Frame, text='Item Size:', font=("Arial",23), pady=5, bg='#f5f1f2')
		Item_Size.place(relx=.42, rely=.58,anchor= CENTER, height=55, width=200)

		Item_Amount = Label(self.Center_Frame, text='Quantity:', font=("Arial",22), pady=5, bg='#f5f1f2')
		Item_Amount.place(relx=.42, rely=.74,anchor= CENTER, height=55, width=200)

		Copyright = Label(self.Bottom_Frame, text='Copyright Coats for Kids 2022', font=("Arial",10), bg='#f5f1f2')
		Copyright.pack(side=BOTTOM)

	#Create Entry Widgets
		Item_Amount_Entry = Entry(self.Center_Frame, text='Enter amount',font=("Arial",14))
		Item_Amount_Entry.place(relx=.58, rely=.74,anchor= CENTER)

	#Create Combobox Widgets
		Item_Combobox = Combobox(self.Center_Frame, text='Select an item', state='readonly',font=("Arial",14))
		Item_Combobox['values'] = ('Hat','Coat','Gloves','Boots','Socks')
		Item_Combobox.place(relx=.58, rely=.22,anchor= CENTER)

		Item_Type_Combobox = Combobox(self.Center_Frame, text='Select item type', state='readonly',font=("Arial",14))
		Item_Type_Combobox['values'] = ('test','test2','test3')
		Item_Type_Combobox.place(relx=.58, rely=.4,anchor= CENTER)

		Item_Size_Combobox = Combobox(self.Center_Frame, text='Select item size', state='readonly',font=("Arial",14))
		Item_Size_Combobox['values'] = ('test','test2','test3')
		Item_Size_Combobox.place(relx=.58, rely=.58,anchor= CENTER)

	#Create Buttons
		#lambda: self.Add_Inventory_Item_Record(Add_Item_Name_Combobox.get(),Add_Item_Type_Entry.get(),Add_Item_Size_Entry.get()),
		Submit = Button(self.Center_Frame, text="Submit",font=("Arial",20), command='', padx=10, pady=10, width=25, bd=3)
		Submit.place(relx=.5, rely=.9,anchor= CENTER, height=55, width=200)

		Exit = Button(self.Bottom_Frame, text="Go Back", font=("Arial",15), command=self.Window.destroy, bd=3)
		Exit.pack(pady=15, padx=45, side=LEFT)

	#View Inventory window
	def View_Inventory_Window(self):
		#Create View Inventory Window
		self.Configure_Window_Defaults(title='View Inventory')

	#~~~ Add Widets ~~~
	#Create Labels
		Title_Image = Label(self.Top_Frame, image=self.Title_Image, font=("Arial",60), pady=5, bg='#f1f5f4')
		Title_Image.pack(fill=X, pady=12)

		Title_Description = Label(self.Top_Frame, text='View Inventory',  font=("Arial",20), bg='#f1f5f4')
		Title_Description.pack(fill=X)

		Select_lbl = Label(self.Center_Frame, text='Search Item', font=("Arial",20), pady=5, bg='#f5f1f2')
		Select_lbl.place(relx=.5, rely=.12,anchor= CENTER)

		Main_Item_lbl = Label(self.Center_Frame, text='Item: ITEM', font=("Arial",20), pady=5, bg='#f5f1f2')
		Main_Item_lbl.place(relx=.46, rely=.36,anchor= CENTER)

		Main_Total_lbl = Label(self.Center_Frame, text='Total: ', font=("Arial",20), pady=5, bg='#f5f1f2')
		Main_Total_lbl.place(relx=.55, rely=.36,anchor= CENTER)

		Seperator_lbl = Label(self.Center_Frame, text=self.Underscore(35),  font=("Arial",15), bg='#f5f1f2')
		Seperator_lbl.place(relx=.35, rely=.4)

		Copyright = Label(self.Bottom_Frame, text='Copyright Coats for Kids 2022', font=("Arial",10), bg='#f5f1f2')
		Copyright.pack(side=BOTTOM)

	#Create Entry Boxes
		Select_CB = Combobox(self.Center_Frame, text='Inventory Item', state='readonly', font=("Arial",14))
		Select_CB['values'] = ('test','test2','test3','banana','banish','banner','banquet','ballot','ballet','ball','balance','barrell','baghdad','bunny','','','','','','','','','','','','','','','')
		Select_CB.place(relx=.5, rely=.2,anchor= CENTER)

	#Create buttons
		Select_btn = Button(self.Center_Frame, text="Search", command='', padx=5, pady=5, font=("Arial", 14), bd=3)
		Select_btn.place(relx=.62, rely=.2,anchor= CENTER)

		Exit = Button(self.Bottom_Frame, text="Go Back", font=("Arial",15), command=self.Window.destroy, bd=3)
		Exit.pack(pady=15, padx=45, side=LEFT)

	#Add Record window
	def Add_Record_Window(self):
		#Create Add Record Window
		self.Configure_Window_Defaults(title='Add Record')

	#~~~ Add Widets ~~~
	#Create Labels
		Title_Image = Label(self.Top_Frame, image=self.Title_Image, font=("Arial",60), pady=5, bg='#f1f5f4')
		Title_Image.pack(fill=X, pady=12)

		Title_Description = Label(self.Top_Frame, text='Add Record',  font=("Arial",20), bg='#f1f5f4')
		Title_Description.pack(fill=X)

		Copyright = Label(self.Bottom_Frame, text='Copyright Coats for Kids 2022', font=("Arial",10), bg='#f5f1f2')
		Copyright.pack(side=BOTTOM)


	#Child Labels
		Child_First_Name = Label(self.Center_Frame, text='Child First', font=("Arial",20), pady=5, bg='#f5f1f2')
		Child_First_Name.place(relx=.24, rely=.12,anchor= CENTER)

		Child_Last_Name = Label(self.Center_Frame, text='Child Last', font=("Arial",20), pady=5, bg='#f5f1f2')
		Child_Last_Name.place(relx=.42, rely=.12,anchor= CENTER)

		Child_Age = Label(self.Center_Frame, text='Age', font=("Arial",20), pady=5, bg='#f5f1f2')
		Child_Age.place(relx=.55, rely=.12,anchor= CENTER)

		Child_Gender = Label(self.Center_Frame, text='Gender', font=("Arial",20), pady=5, bg='#f5f1f2')
		Child_Gender.place(relx=.63, rely=.12,anchor= CENTER)

		Child_School = Label(self.Center_Frame, text='School', font=("Arial",20), pady=5, bg='#f5f1f2')
		Child_School.place(relx=.72, rely=.12,anchor= CENTER)

	#Parent Labels
		Parent_First_Name = Label(self.Center_Frame, text='Parent First', font=("Arial",20), pady=5, bg='#f5f1f2')
		Parent_First_Name.place(relx=.14, rely=.32,anchor= CENTER)

		Parent_Last_Name = Label(self.Center_Frame, text='Parent Last', font=("Arial",20), pady=5, bg='#f5f1f2')
		Parent_Last_Name.place(relx=.31, rely=.32,anchor= CENTER)

		Parent_Phone = Label(self.Center_Frame, text='Phone', font=("Arial",20), pady=5, bg='#f5f1f2')
		Parent_Phone.place(relx=.48, rely=.32,anchor= CENTER)

		Street = Label(self.Center_Frame, text='Street', font=("Arial",20), pady=5, bg='#f5f1f2')
		Street.place(relx=.65, rely=.32,anchor= CENTER)

		City = Label(self.Center_Frame, text='City', font=("Arial",20), pady=5, bg='#f5f1f2')
		City.place(relx=.8, rely=.32,anchor= CENTER)

		Zip = Label(self.Center_Frame, text='Zip', font=("Arial",20), pady=5, bg='#f5f1f2')
		Zip.place(relx=.9, rely=.32,anchor= CENTER)

	#Item Labels
		Hat = Label(self.Center_Frame, text='Hat', font=("Arial",20), pady=5, bg='#f5f1f2')
		Hat.place(relx=.33, rely=.54,anchor= CENTER)

		Coat = Label(self.Center_Frame, text='Coat', font=("Arial",20), pady=5, bg='#f5f1f2')
		Coat.place(relx=.50, rely=.54,anchor= CENTER)

		Gloves = Label(self.Center_Frame, text='Gloves', font=("Arial",20), pady=5, bg='#f5f1f2')
		Gloves.place(relx=.66, rely=.54,anchor= CENTER)

		Socks = Label(self.Center_Frame, text='Socks', font=("Arial",20), pady=5, bg='#f5f1f2')
		Socks.place(relx=.4, rely=.74,anchor= CENTER)

		Boots = Label(self.Center_Frame, text='Boots', font=("Arial",20), pady=5, bg='#f5f1f2')
		Boots.place(relx=.6, rely=.74,anchor= CENTER)

	#Create Entry Widgets
	#Child Entry Widgets
		Child_First_Entry = Entry(self.Center_Frame, font=("Arial",13))
		Child_First_Entry.place(relx=.24, rely=.19,anchor= CENTER)

		Child_Last_Entry = Entry(self.Center_Frame, font=("Arial",13))
		Child_Last_Entry.place(relx=.42, rely=.19,anchor= CENTER)

		Child_Age_Entry = Entry(self.Center_Frame, font=("Arial",13))
		Child_Age_Entry.place(relx=.55, rely=.19,anchor= CENTER, width='50')

		Parent_First_Entry = Entry(self.Center_Frame, font=("Arial",13))
		Parent_First_Entry.place(relx=.14, rely=.39,anchor= CENTER)

		Parent_Last_Entry = Entry(self.Center_Frame, font=("Arial",13))
		Parent_Last_Entry.place(relx=.31, rely=.39,anchor= CENTER)

		Phone_Entry = Entry(self.Center_Frame, font=("Arial",13))
		Phone_Entry.place(relx=.48, rely=.39,anchor= CENTER)

		Street_Entry = Entry(self.Center_Frame, font=("Arial",13))
		Street_Entry.place(relx=.65, rely=.39,anchor= CENTER)

		City_Entry = Entry(self.Center_Frame, font=("Arial",13))
		City_Entry.place(relx=.8, rely=.39,anchor= CENTER, width='150')

		Zip_Entry = Entry(self.Center_Frame, font=("Arial",13))
		Zip_Entry.place(relx=.9, rely=.39,anchor= CENTER, width='75')

	#Create Combobox Widgets
	#User input is required to fill values for all but gender combobox
		Gender_Combobox = Combobox(self.Center_Frame, text='Select Gender', state='readonly')
		Gender_Combobox['values'] = ('Male','Female','Other')
		Gender_Combobox.place(relx=.63, rely=.19,anchor= CENTER, width='65')

		School_Combobox = Combobox(self.Center_Frame, text='Select School', state='readonly')
		School_Combobox['values'] = ('')
		School_Combobox.place(relx=.72, rely=.19,anchor= CENTER, width='100')

		Hat_Combobox = Combobox(self.Center_Frame, text='Select Hat', state='readonly')
		Hat_Combobox.place(relx=.33, rely=.61,anchor= CENTER)

		Coat_Combobox = Combobox(self.Center_Frame, text='Select Coat', state='readonly')
		Coat_Combobox.place(relx=.50, rely=.61,anchor= CENTER)

		Gloves_Combobox = Combobox(self.Center_Frame, text='Select Gloves', state='readonly')
		Gloves_Combobox.place(relx=.66, rely=.61,anchor= CENTER)

		Socks_Combobox = Combobox(self.Center_Frame, text='Select Socks', state='readonly')
		Socks_Combobox.place(relx=.4, rely=.8,anchor= CENTER)

		Boots_Combobox = Combobox(self.Center_Frame, text='Select Boots', state='readonly')
		Boots_Combobox.place(relx=.6, rely=.8,anchor= CENTER)


	#Create Buttons
		Exit = Button(self.Bottom_Frame, text="Go Back", font=("Arial",15), command=self.Window.destroy, bd=3)
		Exit.pack(pady=15, padx=45, side=LEFT)

		Submit = Button(self.Center_Frame, text="Submit Record", font=("Arial",15), command='', bd=3)
		Submit.place(relx=.5,rely=.93,anchor=CENTER)

	#View Record window
	def View_Record_Window(self):
		#Create View Record Window
		self.Configure_Window_Defaults(title='View Record')

	#~~~ Add Widets ~~~
	#Create Labels
		Title_Image = Label(self.Top_Frame, image=self.Title_Image, font=("Arial",60), pady=5, bg='#f1f5f4')
		Title_Image.pack(fill=X, pady=12)

		Title_Description = Label(self.Top_Frame, text='View Inventory',  font=("Arial",20), bg='#f1f5f4')
		Title_Description.pack(fill=X)

		Search = Label(self.Center_Frame, text='Search Records by Child Name', font=("Arial",20), pady=5, bg='#f5f1f2')
		Search.place(relx=.5, rely=.12,anchor= CENTER)

		# Main_Item_lbl = Label(self.Center_Frame, text='Item: ITEM', font=("Arial",20), pady=5, bg='#f5f1f2')
		# Main_Item_lbl.place(relx=.46, rely=.36,anchor= CENTER)
		#
		# Main_Total_lbl = Label(self.Center_Frame, text='Total: ', font=("Arial",20), pady=5, bg='#f5f1f2')
		# Main_Total_lbl.place(relx=.55, rely=.36,anchor= CENTER)

		Underscore = Label(self.Center_Frame, text=self.Underscore(35),  font=("Arial",15), bg='#f5f1f2')
		Underscore.place(relx=.35, rely=.4)

		Copyright = Label(self.Bottom_Frame, text='Copyright Coats for Kids 2022', font=("Arial",10), bg='#f5f1f2')
		Copyright.pack(side=BOTTOM)


	#Create Entry Boxes
		#TO BE REPLACED WITH ALL CHILDREN NAMES IN THE RECORDS TABLE
		TEMPORARY_LIST = ['Jordan','Eli','Gavin','Patrick','Behemoth','Kenny','Budders','Santa Claus']

		AutocompleteBox = AutocompleteEntry(self.Center_Frame, font=("Arial",14), completevalues=TEMPORARY_LIST)
		AutocompleteBox.place(relx=.5, rely=.22,anchor= CENTER)

	#Create buttons
		Search = Button(self.Center_Frame, text="Search", command='', padx=5, pady=5, font=("Arial", 12), bd=3)
		Search.place(relx=.62, rely=.22,anchor= CENTER)

		Exit = Button(self.Bottom_Frame, text="Go Back", font=("Arial",15), command=self.Window.destroy, bd=3)
		Exit.pack(pady=15, padx=45, side=LEFT)

	##### MENU BARS #####
	#Inventory menubar
	def Inventory_Menubar(self):
		self.Configure_Window_Defaults(title='Settings', geometry='800x600')

		#~~~ Add Widets ~~~
		#Add Items Labels
		Add_Item = Label(self.Center_Frame, text='Add an Item to the database', font=("Arial",23), pady=5, bg='#f5f1f2')
		Add_Item.place(relx=.5, rely=.16,anchor= CENTER, height=55)

		Add_Item_Underscore = Label(self.Center_Frame, text=self.Underscore(35), font=("Arial",15), bg='#f5f1f2')
		Add_Item_Underscore.place(relx=.5, rely=.22,anchor= CENTER)

		Add_Item_Name = Label(self.Center_Frame, text='Name', font=("Arial",18), pady=5, bg='#f5f1f2')
		Add_Item_Name.place(relx=.15, rely=.32,anchor= CENTER, height=55)

		Add_Item_Type = Label(self.Center_Frame, text='Type', font=("Arial",18), pady=5, bg='#f5f1f2')
		Add_Item_Type.place(relx=.35, rely=.32,anchor= CENTER, height=55)

		Add_Item_Size = Label(self.Center_Frame, text='Size', font=("Arial",18), pady=5, bg='#f5f1f2')
		Add_Item_Size.place(relx=.55, rely=.32,anchor= CENTER, height=55)

		#Remove Item Labels
		Remove_Item = Label(self.Center_Frame, text='Remove an Item from the database', font=("Arial",23), pady=5, bg='#f5f1f2')
		Remove_Item.place(relx=.5, rely=.56,anchor= CENTER, height=55)

		Remove_Item_Underscore = Label(self.Center_Frame, text=self.Underscore(35), font=("Arial",15), bg='#f5f1f2')
		Remove_Item_Underscore.place(relx=.5, rely=.62,anchor= CENTER)

		Remove_Item_Name = Label(self.Center_Frame, text='Name', font=("Arial",18), pady=5, bg='#f5f1f2')
		Remove_Item_Name.place(relx=.15, rely=.72,anchor= CENTER, height=55)

		Remove_Item_Type = Label(self.Center_Frame, text='Type', font=("Arial",18), pady=5, bg='#f5f1f2')
		Remove_Item_Type.place(relx=.35, rely=.72,anchor= CENTER, height=55)

		Remove_Item_Size = Label(self.Center_Frame, text='Size', font=("Arial",18), pady=5, bg='#f5f1f2')
		Remove_Item_Size.place(relx=.55, rely=.72,anchor= CENTER, height=55)

		Copyright = Label(self.Bottom_Frame, text='Copyright Coats for Kids 2022', font=("Arial",10), bg='#f5f1f2')
		Copyright.pack(side=BOTTOM)

		#Create Entry Boxes
		Add_Item_Type_Entry = Entry(self.Center_Frame, font=("Arial",14), width=15)
		Add_Item_Type_Entry.place(relx=.35, rely=.39,anchor= CENTER)

		Add_Item_Size_Entry = Entry(self.Center_Frame, font=("Arial",14), width=15)
		Add_Item_Size_Entry.place(relx=.55, rely=.39,anchor= CENTER)

		#Create Comboboxes
		Add_Item_Name_Combobox = Combobox(self.Center_Frame, state='readonly', width=15)
		Add_Item_Name_Combobox['values'] = ('Hat','Coat','Gloves','Boots','Socks')
		Add_Item_Name_Combobox.place(relx=.15, rely=.39,anchor= CENTER)

		Remove_Item_Name_Combobox = Combobox(self.Center_Frame, state='readonly', width=15)
		Remove_Item_Name_Combobox['values'] = ('Hat','Coat','Gloves','Boots','Socks')
		Remove_Item_Name_Combobox.place(relx=.15, rely=.79,anchor= CENTER)

		Remove_Item_Type_Entry = Combobox(self.Center_Frame, state='readonly', width=15)
		Remove_Item_Type_Entry['values'] = ('test')
		Remove_Item_Type_Entry.place(relx=.35, rely=.79,anchor= CENTER)

		Remove_Item_Size_Entry = Combobox(self.Center_Frame, state='readonly', width=15)
		Remove_Item_Size_Entry['values'] = ('test')
		Remove_Item_Size_Entry.place(relx=.55, rely=.79,anchor= CENTER)

		#Create Buttons
		#Lambda is required so that the buttons command is not ran upon window creation
		#https://stackoverflow.com/questions/8269096/why-is-button-parameter-command-executed-when-declared
		#lambda: self.Add_Inventory_Item_Record(Add_Item_Name_Combobox.get(),Add_Item_Type_Entry.get(),Add_Item_Size_Entry.get()),
		Add_Item_Submit = Button(self.Center_Frame, text="Submit", font=("Arial",14), command=lambda: self.Populate_Comboboxes(Add_Item_Name_Combobox.get(),Add_Item_Type_Entry.get(),Add_Item_Size_Entry.get()), bd=3)
		Add_Item_Submit.place(relx=.75, rely=.37,anchor= CENTER)

		Remove_Item_Submit = Button(self.Center_Frame, text="Submit", font=("Arial",14), command='', bd=3)
		Remove_Item_Submit.place(relx=.75, rely=.77,anchor= CENTER)

		Exit = Button(self.Bottom_Frame, text="Go Back", font=("Arial",15), command=self.Window.destroy, bd=3)
		Exit.pack(pady=15, padx=45, side=LEFT)

	#Schools menubar
	def Schools_Menubar(self):
		self.Configure_Window_Defaults(title='Schools', geometry='800x600')

		#~~~ Add Widets ~~~
		#Create Labels
		Add_School = Label(self.Center_Frame, text='Add a School to the database', font=("Arial",23), pady=5, bg='#f5f1f2')
		Add_School.place(relx=.5, rely=.16,anchor= CENTER, height=55)

		Add_School_Underscore = Label(self.Center_Frame, text=self.Underscore(35), font=("Arial",15), bg='#f5f1f2')
		Add_School_Underscore.place(relx=.5, rely=.22,anchor= CENTER)

		Add_School_Name = Label(self.Center_Frame, text='Name', font=("Arial",18), pady=5, bg='#f5f1f2')
		Add_School_Name.place(relx=.5, rely=.32,anchor= CENTER, height=55)

		Remove_School = Label(self.Center_Frame, text='Remove a School from the database', font=("Arial",23), pady=5, bg='#f5f1f2')
		Remove_School.place(relx=.5, rely=.56,anchor= CENTER, height=55)

		Remove_School_Underscore = Label(self.Center_Frame, text=self.Underscore(35), font=("Arial",15), bg='#f5f1f2')
		Remove_School_Underscore.place(relx=.5, rely=.62,anchor= CENTER)

		Remove_School_Name = Label(self.Center_Frame, text='Name', font=("Arial",18), pady=5, bg='#f5f1f2')
		Remove_School_Name.place(relx=.5, rely=.72,anchor= CENTER, height=55)

		Copyright = Label(self.Bottom_Frame, text='Copyright Coats for Kids 2022', font=("Arial",10), bg='#f5f1f2')
		Copyright.pack(side=BOTTOM)

		#Create Entry Boxes
		Add_School_Entry = Entry(self.Center_Frame, font=("Arial",14), width=15)
		Add_School_Entry.place(relx=.5, rely=.39,anchor= CENTER)

		#Create Combobox
		Remove_School_Combobox = Combobox(self.Center_Frame, state='readonly', width=15)
		Remove_School_Combobox['values'] = ('test')
		Remove_School_Combobox.place(relx=.5, rely=.79,anchor= CENTER)

		#Create Buttons
		Add_School_Submit = Button(self.Center_Frame, text="Submit", font=("Arial",14), command='', bd=3)
		Add_School_Submit.place(relx=.75, rely=.37,anchor= CENTER)

		Remove_School_Submit = Button(self.Center_Frame, text="Submit", font=("Arial",14), command='', bd=3)
		Remove_School_Submit.place(relx=.75, rely=.77,anchor= CENTER)

		Exit = Button(self.Bottom_Frame, text="Go Back", font=("Arial",15), command=self.Window.destroy, bd=3)
		Exit.pack(pady=15, padx=45, side=LEFT)

	########################################################################

#Exit if this is not being ran as main script
if __name__ == "__main__":
	Application()
else:
	quit()
