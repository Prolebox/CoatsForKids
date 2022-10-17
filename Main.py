#!python3.10
#Ethan Suhr 2022
from ttkwidgets.autocomplete import AutocompleteEntry
from tkinter import *
from tkinter.ttk import Combobox
import Tables
import Queries

#Create the GUI
class Application(Tk):
	def __init__(self):
		super().__init__()

		#Will do nothing if tables are already created
		Tables.Create()

		self.Main_Window()
		self.config(menu=self.menubar)
		#Keeps application running
		self.mainloop()

	#To be used as seperator between labels
	def Underscore(self, num):
		underscore = ''
		for i in range(num):
			underscore = underscore + '_'
		return underscore

	#Add record window
	def Btn_Submit_Inventory(self, name, type, size='', amount=''):
		Queries.Add_Inventory_Record(name.get(),type.get(),size.get(),amount.get())
		self.Clear_Combobox(name, type, size)
		self.Clear_Entry_box(amount)

	def Btn_Remove_Inventory(self, name, type, size='', amount=''):
		Queries.Remove_Inventory_Record(name.get(),type.get(),size.get(),amount.get())
		self.Clear_Combobox(name, type, size)
		self.Clear_Entry_box(amount)

	#View inventory window
	def Btn_View_Inventory(self, name):
		#Enable text box to clear between searches, then to put data in
		self.View_Subitems.config(state=NORMAL)
		self.View_Subitems.delete('1.0', END)

		self.View_Item_Selected['text'] = 'Item: ' + name
		self.View_Total['text'] = 'Total:',Queries.Total_Item_Count(name)

		#Grab dictionary of subitem : count
		subitems = Queries.Total_Subitems_Count(name)

		if name in ['Boots','Coats','Gloves']:
			#Display subitem : count
			for type, size in subitems:
				self.View_Subitems.insert(END, type +', '+ size +': '+ str(subitems[type, size])+'\n')
		elif name in ['Socks','Hats']:
			for type in subitems:
				self.View_Subitems.insert(END, str(type).lstrip("('").rstrip("',)") +': '+ str(subitems[type])+'\n')

		#Disable text widget so you cannot type
		self.View_Subitems.config(state=DISABLED)


	#School menubar window
	def Btn_Submit_School(self, school):
		match Queries.Add_School(school.get()):
			case 'school exists':
				self.Notification_Window(text='This School has already been \nadded to the database!')
			case 'empty':
				self.Notification_Window(text='You must enter a school name \nto be added to the database!')
		self.Clear_Entry_box(school)
		self.Remove_School_Combobox['values'] = (Queries.Grab_Schools())

	#School menubar window
	def Btn_Remove_School(self, school):
		Queries.Remove_School(school.get())
		self.Remove_School_Combobox['values'] = (Queries.Grab_Schools())
		self.Clear_Combobox(school)

	#Add/Remove Item window
	def Btn_Submit_Item(self, name, type, size):
		#Test to see if the item exists. If so, pop up notification.
		#If item doesnt exist it will be added
		if Queries.Add_Item(name.get(),type.get(),size.get()) == 'item exists':
			self.Notification_Window(text='This item already exists \nin the database!')
		elif Queries.Add_Item(name.get(),type.get(),size.get()) == 'empty':
			self.Notification_Window(text='Please enter a value \nin every field!')
		self.Clear_Entry_box(type, size)

	#Add Record Window
	def Btn_Submit_Record(self, CFirst, CLast, CAge, Gender, School, PFirst, PLast, Phone, Street, City, Zip, Hat, Coat, Gloves, Socks, Boots):
		#Submit record
		if Queries.Add_Record(CFirst.get(), CLast.get(), CAge.get(), Gender.get(), School.get(), PFirst.get(), PLast.get(), Phone.get(), Street.get(), City.get(), Zip.get(), Hat.get(), Coat.get(), Gloves.get(), Socks.get(), Boots.get()) == 'empty':
			self.Notification_Window(text='Please enter a value \nin every entry box!')

		self.Clear_Entry_box(CFirst, CLast, CAge, PFirst, PLast, Phone, Street, City, Zip)
		self.Clear_Combobox(Gender, School, Hat, Coat, Gloves, Socks, Boots)

	def Btn_Remove_Record(self, record):
		Queries.Remove_Record(record.get())
		self.Clear_Combobox(record)
		self.Remove_Record_Combobox['values'] = Queries.Populate_Record_CName_Id()

	def Btn_View_Record(self, record):

		#Grab the record desired from the Records table
		results = Queries.Grab_Records(record.get())

		#Order of results list
		#('CFirst', 'CLast', 'CAge', 'Male', 'Hedhges',
		#'PFirst', 'PLast', 'Phone', 'Street', 'City', 'Zip',
		#'Hats', 'Coat, Coat', 'Gloves, Gloves', 'Socks', 'Boots, Boots', 39)

		#Populate labels with record information
		self.View_Child_First['text'] = 'Childs First: '+results[0]
		self.View_Child_Last['text'] = 'Childs Last: '+results[1]
		self.View_Child_Age['text'] = 'Childs Age: '+results[2]
		self.View_Child_Gender['text'] = 'Childs Gender: '+results[3]
		self.View_Child_School['text'] = 'Childs School: '+results[4]

		self.View_Parent_First['text'] = 'Parents First: '+results[5]
		self.View_Parent_Last['text'] = 'Parents Last: '+results[6]
		self.View_Parent_Phone['text'] = 'Phone: '+results[7]
		self.View_Parent_Street['text'] = 'Street: '+results[8]
		self.View_Parent_City['text'] = 'City: '+results[9]
		self.View_Parent_Zip['text'] = 'Zip: '+results[10]

		self.View_Hat['text'] = 'Hat: '+results[11]
		self.View_Coat['text'] = 'Coat: '+results[12]
		self.View_Gloves['text'] = 'Gloves: '+results[13]
		self.View_Socks['text'] = 'Socks: '+results[14]
		self.View_Boots['text'] = 'Boots: '+results[15]
		self.View_Id['text'] = 'Record ID: '+str(results[16])

	#Add/Remove Item window
	def Btn_Remove_Item(self, name, type, size):
		Queries.Remove_Item(name.get(),type.get(),size.get())
		self.Clear_Combobox(type, size)
		#Must pass an argument since the function is bound to a tkinter event and expects one
		#Passing an emtpy string seems to work
		self.Update_Remove_Item_Type_Combobox('')

	def Clear_Entry_box(self, *args):
		for each in args:
			each.delete(0, END)

	def Clear_Combobox(self, *args):
		for each in args:
			#Set because comboboxes are populated with strings
			each.set('')

	#Configure the defaults for child windows of the main window
	def Configure_Window_Defaults(self, window_name='', title='', geometry='1280x720'):
			#Create new window on top of the Main window
			self.Window = Toplevel(self)
			self.Window.title(title)
			self.Window.geometry(geometry)
			#Disallows resizing the window
			self.Window.resizable(0,0)

			#Divides window into 3 rows
			self.Top_Frame = Frame(self.Window, bg='#f1f5f4', relief='groove', bd=3)
			self.Center_Frame = Frame(self.Window, bg='#f5f1f2')
			self.Bottom_Frame = Frame(self.Window, bg='#f5f1f2')

			#Configure grid and frames
			self.Window.grid_rowconfigure(1, weight=1)
			self.Window.grid_columnconfigure(0, weight=1)

			self.Top_Frame.grid(row=0, sticky='ew')
			self.Center_Frame.grid(row=1, sticky='nsew')
			self.Bottom_Frame.grid(row=3, sticky='ew')

	############################# Bounds Events ############################

	def Reset_Counter(self, event):
		self.counter = 0

	## REMOVE INVENTORY WINDOW ##
	def Update_Remove_Inventory_Type_Combobox(self, event):
		self.Clear_Combobox(self.Remove_Inventory_Type_Combobox)
		self.Clear_Combobox(self.Remove_Inventory_Size_Combobox)
		name = self.Remove_Inventory_Combobox.get()
		if name in ['Boots','Coats','Gloves']:
			self.Remove_Inventory_Type_Combobox['values'] = (Queries.Grab_Item_Types(name))
		elif name in ['Socks','Hats']:
			self.Remove_Inventory_Type_Combobox['values'] = (Queries.Grab_Item_Types(name))
			self.Remove_Inventory_Size_Combobox['values'] = ()

	#Update the item size based off the item type selected
	def Update_Remove_Inventory_Size_Combobox(self, event):
		#Clear the box when switching b/c certain types do not share the previously selected size
		self.Clear_Combobox(self.Remove_Inventory_Size_Combobox)
		name = self.Remove_Inventory_Combobox.get()
		type = self.Remove_Inventory_Type_Combobox.get()
		if name in ['Boots','Coats','Gloves']:
			self.Remove_Inventory_Size_Combobox['values'] = (Queries.Grab_Item_Sizes(name, type))


	## ADD INVENTORY WINDOW ##
	#Update the Item Type based on Item selected
	def Update_Add_Inventory_Type_Combobox(self, event):
		self.Clear_Combobox(self.Add_Inventory_Type_Combobox)
		self.Clear_Combobox(self.Add_Inventory_Size_Combobox)
		name = self.Add_Inventory_Combobox.get()
		if name in ['Boots','Coats','Gloves']:
			self.Add_Inventory_Type_Combobox['values'] = (Queries.Grab_Item_Types(name))
		elif name in ['Socks','Hats']:
			self.Add_Inventory_Type_Combobox['values'] = (Queries.Grab_Item_Types(name))
			self.Add_Inventory_Size_Combobox['values'] = ()

	#Update the item size based off the item type selected
	def Update_Add_Inventory_Size_Combobox(self, event):
		#Clear the box when switching b/c certain types do not share the previously selected size
		self.Clear_Combobox(self.Add_Inventory_Size_Combobox)
		name = self.Add_Inventory_Combobox.get()
		type = self.Add_Inventory_Type_Combobox.get()
		if name in ['Boots','Coats','Gloves']:
			self.Add_Inventory_Size_Combobox['values'] = (Queries.Grab_Item_Sizes(name, type))

	## ITEM MENUBAR ##
	#Update the item type for the remove combo boxes based off item selected for removal
	def Update_Remove_Item_Type_Combobox(self, event):
		self.Clear_Combobox(self.Remove_Item_Type_Combobox)
		self.Clear_Combobox(self.Remove_Item_Size_Combobox)
		name = self.Remove_Item_Name_Combobox.get()
		if name in ['Boots','Coats','Gloves']:
			self.Remove_Item_Type_Combobox['values'] = (Queries.Grab_Item_Types(name))
		elif name in ['Socks','Hats']:
			self.Remove_Item_Type_Combobox['values'] = (Queries.Grab_Item_Types(name))
			#Set Size Combobox to be empty
			self.Remove_Item_Size_Combobox['values'] = ()

	#Update the item size for the remove combo boxes based off item type selected for removal
	def Update_Remove_Item_Size_Combobox(self, event):
		name = self.Remove_Item_Name_Combobox.get()
		type = self.Remove_Item_Type_Combobox.get()
		if name in ['Boots','Coats','Gloves']:
			self.Remove_Item_Size_Combobox['values'] = (Queries.Grab_Item_Sizes(name, type))

	#Disable or Enable the Item Size entry box for the add item window based off item selected
	def Disable_Enable_Entry_Box(self, event):
		name = self.Add_Item_Name_Combobox.get()
		if name in ['Boots','Coats','Gloves']:
			if self.Add_Item_Size_Entry['state'] == 'disabled':
				self.Add_Item_Size_Entry.config(state="normal")
			else:
				pass
		elif name in ['Socks','Hats']:
			self.Add_Item_Size_Entry.delete(0, END)
			self.Add_Item_Size_Entry.config(state="disabled")


	################################## GUI #################################

	##### MAIN GUI WINDOWS #####
	#Menu screen
	def Main_Window(self):

		self.title('Coats for Kids - Inventory & Record Tracker')
		self.geometry('1600x900')
		self.Title_Image = PhotoImage(file='Title.png')

		#Counter to limit number of open windows
		self.counter = 0

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
		#Menubar title
		self.menubar.add_cascade(label='Database', menu=self.filemenu)
		#Menubar option
		self.filemenu.add_command(label="Add/Remove Item", command=self.Item_Menubar)
		self.filemenu.add_command(label="Schools", command=self.Schools_Menubar)
		self.filemenu.add_separator()
		self.filemenu.add_command(label='Quit', command=quit)


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
		Add_Inventory.place(relx=.5, rely=.5,anchor= CENTER, height=55, width=250)

		Remove_Inventory = Button(Center_Left_Frame, text="Remove Inventory", command=self.Remove_Inventory_Window, font=("Arial",20), bd=3)
		Remove_Inventory.place(relx=.5, rely=.62,anchor= CENTER, height=55, width=250)

		View_Inventory = Button(Center_Left_Frame, text="View Inventory", command=self.View_Inventory_Window, font=("Arial",20), bd=3)
		View_Inventory.place(relx=.5, rely=.74,anchor= CENTER, height=55, width=250)

		Lookup_Record = Button(Center_Right_Frame, text="Add Record", command=self.Add_Record_Window, font=("Arial",20), bd=3)
		Lookup_Record.place(relx=.5, rely=.5,anchor= CENTER, height=55, width=250)

		Add_Record = Button(Center_Right_Frame, text="View record", command=self.View_Record_Window, font=("Arial",20), bd=3)
		Add_Record.place(relx=.5, rely=.74,anchor= CENTER, height=55, width=250)

		Remove_Record = Button(Center_Right_Frame, text="Remove record", command=self.Remove_Record_Window, font=("Arial",20), bd=3)
		Remove_Record.place(relx=.5, rely=.62,anchor= CENTER, height=55, width=250)


	def Remove_Inventory_Window(self):
		if self.counter < 1:
			self.counter += 1
			#Create Add Inventory Window
			self.Configure_Window_Defaults(title='Remove Inventory')

			#~~~ Add Widets ~~~
			#Create Labels
			Title_Image = Label(self.Top_Frame, image=self.Title_Image, font=("Arial",60), pady=5, bg='#f1f5f4')
			Title_Image.pack(fill=X, pady=12)

			Title_Desc = Label(self.Top_Frame, text='Remove Inventory',  font=("Arial",25), bg='#f1f5f4')
			Title_Desc.pack(fill=X)

			Item_Name = Label(self.Center_Frame, text='Item Name:', font=("Arial",23), pady=5, bg='#f5f1f2')
			Item_Name.place(relx=.42, rely=.22,anchor= CENTER, height=55, width=200)

			Item_Type = Label(self.Center_Frame, text='Item Type:', font=("Arial",23), pady=5, bg='#f5f1f2')
			Item_Type.place(relx=.42, rely=.4,anchor= CENTER, height=55, width=200)

			Item_Size = Label(self.Center_Frame, text='Item Size:', font=("Arial",23), pady=5, bg='#f5f1f2')
			Item_Size.place(relx=.42, rely=.58,anchor= CENTER, height=55, width=200)

			Item_Amount = Label(self.Center_Frame, text='Amount:', font=("Arial",22), pady=5, bg='#f5f1f2')
			Item_Amount.place(relx=.42, rely=.74,anchor= CENTER, height=55, width=200)

			Copyright = Label(self.Bottom_Frame, text='Copyright Coats for Kids 2022', font=("Arial",10), bg='#f5f1f2')
			Copyright.pack(side=BOTTOM)

			#Create Combobox Widgets
			self.Remove_Inventory_Combobox = Combobox(self.Center_Frame, state='readonly',font=("Arial",14))
			self.Remove_Inventory_Combobox.bind("<<ComboboxSelected>>", self.Update_Remove_Inventory_Type_Combobox)
			self.Remove_Inventory_Combobox['values'] = ('Hats','Coats','Gloves','Boots','Socks')
			self.Remove_Inventory_Combobox.place(relx=.58, rely=.22,anchor= CENTER)

			self.Remove_Inventory_Type_Combobox = Combobox(self.Center_Frame, state='readonly',font=("Arial",14))
			self.Remove_Inventory_Type_Combobox.bind("<<ComboboxSelected>>", self.Update_Remove_Inventory_Size_Combobox)
			self.Remove_Inventory_Type_Combobox.place(relx=.58, rely=.4,anchor= CENTER)

			self.Remove_Inventory_Size_Combobox = Combobox(self.Center_Frame, state='readonly',font=("Arial",14))
			self.Remove_Inventory_Size_Combobox.place(relx=.58, rely=.58,anchor= CENTER)

			#Create Entry Widgets
			self.Remove_Inventory_Amount_Entry = Entry(self.Center_Frame, text='Enter amount',font=("Arial",14))
			self.Remove_Inventory_Amount_Entry.place(relx=.58, rely=.74,anchor= CENTER)

			#Clear combobox and entry widgets because for some reason the inventory comboboxes are keeping values stored
			#when window is closed. All other windows besides these clear upon close. I want to clear upon close. I cannot for the life of me
			#figure out why so I am putting this here out of spite
			self.Clear_Combobox(self.Remove_Inventory_Combobox, self.Remove_Inventory_Type_Combobox, self.Remove_Inventory_Size_Combobox)
			self.Clear_Entry_box(self.Remove_Inventory_Amount_Entry)

			#Create Buttons
			Submit = Button(self.Center_Frame, text="Submit",font=("Arial",20), command=lambda: self.Btn_Remove_Inventory(self.Remove_Inventory_Combobox, self.Remove_Inventory_Type_Combobox, self.Remove_Inventory_Size_Combobox, self.Remove_Inventory_Amount_Entry), padx=10, pady=10, width=25, bd=3)
			Submit.place(relx=.5, rely=.9,anchor= CENTER, height=55, width=200)

			Exit = Button(self.Bottom_Frame, text="Go Back", font=("Arial",15), command=self.Window.destroy, bd=3)
			Exit.bind("<Button-1>", self.Reset_Counter)
			Exit.pack(pady=15, padx=45, side=LEFT)

	def Add_Inventory_Window(self):
		if self.counter < 1:
			self.counter += 1
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

			Item_Amount = Label(self.Center_Frame, text='Amount:', font=("Arial",22), pady=5, bg='#f5f1f2')
			Item_Amount.place(relx=.42, rely=.74,anchor= CENTER, height=55, width=200)

			Copyright = Label(self.Bottom_Frame, text='Copyright Coats for Kids 2022', font=("Arial",10), bg='#f5f1f2')
			Copyright.pack(side=BOTTOM)

			#Create Combobox Widgets
			self.Add_Inventory_Combobox = Combobox(self.Center_Frame, text='Select an item', state='readonly',font=("Arial",14))
			self.Add_Inventory_Combobox['values'] = ('Hats','Coats','Gloves','Boots','Socks')
			self.Add_Inventory_Combobox.bind("<<ComboboxSelected>>", self.Update_Add_Inventory_Type_Combobox)
			self.Add_Inventory_Combobox.place(relx=.58, rely=.22,anchor= CENTER)

			self.Add_Inventory_Type_Combobox = Combobox(self.Center_Frame, text='Select item type', state='readonly',font=("Arial",14))
			self.Add_Inventory_Type_Combobox.bind("<<ComboboxSelected>>", self.Update_Add_Inventory_Size_Combobox)
			self.Add_Inventory_Type_Combobox.place(relx=.58, rely=.4,anchor= CENTER)

			self.Add_Inventory_Size_Combobox = Combobox(self.Center_Frame, text='Select item size', state='readonly',font=("Arial",14))
			self.Add_Inventory_Size_Combobox.place(relx=.58, rely=.58,anchor= CENTER)

			#Create Entry Widgets
			self.Add_Inventory_Amount_Entry = Entry(self.Center_Frame, text='Enter amount',font=("Arial",14))
			self.Add_Inventory_Amount_Entry.place(relx=.58, rely=.74,anchor= CENTER)

			self.Clear_Combobox(self.Add_Inventory_Combobox, self.Add_Inventory_Type_Combobox, self.Add_Inventory_Size_Combobox)
			self.Clear_Entry_box(self.Add_Inventory_Amount_Entry)


			#Create Buttons
			#lambda: self.Add_Inventory_Record(Add_Item_Name_Combobox.get(),Add_Item_Type_Entry.get(),Add_Item_Size_Entry.get()),
			#lambda: self.Btn_Submit_Record(self.Item_Combobox, self.Item_Type_Combobox, self.Item_Size_Combobox, self.Item_Amount_Entry)
			Submit = Button(self.Center_Frame, text="Submit",font=("Arial",20), command=lambda: self.Btn_Submit_Inventory(self.Add_Inventory_Combobox, self.Add_Inventory_Type_Combobox, self.Add_Inventory_Size_Combobox, self.Add_Inventory_Amount_Entry), padx=10, pady=10, width=25, bd=3)
			Submit.place(relx=.5, rely=.9,anchor= CENTER, height=55, width=200)

			Exit = Button(self.Bottom_Frame, text="Go Back", command=self.Window.destroy, font=("Arial",15), bd=3)
			Exit.bind("<Button-1>", self.Reset_Counter)
			Exit.pack(pady=15, padx=45, side=LEFT)

	def View_Inventory_Window(self):
		if self.counter < 1:
			self.counter += 1
			#Create View Inventory Window
			self.Configure_Window_Defaults(title='View Inventory')


			#~~~ Add Widets ~~~
			#Create Labels
			Title_Image = Label(self.Top_Frame, image=self.Title_Image, font=("Arial",60), pady=5, bg='#f1f5f4')
			Title_Image.pack(fill=X, pady=12)

			Title_Desc = Label(self.Top_Frame, text='View Inventory',  font=("Arial",20), bg='#f1f5f4')
			Title_Desc.pack(fill=X)

			Search_Item = Label(self.Center_Frame, text='Search Item', font=("Arial",20), pady=5, bg='#f5f1f2')
			Search_Item.place(relx=.5, rely=.12,anchor= CENTER)

			self.View_Item_Selected = Label(self.Center_Frame, text='', font=("Arial",20), pady=5, bg='#f5f1f2')
			self.View_Item_Selected.place(relx=.42, rely=.36, anchor= CENTER)

			self.View_Total = Label(self.Center_Frame, text='', font=("Arial",20), pady=5, bg='#f5f1f2')
			self.View_Total.place(relx=.585, rely=.36,anchor= CENTER)

			self.View_Subitems = Text(self.Center_Frame, font=("Arial",20), bg='#f5f1f2', width=30, height=6)
			self.View_Subitems.place(relx=.5, rely=.75,anchor= CENTER)

			Separator = Label(self.Center_Frame, text=self.Underscore(35),  font=("Arial",15), bg='#f5f1f2')
			Separator.place(relx=.35, rely=.4)

			Copyright = Label(self.Bottom_Frame, text='Copyright Coats for Kids 2022', font=("Arial",10), bg='#f5f1f2')
			Copyright.pack(side=BOTTOM)

			#Create Entry Boxes
			self.View_Select_Item_CB = Combobox(self.Center_Frame, text='Inventory Item', state='readonly', font=("Arial",14))
			self.View_Select_Item_CB['values'] = ('Hats','Coats','Gloves','Boots','Socks')
			self.View_Select_Item_CB.place(relx=.5, rely=.2,anchor= CENTER)

			#Create buttons
			Select = Button(self.Center_Frame, text="Search", font=("Arial", 14), command=lambda: self.Btn_View_Inventory(self.View_Select_Item_CB.get()), padx=5, pady=5, bd=3)
			Select.place(relx=.625, rely=.2,anchor= CENTER)

			self.Clear_Combobox(self.View_Select_Item_CB)


			Exit = Button(self.Bottom_Frame, text="Go Back", font=("Arial",15), command=self.Window.destroy, bd=3)
			Exit.bind("<Button-1>", self.Reset_Counter)
			Exit.pack(pady=15, padx=45, side=LEFT)


	def Remove_Record_Window(self):
		if self.counter < 1:
			self.counter += 1
			#Create Add Inventory Window
			self.Configure_Window_Defaults(title='Remove Inventory')

			#~~~ Add Widets ~~~
			#Create Labels
			Title_Image = Label(self.Top_Frame, image=self.Title_Image, font=("Arial",60), pady=5, bg='#f1f5f4')
			Title_Image.pack(fill=X, pady=12)

			Title_Desc = Label(self.Top_Frame, text='Remove Inventory',  font=("Arial",25), bg='#f1f5f4')
			Title_Desc.pack(fill=X)

			Record = Label(self.Center_Frame, text='Select a record to delete', font=("Arial",23), pady=5, bg='#f5f1f2')
			Record.place(relx=.5, rely=.4,anchor= CENTER, height=55)

			Copyright = Label(self.Bottom_Frame, text='Copyright Coats for Kids 2022', font=("Arial",10), bg='#f5f1f2')
			Copyright.pack(side=BOTTOM)

			#Create Combobox Widgets

			self.Remove_Record_Combobox = Combobox(self.Center_Frame, state='readonly',font=("Arial",14))
			self.Remove_Record_Combobox['values'] = Queries.Populate_Record_CName_Id()
			#self.Record_Combobox.bind("<<ComboboxSelected>>", self.Update_Remove_Inventory_Size_Combobox)
			self.Remove_Record_Combobox.place(relx=.5, rely=.55,anchor= CENTER)


			#Clear combobox and entry widgets because for some reason the inventory comboboxes are keeping values stored
			#when window is closed. All other windows besides these clear upon close. I want to clear upon close. I cannot for the life of me
			#figure out why so I am putting this here out of spite
			self.Clear_Combobox(self.Remove_Record_Combobox)

			#Create Buttons
			Submit = Button(self.Center_Frame, text="Submit",font=("Arial",20), command=lambda: self.Btn_Remove_Record(self.Remove_Record_Combobox), padx=10, pady=10, width=25, bd=3)
			Submit.place(relx=.5, rely=.9,anchor= CENTER, height=55, width=200)

			Exit = Button(self.Bottom_Frame, text="Go Back", font=("Arial",15), command=self.Window.destroy, bd=3)
			Exit.bind("<Button-1>", self.Reset_Counter)
			Exit.pack(pady=15, padx=45, side=LEFT)

	def Add_Record_Window(self):
		if self.counter < 1:
			self.counter += 1
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
			self.Child_First_Entry = Entry(self.Center_Frame, font=("Arial",13))
			self.Child_First_Entry.place(relx=.24, rely=.19,anchor= CENTER)

			self.Child_Last_Entry = Entry(self.Center_Frame, font=("Arial",13))
			self.Child_Last_Entry.place(relx=.42, rely=.19,anchor= CENTER)

			self.Child_Age_Entry = Entry(self.Center_Frame, font=("Arial",13))
			self.Child_Age_Entry.place(relx=.55, rely=.19,anchor= CENTER, width='50')

			self.Parent_First_Entry = Entry(self.Center_Frame, font=("Arial",13))
			self.Parent_First_Entry.place(relx=.14, rely=.39,anchor= CENTER)

			self.Parent_Last_Entry = Entry(self.Center_Frame, font=("Arial",13))
			self.Parent_Last_Entry.place(relx=.31, rely=.39,anchor= CENTER)

			self.Phone_Entry = Entry(self.Center_Frame, font=("Arial",13))
			self.Phone_Entry.place(relx=.48, rely=.39,anchor= CENTER)

			self.Street_Entry = Entry(self.Center_Frame, font=("Arial",13))
			self.Street_Entry.place(relx=.65, rely=.39,anchor= CENTER)

			self.City_Entry = Entry(self.Center_Frame, font=("Arial",13))
			self.City_Entry.place(relx=.8, rely=.39,anchor= CENTER, width='150')

			self.Zip_Entry = Entry(self.Center_Frame, font=("Arial",13))
			self.Zip_Entry.place(relx=.9, rely=.39,anchor= CENTER, width='75')

			#Create Combobox Widgets
			#User input is required to fill values for all but gender combobox
			self.Gender_Combobox = Combobox(self.Center_Frame, text='Select Gender', state='readonly')
			self.Gender_Combobox['values'] = ('Male','Female','Other')
			self.Gender_Combobox.place(relx=.63, rely=.19,anchor= CENTER, width='65')

			self.School_Combobox = Combobox(self.Center_Frame, text='Select School', state='readonly')
			self.School_Combobox['values'] = Queries.Grab_Schools()
			self.School_Combobox.place(relx=.72, rely=.19,anchor= CENTER, width='100')

			self.Hat_Combobox = Combobox(self.Center_Frame, text='Select Hat', state='readonly')
			self.Hat_Combobox['values'] = Queries.Populate_Add_Record_CBs('Hats')
			self.Hat_Combobox.place(relx=.33, rely=.61,anchor= CENTER)

			self.Coat_Combobox = Combobox(self.Center_Frame, text='Select Coat', state='readonly')
			self.Coat_Combobox['values'] = Queries.Populate_Add_Record_CBs('Coats')
			self.Coat_Combobox.place(relx=.50, rely=.61,anchor= CENTER)

			self.Gloves_Combobox = Combobox(self.Center_Frame, text='Select Gloves', state='readonly')
			self.Gloves_Combobox['values'] = Queries.Populate_Add_Record_CBs('Gloves')
			self.Gloves_Combobox.place(relx=.66, rely=.61,anchor= CENTER)

			self.Socks_Combobox = Combobox(self.Center_Frame, text='Select Socks', state='readonly')
			self.Socks_Combobox['values'] = Queries.Populate_Add_Record_CBs('Socks')
			self.Socks_Combobox.place(relx=.4, rely=.8,anchor= CENTER)

			self.Boots_Combobox = Combobox(self.Center_Frame, text='Select Boots', state='readonly')
			self.Boots_Combobox['values'] = Queries.Populate_Add_Record_CBs('Boots')
			self.Boots_Combobox.place(relx=.6, rely=.8,anchor= CENTER)


			#Create Buttons
			Exit = Button(self.Bottom_Frame, text="Go Back", font=("Arial",15), command=self.Window.destroy, bd=3)
			Exit.bind("<Button-1>", self.Reset_Counter)
			Exit.pack(pady=15, padx=45, side=LEFT)


			Submit = Button(self.Center_Frame, text="Submit Record", font=("Arial",15), command=lambda:self.Btn_Submit_Record(self.Child_First_Entry, self.Child_Last_Entry, self.Child_Age_Entry, self.Gender_Combobox, self.School_Combobox,
						self.Parent_First_Entry, self.Parent_Last_Entry, self.Phone_Entry, self.Street_Entry, self.City_Entry, self.Zip_Entry,
						self.Hat_Combobox, self.Coat_Combobox, self.Gloves_Combobox, self.Socks_Combobox, self.Boots_Combobox), bd=3)
			Submit.place(relx=.5,rely=.93,anchor=CENTER)

			#Clear combobox and entry widgets because for some reason the inventory comboboxes are keeping values stored
			#when window is closed. All other windows besides these clear upon close. I want to clear upon close. I cannot for the life of me
			#figure out why so I am putting this here out of spite
			self.Clear_Combobox(self.Gender_Combobox, self.School_Combobox, self.Hat_Combobox, self.Coat_Combobox, self.Gloves_Combobox, self.Socks_Combobox, self.Boots_Combobox)

	def View_Record_Window(self):
		if self.counter < 1:
			self.counter += 1
			#Create View Record Window
			self.Configure_Window_Defaults(title='View Record')


			#~~~ Add Widets ~~~
			#Create Labels
			Title_Image = Label(self.Top_Frame, image=self.Title_Image, font=("Arial",60), pady=5, bg='#f1f5f4')
			Title_Image.pack(fill=X, pady=12)

			Title_Description = Label(self.Top_Frame, text='View Inventory',  font=("Arial",20), bg='#f1f5f4')
			Title_Description.pack(fill=X)

			Search = Label(self.Center_Frame, text='Search records by child name', font=("Arial",20), pady=5, bg='#f5f1f2')
			Search.place(relx=.5, rely=.12,anchor= CENTER)

			Separator = Label(self.Center_Frame, text=self.Underscore(35),  font=("Arial",15), bg='#f5f1f2')
			Separator.place(relx=.35, rely=.3)

			Copyright = Label(self.Bottom_Frame, text='Copyright Coats for Kids 2022', font=("Arial",10), bg='#f5f1f2')
			Copyright.pack(side=BOTTOM)


			self.Records_List = Combobox(self.Center_Frame, text='Select Gloves', state='readonly')
			self.Records_List['values'] = Queries.Populate_Record_CName_Id()
			self.Records_List.place(relx=.5, rely=.22,anchor= CENTER)

			#Clear combobox so values do not stay populated when window is closed and reopened
			self.Clear_Combobox(self.Records_List)

			self.View_Child_First = Label(self.Center_Frame, text='Childs First: ', font=("Arial",20), pady=5, bg='#f5f1f2')
			self.View_Child_First.place(relx=.2, rely=.45,anchor= CENTER)

			self.View_Child_Last = Label(self.Center_Frame, text='Childs Last: ', font=("Arial",20), pady=5, bg='#f5f1f2')
			self.View_Child_Last.place(relx=.2, rely=.55,anchor= CENTER)

			self.View_Child_Age = Label(self.Center_Frame, text='Childs Age: ', font=("Arial",20), pady=5, bg='#f5f1f2')
			self.View_Child_Age.place(relx=.2, rely=.65,anchor= CENTER)

			self.View_Child_Gender = Label(self.Center_Frame, text='Childs Gender: ', font=("Arial",20), pady=5, bg='#f5f1f2')
			self.View_Child_Gender.place(relx=.2, rely=.75,anchor= CENTER)

			self.View_Child_School = Label(self.Center_Frame, text='Childs Schools: ', font=("Arial",20), pady=5, bg='#f5f1f2')
			self.View_Child_School.place(relx=.2, rely=.85,anchor= CENTER)

			self.View_Parent_First = Label(self.Center_Frame, text='Parents First: ', font=("Arial",20), pady=5, bg='#f5f1f2')
			self.View_Parent_First.place(relx=.5, rely=.45,anchor= CENTER)

			self.View_Parent_Last = Label(self.Center_Frame, text='Parents Last: ', font=("Arial",20), pady=5, bg='#f5f1f2')
			self.View_Parent_Last.place(relx=.5, rely=.55,anchor= CENTER)

			self.View_Parent_Phone = Label(self.Center_Frame, text='Parents Phone: ', font=("Arial",20), pady=5, bg='#f5f1f2')
			self.View_Parent_Phone.place(relx=.5, rely=.65,anchor= CENTER)

			self.View_Parent_Street = Label(self.Center_Frame, text='Parents Street: ', font=("Arial",20), pady=5, bg='#f5f1f2')
			self.View_Parent_Street.place(relx=.5, rely=.75,anchor= CENTER)

			self.View_Parent_City = Label(self.Center_Frame, text='Parents City: ', font=("Arial",20), pady=5, bg='#f5f1f2')
			self.View_Parent_City.place(relx=.5, rely=.85,anchor= CENTER)

			self.View_Parent_Zip = Label(self.Center_Frame, text='Parents Zip: ', font=("Arial",20), pady=5, bg='#f5f1f2')
			self.View_Parent_Zip.place(relx=.5, rely=.95,anchor= CENTER)

			self.View_Hat = Label(self.Center_Frame, text='Hat: ', font=("Arial",20), pady=5, bg='#f5f1f2')
			self.View_Hat.place(relx=.8, rely=.45,anchor= CENTER)

			self.View_Coat = Label(self.Center_Frame, text='Coat: ', font=("Arial",20), pady=5, bg='#f5f1f2')
			self.View_Coat.place(relx=.8, rely=.55,anchor= CENTER)

			self.View_Gloves = Label(self.Center_Frame, text='Gloves: ', font=("Arial",20), pady=5, bg='#f5f1f2')
			self.View_Gloves.place(relx=.8, rely=.65,anchor= CENTER)

			self.View_Socks = Label(self.Center_Frame, text='Socks: ', font=("Arial",20), pady=5, bg='#f5f1f2')
			self.View_Socks.place(relx=.8, rely=.75,anchor= CENTER)

			self.View_Boots = Label(self.Center_Frame, text='Boots: ', font=("Arial",20), pady=5, bg='#f5f1f2')
			self.View_Boots.place(relx=.8, rely=.85,anchor= CENTER)

			self.View_Id = Label(self.Center_Frame, text='Record ID: ', font=("Arial",20), pady=5, bg='#f5f1f2')
			self.View_Id.place(relx=.8, rely=.95,anchor= CENTER)

			#Create buttons
			Submit = Button(self.Center_Frame, text="Search", command=lambda: self.Btn_View_Record(self.Records_List), padx=5, pady=5, font=("Arial", 12), bd=3)
			Submit.place(relx=.62, rely=.22,anchor= CENTER)

			Exit = Button(self.Bottom_Frame, text="Go Back", font=("Arial",15), command=self.Window.destroy, bd=3)
			Exit.bind("<Button-1>", self.Reset_Counter)
			Exit.pack(pady=15, padx=45, side=LEFT)


	##### MENU BARS #####
	def Item_Menubar(self):
		if self.counter < 1:
			self.counter += 1
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
			self.Add_Item_Type_Entry = Entry(self.Center_Frame, font=("Arial",14), width=15)
			self.Add_Item_Type_Entry.place(relx=.35, rely=.39,anchor= CENTER)

			self.Add_Item_Size_Entry = Entry(self.Center_Frame, font=("Arial",14), width=15)
			self.Add_Item_Size_Entry.place(relx=.55, rely=.39,anchor= CENTER)

			#Create Comboboxes
			self.Add_Item_Name_Combobox = Combobox(self.Center_Frame, state='readonly', width=15)
			self.Add_Item_Name_Combobox.bind("<<ComboboxSelected>>", self.Disable_Enable_Entry_Box)
			self.Add_Item_Name_Combobox['values'] = ('Coats','Gloves','Boots','Hats','Socks')
			self.Add_Item_Name_Combobox.place(relx=.15, rely=.39,anchor= CENTER)


			self.Remove_Item_Name_Combobox = Combobox(self.Center_Frame, state='readonly', width=15)
			self.Remove_Item_Name_Combobox['values'] = ('Coats','Gloves','Boots','Hats','Socks')
			self.Remove_Item_Name_Combobox.bind("<<ComboboxSelected>>", self.Update_Remove_Item_Type_Combobox)
			self.Remove_Item_Name_Combobox.place(relx=.15, rely=.79,anchor= CENTER)

			self.Remove_Item_Type_Combobox = Combobox(self.Center_Frame, state='readonly', width=15)
			self.Remove_Item_Type_Combobox.bind("<<ComboboxSelected>>", self.Update_Remove_Item_Size_Combobox)
			self.Remove_Item_Type_Combobox.place(relx=.35, rely=.79,anchor= CENTER)

			self.Remove_Item_Size_Combobox = Combobox(self.Center_Frame, state='readonly', width=15)
			self.Remove_Item_Size_Combobox.place(relx=.55, rely=.79,anchor= CENTER)

			#Create Buttons
			#Lambda is required so that the buttons command is not ran upon window creation
			#https://stackoverflow.com/questions/8269096/why-is-button-parameter-command-executed-when-declared
			#Passing tkinter objects instead of values bc i'll pass the entry boxes to the clear entry box function
			Add_Item_Submit_Btn = Button(self.Center_Frame, text="Submit", font=("Arial",14), command=lambda: self.Btn_Submit_Item(self.Add_Item_Name_Combobox,self.Add_Item_Type_Entry,self.Add_Item_Size_Entry), bd=2)
			Add_Item_Submit_Btn.place(relx=.75, rely=.37,anchor= CENTER)

			Remove_Item_Submit_Btn = Button(self.Center_Frame, text="Submit", font=("Arial",14), command=lambda: self.Btn_Remove_Item(self.Remove_Item_Name_Combobox,self.Remove_Item_Type_Combobox,self.Remove_Item_Size_Combobox), bd=2)
			Remove_Item_Submit_Btn.place(relx=.75, rely=.77,anchor= CENTER)

			Exit = Button(self.Bottom_Frame, text="Go Back", font=("Arial",15), command=self.Window.destroy, bd=2)
			Exit.bind("<Button-1>", self.Reset_Counter)
			Exit.pack(pady=15, padx=45, side=LEFT)

	def Schools_Menubar(self):
		if self.counter < 1:
			self.counter += 1
			self.Configure_Window_Defaults(window_name='Schools_Menubar', title='Schools', geometry='800x600')

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
			self.Add_School_Entry = Entry(self.Center_Frame, font=("Arial",14), width=15)
			self.Add_School_Entry.place(relx=.5, rely=.39,anchor= CENTER)

			#Create Combobox
			self.Remove_School_Combobox = Combobox(self.Center_Frame, state='readonly', width=15)
			self.Remove_School_Combobox['values'] = (Queries.Grab_Schools())
			self.Remove_School_Combobox.place(relx=.5, rely=.79,anchor= CENTER)

			#Create Buttons
			Add_School_Submit = Button(self.Center_Frame, text="Submit", font=("Arial",14), command=lambda: self.Btn_Submit_School(self.Add_School_Entry), bd=2)
			Add_School_Submit.place(relx=.75, rely=.37,anchor= CENTER)

			Remove_School_Submit = Button(self.Center_Frame, text="Submit", font=("Arial",14), command=lambda: self.Btn_Remove_School(self.Remove_School_Combobox), bd=2)
			Remove_School_Submit.place(relx=.75, rely=.77,anchor= CENTER)

			Exit = Button(self.Bottom_Frame, text="Go Back", font=("Arial",15), command=self.Window.destroy, bd=2)
			Exit.bind("<Button-1>", self.Reset_Counter)
			Exit.pack(pady=15, padx=45, side=LEFT)

	##### POP-UP WINDOWS #####
	def Notification_Window(self, text):
		self.Configure_Window_Defaults(title='Notification', geometry='640x200')

		#~~~ Add Widets ~~~
		#Create Labels
		Main_Label = Label(self.Center_Frame, text=text, font=("Arial",18), pady=5, bg='#f5f1f2')
		Main_Label.place(relx=.5, rely=.5,anchor= CENTER, height=55)

		#Create Buttons
		Exit = Button(self.Bottom_Frame, text="Go Back", font=("Arial",13), command=self.Window.destroy, bd=2)
		Exit.pack(pady=15, padx=45)
	########################################################################

#Exit if this is not being ran as main script
if __name__ == "__main__":
	Application()
else:
	quit()
