from tkinter import *
from tkinter import ttk
import Login
import os
import sqlite3
import tkinter.messagebox as tmsg
import datetime

class Customer_page(Tk):
  def __init__(self,emailId):
    super().__init__()
    self.geometry("%dx%d+0+0" % (self.winfo_screenwidth(), self.winfo_screenheight()))
    self.title(f"Welcome to Maharaja Hotel, Customer {emailId}")
    self.wm_iconbitmap("Burger.ico")

    style_button = ttk.Style()
    style_button.configure("TButton",font = ("arial",10,"bold"),background="lightgreen")
  
    self.customerEmail = emailId

    db = sqlite3.connect('../hotel_database.db')
    cursor = db.cursor()
    cursor.execute("select distinct category from menu;")
    menu_categories = cursor.fetchall()
    self.menu_category = []
    for i in menu_categories:
      self.menu_category.append(str(i[0]))

    self.order_dict = {}
    for i in self.menu_category:
        self.order_dict[i] = {}

    #================Title==============
    title_frame = Frame(self, bd=8, bg="yellow", relief=GROOVE)
    title_frame.pack(side=TOP, fill="x")
    
    logout_frame = Frame(title_frame, bg="yellow")
    logout_frame.pack(side='right')
    
    login_name = Label(logout_frame,text=emailId,
                       font=("arial", 15, "bold"),bg = "yellow")
    login_name.grid(row=0,column=0)
    
    logout_button = ttk.Button(logout_frame, text="LOGOUT"
                            ,command=self.logout_operation)
    logout_button.grid(row=0,column=1,padx=10)
    
    title_label = Label(title_frame, text="Maharaja Hotel", 
                        font=("times new roman", 20, "bold"),bg = "yellow", fg="red", pady=5)
    title_label.pack()
    
    #===============Menu===============
    menu_frame = Frame(self,bd=8, bg="lightgreen", relief=GROOVE,width=(self.winfo_screenwidth()//2))
    menu_frame.pack(side='left',fill='both')
    
    menu_label = Label(menu_frame, text="Menu", 
                        font=("times new roman", 18, "bold"),bg = "lightgreen", fg="red", pady=0)
    menu_label.pack(side=TOP,fill="x")
    
    menu_category_frame = Frame(menu_frame,bg="lightgreen",pady=10)
    menu_category_frame.pack(fill="x")
    
    combo_lable = Label(menu_category_frame,text="Select Type", 
                        font=("arial", 12, "bold"),bg = "lightgreen", fg="blue")
    combo_lable.grid(row=0,column=0,padx=10)
    
    self.menuCategory = StringVar()

    combo_menu = ttk.Combobox(menu_category_frame,values=self.menu_category,
                                textvariable=self.menuCategory)
    combo_menu.grid(row=0,column=1,padx=30)
    
    show_button = ttk.Button(menu_category_frame, text="Show",width=10,
                            command=self.show_button_operation)
    show_button.grid(row=0,column=2,padx=60)
    
    show_all_button = ttk.Button(menu_category_frame, text="Show All",
                            width=10,command=self.load_menu)
    show_all_button.grid(row=0,column=3,padx=(10,50))
    
    ############################# Menu Tabel ##########################################
    menu_tabel_frame = Frame(menu_frame,bd=2, relief=SUNKEN)
    menu_tabel_frame.pack(fill=BOTH,expand=1)
    
    scrollbar_menu_x = Scrollbar(menu_tabel_frame,orient=HORIZONTAL)
    scrollbar_menu_y = Scrollbar(menu_tabel_frame,orient=VERTICAL)
    
    style = ttk.Style()
    style.configure("Treeview.Heading",font=("arial",13, "bold"))
    style.configure("Treeview",font=("arial",12),rowheight=25)
    
    self.menu_tabel = ttk.Treeview(menu_tabel_frame,style = "Treeview",
                columns =("name","price","category"),xscrollcommand=scrollbar_menu_x.set,
                yscrollcommand=scrollbar_menu_y.set)
    
    self.menu_tabel.heading("name",text="Name")
    self.menu_tabel.heading("price",text="Price")
    self.menu_tabel["displaycolumns"]=("name", "price")
    self.menu_tabel["show"] = "headings"
    self.menu_tabel.column("price",width=50,anchor='center')
    
    scrollbar_menu_x.pack(side=BOTTOM,fill=X)
    scrollbar_menu_y.pack(side=RIGHT,fill=Y)
    
    scrollbar_menu_x.configure(command=self.menu_tabel.xview)
    scrollbar_menu_y.configure(command=self.menu_tabel.yview)
    
    self.menu_tabel.pack(fill=BOTH,expand=1)
    
    
    #menu_tabel.insert('',END,values=["Masala Dosa","50"])
    self.load_menu()
    self.menu_tabel.bind("<ButtonRelease-1>",self.load_item_from_menu)
    
    ###########################################################################################
    
    #===============Item Frame=============
    item_frame = Frame(self,bd=8, bg="lightgreen", relief=GROOVE)
    item_frame.pack(fill='x',anchor=SE)
    
    item_title_label = Label(item_frame, text="Item", 
                        font=("times new roman", 18, "bold"),bg = "lightgreen", fg="red")
    item_title_label.pack(side=TOP,fill="x")
    
    item_frame2 = Frame(item_frame, bg="lightgreen")
    item_frame2.pack(fill=X)
    
    item_name_label = Label(item_frame2, text="Name", 
                        font=("arial", 12, "bold"),bg = "lightgreen", fg="blue")
    item_name_label.grid(row=0,column=0,padx=(30,10))
    
    self.itemCategory = StringVar()
    self.itemCategory.set("")
    
    self.itemName = StringVar()
    self.itemName.set("")
    item_name = Entry(item_frame2, font="arial 12",textvariable=self.itemName,state=DISABLED, width=25)
    item_name.grid(row=0,column=1,padx=(0,10))
    
    item_rate_label = Label(item_frame2, text="Rate", 
                        font=("arial", 12, "bold"),bg = "lightgreen", fg="blue")
    item_rate_label.grid(row=0,column=2,padx=(40,10))
    
    self.itemRate = StringVar()
    self.itemRate.set("")
    item_rate = Entry(item_frame2, font="arial 12",textvariable=self.itemRate,state=DISABLED, width=10)
    item_rate.grid(row=0,column=3,padx=0)
    
    item_quantity_label = Label(item_frame2, text="Quantity", 
                        font=("arial", 12, "bold"),bg = "lightgreen", fg="blue")
    item_quantity_label.grid(row=1,column=0,padx=(30,0),pady=15)
    
    self.itemQuantity = StringVar()
    self.itemQuantity.set("")
    item_quantity = Entry(item_frame2, font="arial 12",textvariable=self.itemQuantity, width=10)
    item_quantity.grid(row=1,column=1,padx=0)
    
    item_frame3 = Frame(item_frame, bg="lightgreen")
    item_frame3.pack(fill=X)
    
    add_button = ttk.Button(item_frame3, text="Add Item"
                            ,command=self.add_button_operation)
    add_button.grid(row=0,column=0,padx=(40,25),pady=30)
    
    remove_button = ttk.Button(item_frame3, text="Remove Item"
                            ,command=self.remove_button_operation)
    remove_button.grid(row=0,column=1,padx=25,pady=30)
    
    update_button = ttk.Button(item_frame3, text="Update Quantity"
                            ,command=self.update_button_operation)
    update_button.grid(row=0,column=2,padx=25,pady=30)
    
    clear_button = ttk.Button(item_frame3, text="Clear",
                            width=8,command=self.clear_button_operation)
    clear_button.grid(row=0,column=3,padx=25,pady=30)
    
    #==============Order Frame=====================
    order_frame = Frame(self,bd=8, bg="lightgreen", relief=GROOVE)
    order_frame.pack(fill='both',anchor=SE,expand=True)
    
    order_title_label = Label(order_frame, text="Your Order", 
                        font=("times new roman", 18, "bold"),bg = "lightgreen", fg="red")
    order_title_label.pack(side=TOP,fill="x")
    
    ############################## Order Tabel ###################################
    order_tabel_frame = Frame(order_frame, bd=2, relief=SUNKEN)
    order_tabel_frame.pack(fill='x')
    
    scrollbar_order_x = Scrollbar(order_tabel_frame,orient=HORIZONTAL)
    scrollbar_order_y = Scrollbar(order_tabel_frame,orient=VERTICAL)
    
    self.order_tabel = ttk.Treeview(order_tabel_frame,
                columns =("name","rate","quantity","price","category"),xscrollcommand=scrollbar_order_x.set,
                yscrollcommand=scrollbar_order_y.set)
    
    self.order_tabel.heading("name",text="Name")
    self.order_tabel.heading("rate",text="Rate")
    self.order_tabel.heading("quantity",text="Quantity")
    self.order_tabel.heading("price",text="Price")
    self.order_tabel["displaycolumns"]=("name", "rate","quantity","price")
    self.order_tabel["show"] = "headings"
    self.order_tabel.column("rate",width=100,anchor='center', stretch=NO)
    self.order_tabel.column("quantity",width=100,anchor='center', stretch=NO)
    self.order_tabel.column("price",width=100,anchor='center', stretch=NO)
    
    self.order_tabel.bind("<ButtonRelease-1>",self.load_item_from_order)
    
    scrollbar_order_x.pack(side=BOTTOM,fill=X)
    scrollbar_order_y.pack(side=RIGHT,fill=Y)
    
    scrollbar_order_x.configure(command=self.order_tabel.xview)
    scrollbar_order_y.configure(command=self.order_tabel.yview)
    
    self.order_tabel.pack(fill=BOTH,expand=1)
    
    # order_tabel.insert('',END,text="HEllo",values=["Masala Dosa","50","2","100"])
    ###########################################################################################
    
    total_price_label = Label(order_frame, text="Total Price", 
                        font=("arial", 12, "bold"),bg = "lightgreen", fg="blue")
    total_price_label.pack(side='left',anchor=N,padx=(20,5),pady=20)
    
    self.totalPrice = StringVar()
    self.totalPrice.set("")
    total_price_entry = Entry(order_frame, font="arial 12",textvariable=self.totalPrice,state=DISABLED, 
                                width=10)
    total_price_entry.pack(side='left',anchor=N,padx=0,pady=20)
    
    place_order_button = ttk.Button(order_frame, text="Place Order",
                            command=self.place_order_button_operation)
    place_order_button.pack(side='left',anchor=N,padx=50,pady=20)
    
    cancel_button = ttk.Button(order_frame, text="Delete Order",command=self.cancel_button_operation)
    cancel_button.pack(side='left',anchor=N,padx=0,pady=20)
    
    #====================Frontend code ends=====================
        
  def show_button_operation(self):
    category = self.menuCategory.get()
    if category not in self.menu_category:
        tmsg.showinfo("Error", "Please select valid Choice")
    else:
      self.menu_tabel.delete(*self.menu_tabel.get_children())
      db = sqlite3.connect('../hotel_database.db')
      cursor = db.cursor()
      cursor.execute(f"select * from menu where category='{category}';")
      rows = cursor.fetchall()
      for row in rows:
        self.menu_tabel.insert('',END,values=row)
    
  def load_menu(self):
    self.menu_tabel.delete(*self.menu_tabel.get_children())
    self.menuCategory.set("")
    db = sqlite3.connect('../hotel_database.db')
    cursor1 = db.cursor()
    cursor2 = db.cursor()
    cursor1.execute("select distinct category from menu;")
    categories = cursor1.fetchall()
    for category in categories:
      cursor2.execute(f"select * from menu where category='{category[0]}';")
      rows = cursor2.fetchall()
      name = "\t\t"+str(category[0])
      price = ""
      self.menu_tabel.insert('',END,values=[name,price,category[0]])
      for row in rows:
        self.menu_tabel.insert('',END,values=row)

  def load_item_from_menu(self,event):
    cursor_row = self.menu_tabel.focus()
    contents = self.menu_tabel.item(cursor_row)
    row = contents["values"]

    self.itemName.set(str(row[0]))
    self.itemRate.set(row[1])
    self.itemCategory.set(row[2])
    self.itemQuantity.set("1")

  def add_button_operation(self):
    name = self.itemName.get()
    rate = self.itemRate.get()
    category = self.itemCategory.get()
    quantity = self.itemQuantity.get()
    if name=="":
      return
    if name in self.order_dict[category].keys():
        tmsg.showinfo("Error", "Item already exist in your order")
        return
    if not quantity.isdigit():
        tmsg.showinfo("Error", "Please Enter Valid Quantity")
        return
    lis = [name,rate,quantity,str(int(rate)*int(quantity)),category]
    self.order_dict[category][name] = lis
    self.load_order()

  def remove_button_operation(self):
    name = self.itemName.get()
    category = self.itemCategory.get()
    if category=="":
        return
    if name not in self.order_dict[category].keys():
        tmsg.showinfo("Error", "Item is not in your order list")
        return
    del self.order_dict[category][name]
    self.load_order()

  def update_button_operation(self):
    name = self.itemName.get()
    rate = self.itemRate.get()
    category = self.itemCategory.get()
    quantity = self.itemQuantity.get()
    if category=="":
        return
    if name not in self.order_dict[category].keys():
        tmsg.showinfo("Error", "Item is not in your order list")
        return
    if self.order_dict[category][name][2]==quantity:
        tmsg.showinfo("Error", "No changes in Quantity")
        return
    self.order_dict[category][name][2] = quantity
    self.order_dict[category][name][3] = str(int(rate)*int(quantity))
    self.load_order()

  def clear_button_operation(self):
    self.itemName.set("")
    self.itemRate.set("")
    self.itemQuantity.set("")
    self.itemCategory.set("")

  def load_item_from_order(self,event):
    cursor_row = self.order_tabel.focus()
    contents = self.order_tabel.item(cursor_row)
    row = contents["values"]
    self.itemName.set(row[0])
    self.itemRate.set(row[1])
    self.itemQuantity.set(row[2])
    self.itemCategory.set(row[4])

  def load_order(self):
    self.order_tabel.delete(*self.order_tabel.get_children())
    for category in self.order_dict.keys():
        if self.order_dict[category]:
            for lis in self.order_dict[category].values():
                self.order_tabel.insert('',END,values=lis)
    self.update_total_price()

  def update_total_price(self):
    price = 0
    for i in self.menu_category:
        for j in self.order_dict[i].keys():
            price += int(self.order_dict[i][j][3])
    if price == 0:
        self.totalPrice.set("")
    else:
        self.totalPrice.set("Rs. "+str(price)+"  /-")

  def place_order_button_operation(self):
    names = []
    for i in self.menu_category:
        names.extend(list(self.order_dict[i].keys()))
    if len(names)==0:
        tmsg.showinfo("Error", "Your order list is Empty")
        return
    ans = tmsg.askquestion("Place Order", "Are You Sure to Place Order?")
    ans = "yes"
    if ans=="yes":
      x = datetime.datetime.now()
      order_no = str(str(self.customerEmail) + ';' + x.strftime("%d") + '/' +
                  x.strftime("%m") + '/' + x.strftime("%Y") + ';' +
                  x.strftime("%H") + ':' + x.strftime("%M") + ':' + x.strftime("%S"))
      db = sqlite3.connect('../hotel_database.db')
      cursor = db.cursor()
      date_time_cursor = db.cursor()
      date_time_cursor.execute("SELECT datetime('now');")
      date,time = date_time_cursor.fetchall()[0][0].split(' ')
      cursor.execute(f"insert into orders values('{order_no}','{date}','{time}','{self.customerEmail}');")
      db.commit()
      db = sqlite3.connect('../hotel_database.db')
      items_cursor = db.cursor()
      for i in self.menu_category:
        for j in self.order_dict[i].keys():
          lis = self.order_dict[i][j]
          name = lis[0]
          rate = int(lis[1])
          quantity = int(lis[2])
          category = lis[4]
          items_cursor.execute(f"insert into items values('{name}',{rate},{quantity},'{order_no}','Not Completed','{category}')")
          db.commit()
      tmsg.showinfo("Successful", "Your order has been placed")
      self.logout_operation()

  def cancel_button_operation(self):
    ans = tmsg.askquestion("Generate Bill", "Are You Sure to Cancel Order?")
    if ans=="yes":
      for i in self.order_dict.keys():
        del self.order_dict[i]
      self.load_order()
  
  def logout_operation(self):
    self.destroy()
    self = Login.Login_page()
    
'''
# For Test
if __name__=="__main__":
  root = Customer_page('Demo_Customer')
  root.mainloop()
'''