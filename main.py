from tkinter import *
import tkinter.messagebox as messagebox
import pymongo

#setting up the connection database and collections

global url 
url = "mongodb://localhost:27017/"
db = pymongo.MongoClient(url)
db_name = "crud_db"
crud_db = db[db_name]
collection_name="student"
student = crud_db[collection_name]

#funtions

def create():
    name = ename.get()
    prn = eprn.get()
    phone = ephone.get()
    if(name=="" or prn=="" or phone==""):
        messagebox.showinfo("Create","All fiels are required")
    else:
        read = student.find_one({'prn':prn})
        if(read):
            messagebox.showinfo("Create","Student with this prn allready present")
            ename.delete(0,END)
            eprn.delete(0,END)
            ephone.delete(0,END)
        else:
            data = {
                'name': name,
                'prn':prn,
                'phone':phone
            }
            student.insert_one(data)
            messagebox.showinfo("Create","Data Inserted successfully")
            ename.delete(0,END)
            eprn.delete(0,END)
            ephone.delete(0,END)

def reset():
    ename.delete(0,END)
    eprn.delete(0,END)
    ephone.delete(0,END)
def update():
    name = ename.get()
    prn = eprn.get()
    phone = ephone.get()
    if(name=="" or prn=="" or phone==""):
        messagebox.showinfo("Create","All fiels are required")
    else:
        read = student.find_one({'prn':prn})
        if(read):
            current = student.find_one({'prn':prn})
            new={'$set':{'name':name,'phone':phone}}
            student.update_one(current,new)
            messagebox.showinfo("Create","Studnet Data Updated successfully")
            ename.delete(0,END)
            eprn.delete(0,END)
            ephone.delete(0,END)
        else:
            messagebox.showinfo("Update",f"NO student with {prn} exists")
            eprn.delete(0,END)

def read():
    data = student.find({})
    list_of_list = []
    name = []
    prn = []
    phone = []
    for i in data:
        name.append(i['name'])
        prn.append(i['prn'])
        phone.append(i['phone'])
    list_of_list.append(name)
    list_of_list.append(prn)
    list_of_list.append(phone)
    if(data):
        subwindow = Toplevel(root)
        subwindow.title("Student Data")
        subwindow.minsize(600,300)
        subwindow.geometry("600x300")
        rowtitle = ["name","prn","phone"]
        for k in range(3):
            e = Entry(subwindow,width=20)
            e.grid(row=0,column=k)
            e.insert(END,rowtitle[k])
        for i in range(3):
            for j in range(len(list_of_list[0])):
                e = Entry(subwindow,width=20)
                e.grid(row=j+1,column=i)
                e.insert(END,list_of_list[i][j])
    else:
        messagebox.showinfo("Read","No Student Data found")

def delete():
    prn = eprn.get()
    data = student.find_one({'prn':prn})
    if(prn=="" ):
        messagebox.showinfo("Delete","PRN field is compulsory ")
    else:
        if(data):
            data = student.delete_one({'prn':prn})
            messagebox.showinfo("Create","Student Deleted successfully")
            eprn.delete(0,END)
        else:
            messagebox.showinfo("Read","No Student Data found")

#GUI part

root = Tk()
root.minsize(600,300)
root.geometry('600x300')
root.title("CRUD Application")

#labels
name = Label(root,text="Enter Name : ",font=('bold',10))
name.place(x=20,y=40)
prn = Label(root,text="Enter PRN(eg.92): ",font=('bold',10))
prn.place(x=20,y=70)
phone = Label(root,text="Enter Phone : ",font=('bold',10))
phone.place(x=20,y=100)

#Entries
ename = Entry(root,width=60)
ename.place(x=150,y=40)
eprn = Entry(root,width=60)
eprn.place(x=150,y=70)
ephone = Entry(root,width=60)
ephone.place(x=150,y=100)

#buttons
create = Button(root,text="Create",font=('italic',12),bg='green',command=create)
create.place(x=40,y=150)
reset = Button(root,text="Reset",font=('italic',12),bg='yellow',command=reset)
reset.place(x=140,y=150)
update = Button(root,text="Update",font=('italic',12),bg='yellow',command=update)
update.place(x=240,y=150)
read = Button(root,text="Read",font=('italic',12),bg='white',command=read)
read.place(x=340,y=150)
delete = Button(root,text="Delete",font=('italic',12),bg='red',command=delete)
delete.place(x=440,y=150)

root.mainloop()