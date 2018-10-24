import MySQLdb
import tkinter as tk
from tkinter.ttk import *
import tkinter.messagebox as tm
from validate_email import validate_email
from datetime import datetime, date, time
import cv2
from pyzbar import pyzbar
import qrcode
import argparse
import imutils
import time
import re
import os
import sys
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from PIL import ImageTk,Image


LARGE_FONT=("Verdana",15)
H_FONT=("Verdana",30,"bold")
K_FONT=("Fixedsys",42,"bold")
F_FONT=("Verdana",12)

global db


db = MySQLdb.connect("localhost","root","","pyzombies")
db.autocommit(True)
query = db.cursor()

class Hello(tk.Tk):

    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)

        global query       
        
        container=tk.Frame(self)
        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)
        self.frames={}
        for F in (First,Second,Third,Fourth,Fifth,Sixth,Seventh,Eighth,Ninth,Tenth):
            frame=F(container,self)
            self.frames[F]=frame
            frame.grid(row=0,column=0,sticky="nsew")

        self.show_frame(First)
        
    def show_frame(self,cont):
        frame=self.frames[cont]
        frame.tkraise()

    def get_page(self, page_class):
        return self.frames[page_class]

    def logout(self,query):
        self.query = query
        self.show_frame(First)
        del self.query
        db.close()
        os.execl(sys.executable, sys.executable, *sys.argv)

    
            
    
class First(tk.Frame):
    def __init__(self,box,controller):
        tk.Frame.__init__(self,box)

        self.controller = controller

        #image = Image.open('image.png')
        #photo_image = ImageTk.PhotoImage(image)
        #label = tk.Label(self, image = photo_image)
        #label.image = photo_image
        #label.grid(row=0, column=0)

        
        
        self.lbl0=tk.Label(self,text="ATTENDANCE MANAGEMENT SYSTEM",font="bold",fg="orange",bg="green")
        self.lbl1=tk.Label(self,text="LOGIN  HERE",font="bold",fg="red",width="12",bg="darkblue")
        self.lbl2=tk.Label(self,text="Email ID",fg="white",width="15",bg="darkblue")
        self.lbl3=tk.Label(self,text="Password",fg="white",width="15",bg="darkblue")


        self.lbl0.config(font=K_FONT)
        self.lbl1.config(font=H_FONT)
        self.lbl2.config(font=LARGE_FONT)
        self.lbl3.config(font=LARGE_FONT) 

        self.entry_1=tk.Entry(self,width="35")
        self.entry_2=tk.Entry(self,show="*",width="35")
      
        self.entry_1.config(bg='lightgrey',fg='black')
        self.entry_2.config(bg='lightgrey',fg='black')

        self.lbl0.place(x=90,y=0)
        self.lbl1.place(x=400,y=200)
        self.lbl2.place(x=350,y=320)
        self.lbl3.place(x=350,y=390)

        self.entry_1.place(x=510,y=330)
        self.entry_2.place(x=510,y=400)
        
        self.button1=tk.Button(self,text="LOGIN",bg="light blue", fg="red",relief="raised",width="10",height="1",command=self.login)
        self.button1.config(font=F_FONT)
        self.button2=tk.Button(self,text="REGISTER NOW",bg="light blue", fg="red",relief="raised",width="13",height="1",command=lambda:controller.show_frame(Second))
        self.button2.config(font=F_FONT)
        self.button1.place(x=420,y=470)
        self.button2.place(x=560,y=470)

        self.configure(bg="darkblue")
    


    def login(self):

        

        global user_id
        

        # login
       
        email_id_login=self.entry_1.get()
        password_login=self.entry_2.get()
            
        sql_login = "SELECT * FROM users WHERE Email = '" + email_id_login + "'"
        if(query.execute(sql_login)):
            db.commit
            pass
                                         
        else:
            db.commit
            tm.showerror("Login Error","Not registered")
            return
      

        sql_check_pass = "SELECT * FROM users WHERE Email = '" + email_id_login + "' AND Password = '" + password_login + "'"
        if(query.execute(sql_check_pass)):
            db.commit
            results = query.fetchall()
            for row in results:
                user_id = row[0]
           
            self.controller.show_frame(Third)
            self.entry_1.delete(0, 'end')
            return
                
                                   
        else:
            db.commit
            tm.showerror("Login Error","Email-id and password do not match")
            return

    
        
       


class Second(tk.Frame):
   
    
    def __init__(self,box,controller):
        tk.Frame.__init__(self,box)

        global query

        self.controller = controller

        self.lbl0=tk.Label(self,text="REGISTRATION FORM",font="bold",fg="red",width="20",bg="darkblue")
        self.lbl1=tk.Label(self,text="Username",fg="white",width="20",bg="darkblue")
        self.lbl2=tk.Label(self,text="Email-ID",fg="white",width="20",bg="darkblue")
        self.lbl3=tk.Label(self,text="Mobile Number",fg="white",width="20",bg="darkblue")
        self.lbl4=tk.Label(self,text="Password",fg="white",width="20",bg="darkblue")
        self.lbl5=tk.Label(self,text="Confirm Password",fg="white",width="20",bg="darkblue")
        self.lbl6=tk.Label(self,text="Already Registered?",fg="red",width="20",bg="darkblue")

        self.lbl0.config(font=H_FONT)
        self.lbl1.config(font=LARGE_FONT)
        self.lbl2.config(font=LARGE_FONT)
        self.lbl3.config(font=LARGE_FONT)
        self.lbl4.config(font=LARGE_FONT)
        self.lbl5.config(font=LARGE_FONT)
        self.lbl6.config(font=LARGE_FONT)

        self.entry_1=tk.Entry(self,width="35",)
        self.entry_2=tk.Entry(self,width="35")
        self.entry_3=tk.Entry(self,width="35")
        self.entry_4=tk.Entry(self,show="*",width="35")
        self.entry_5=tk.Entry(self,show="*",width="35")
        

        self.entry_1.config(bg='lightgrey',fg='black')
        self.entry_2.config(bg='lightgrey',fg='black')
        self.entry_3.config(bg='lightgrey',fg='black')
        self.entry_4.config(bg='lightgrey',fg='black')
        self.entry_5.config(bg='lightgrey',fg='black')
        

        self.lbl0.place(x=0,y=45)
        self.lbl1.place(x=0,y=120)
        self.lbl2.place(x=0,y=170)
        self.lbl3.place(x=0,y=220)
        self.lbl4.place(x=0,y=270)
        self.lbl5.place(x=0,y=320)
        self.lbl6.place(x=70,y=450)
        
        self.entry_1.place(x=250,y=130)
        self.entry_2.place(x=250,y=180)
        self.entry_3.place(x=250,y=230)
        self.entry_4.place(x=250,y=280)
        self.entry_5.place(x=250,y=330)

        self.button1=tk.Button(self,bg="light blue",fg="red",relief="raised",text="Sign Up",width="12",height="1",command=self.reg_user)
        self.button1.config(font=LARGE_FONT)
        self.button1.place(x=130,y=390)

        self.button2=tk.Button(self,bg="light blue",fg="red",relief="raised",text="Sign In",width="6",height="1",command=lambda:controller.show_frame(First))
        self.button2.config(font=LARGE_FONT)
        self.button2.place(x=320,y=450)

        self.button3=tk.Button(self,bg="lightgrey",fg="black",relief="raised",text="Back",width="5",height="1",command=lambda:controller.show_frame(First))
        self.button3.config(font=LARGE_FONT)
        self.button3.place(x=1030,y=0)

        
        


        self.configure(bg="darkblue")



    def reg_user(self):
        
        username_reg = self.entry_1.get()
        email_id_reg = self.entry_2.get()
        mobile_num_reg = self.entry_3.get()
        password_reg = self.entry_4.get()
        conf_pass_reg = self.entry_5.get()

        # checks empty input
        if(len(username_reg) == 0 or len(email_id_reg) == 0 or len(mobile_num_reg) == 0 or len(password_reg) == 0 or len(conf_pass_reg) == 0):
            tm.showerror("Detais error","Fill all the details")
            self.controller.show_frame(Second)
            return
        
        # checks a valid email
        is_valid = validate_email(email_id_reg)
       

        if(is_valid):
            pass
        else:
            tm.showerror("Email-id error","Please provide a valid email address")
            return
        
        # checks a valid mobile number
        if(len(mobile_num_reg) != 10):
            tm.showerror("Mobile number error","Please enter a valid mobile number")
            return

        #compares password and conf-pass
        if(password_reg != conf_pass_reg):
            tm.showerror("Password error","Password and Confirm Password do not match")
            return

        
            
            

      

        sql_check_email = "SELECT Email FROM users"
        if(query.execute(sql_check_email)):
            results = query.fetchall()
                       

            for row in results:
                i=0
                if(email_id_reg == row[i]):
                    db.commit
                    tm.showerror("Register Error","Already registered")
                    break
                
                i=i+1

        else:
            print("query error")

        
        

        sql_register = "INSERT INTO users(Email, Username, Mobile_num, Password)VALUES(%s, %s, %s, %s)"
        args = (email_id_reg, username_reg, mobile_num_reg, password_reg)

        if(query.execute(sql_register, args)):
            db.commit
            tm.showinfo("Success","Registered Successfully")
            self.controller.show_frame(First)
            return

            

class Third(tk.Frame):
    def __init__(self,box,controller):
        tk.Frame.__init__(self,box)

        global query
        
        self.controller=controller

        self.button1=tk.Button(self,bg="violet",fg="black",relief="raised",text="Add Event",width="40",height="11",command=lambda:controller.show_frame(Fourth))
        self.button1.config(font=LARGE_FONT)
        self.button1.place(x=15,y=50)

        self.button2=tk.Button(self,bg="dodgerblue",fg="black",relief="raised",text="View Events",width="40",height="11",command=self.button2_do)
        self.button2.config(font=LARGE_FONT)
        self.button2.place(x=560,y=50)

        self.button3=tk.Button(self,bg="dodgerblue",fg="black",relief="raised",text="Upcoming  Events",width="40",height="11",command=self.button5_do)
        self.button3.config(font=LARGE_FONT)
        self.button3.place(x=15,y=360)

        self.button4=tk.Button(self,bg="violet",fg="black",relief="raised",text="Scan QR Code",width="40",height="11",command = lambda:controller.show_frame(Seventh))
        self.button4.config(font=LARGE_FONT)
        self.button4.place(x=560,y=360)
        
        self.button5=tk.Button(self,bg="lightgrey",fg="black",relief="raised",text="Logout",width="5",height="1",command=lambda:controller.logout(query))
        self.button5.config(font=LARGE_FONT)
        self.button5.place(x=950,y=0)
        
        self.button6=tk.Button(self,bg="lightgrey",fg="black",relief="raised",text="Back",width="5",height="1",command=lambda:controller.show_frame(Second))
        self.button6.config(font=LARGE_FONT)
        self.button6.place(x=1030,y=0)
        self.configure(bg="black")
        
    def button2_do(self):

        page = self.controller.get_page(Fifth)
        page.get_events()

    def button5_do(self):

        page = self.controller.get_page(Tenth)
        page.get_upcoming_events()
        
        
        

class Fourth(tk.Frame):
    
    def __init__(self,box,controller):
        
        tk.Frame.__init__(self,box)
        
        global query
        
        self.controller=controller

        self.lbl0=tk.Label(self,text="ADD YOUR EVENT HERE",fg="red",width="30",bg="darkblue")
        self.lbl1=tk.Label(self,text="Event Name",fg="white",width="30",bg="darkblue")
        self.lbl2=tk.Label(self,text="Event Date",fg="white",width="30",bg="darkblue")
        self.lbl3=tk.Label(self,text="Event Time",fg="white",width="30",bg="darkblue")
        self.lbl4=tk.Label(self,text="Event Venue",fg="white",width="30",bg="darkblue")
        
        self.lbl0.config(font=K_FONT)
        self.lbl1.config(font=LARGE_FONT)
        self.lbl2.config(font=LARGE_FONT)
        self.lbl3.config(font=LARGE_FONT)
        self.lbl4.config(font=LARGE_FONT)

        self.entry_0=tk.Entry(self,width="45")
        self.entry_1=tk.Entry(self,width="45")
        self.entry_2=tk.Entry(self,width="45")
        self.entry_3=tk.Entry(self,width="45")

        self.entry_1.insert(0,"YYYY-MM-DD")
        self.entry_2.insert(0,"00:00")
        

        self.entry_0.config(bg='lightgrey',fg='black')
        self.entry_1.config(bg='lightgrey',fg='black')
        self.entry_2.config(bg='lightgrey',fg='black')
        self.entry_3.config(bg='lightgrey',fg='black')
       

        self.lbl0.place(x=50,y=50)
        self.lbl1.place(x=165,y=200)
        self.lbl2.place(x=160,y=270)
        self.lbl3.place(x=160,y=340)
        self.lbl4.place(x=164,y=410)

        
        self.entry_0.place(x=460,y=210)
        self.entry_1.place(x=460,y=280)
        self.entry_2.place(x=460,y=350)
        self.entry_3.place(x=460,y=420)
        
        self.button1=tk.Button(self,bg="dodgerblue",fg="black",relief="raised",text="Submit",width="15",height="1",command=self.add)
        self.button1.config(font=LARGE_FONT)
        self.button1.place(x=450,y=480)
        
        self.button2=tk.Button(self,bg="lightgrey",fg="black",relief="raised",text="Logout",width="5",height="1",command=lambda:controller.logout(query))
        self.button2.config(font=LARGE_FONT)
        self.button2.place(x=950,y=0)
        
        self.button3=tk.Button(self,bg="lightgrey",fg="black",relief="raised",text="Back",width="5",height="1",command=lambda:controller.show_frame(Third))
        self.button3.config(font=LARGE_FONT)
        self.button3.place(x=1030,y=0)
        
        
          
        self.configure(bg="darkblue")

    def add(self):

        event_name = self.entry_0.get()
        event_date = self.entry_1.get()
        event_time = self.entry_2.get()
        event_venue = self.entry_3.get()

        if(len(event_name) == 0 or len(event_date) == 0 or len(event_time) == 0 or len(event_venue) == 0):
            tm.showerror("Details error","Fill all the details")
            self.controller.show_frame(Fourth)
            return
        
        x=re.search(r"(20[0-9][0-9])(-)(0[1-9]|1[0-2])(-)(0[1-9]|1[0-9]|2[0-9]|3[0-1])$",event_date)
        
        if(x != None):
            if(x.group(0) == event_date):
                pass                    
        else:
           tm.showerror("Error","Check Date Format  (YYYY-MM-DD)")
           return
            
        time_re = re.search(r"(0[0-9]|1[0-9]|2[0-4])(:)([0-5])([0-9])",event_time)
        
        if(time_re != None):
            if(time_re.group(0)==event_time):
                pass
        else:
            tm.showerror("Error","Check Time Format  (00:00)")
            return


        
        sql_event = "INSERT INTO events(Event_name, Event_date, Event_time, Event_venue, User_id)VALUES(%s, %s, %s, %s, %s)"
        args = (event_name, event_date, event_time, event_venue, str(user_id)) 
       

        if(query.execute(sql_event,args)):
            tm.showinfo("Success","Event added Successfully")
            page = self.controller.get_page(Fifth)
            page.get_events()
            
            self.controller.show_frame(Fifth)
            return

        else:
            tm.showerror("Warning","Query error")
            

class Fifth(tk.Frame):
    def __init__(self,box,controller):
        tk.Frame.__init__(self,box)
        
        self.controller = controller

        self.id_list = []
        self.name_list = []
        self.date_list = []
        self.time_list = []
        self.venue_list = []

        self.label1 = tk.Label(self,text="Events",fg="white", bg="darkblue",width = "20")
        self.label1.config(font=H_FONT)
        self.label1.grid(column = 0,columnspan=5,pady = 10)

        self.button2=tk.Button(self,bg="lightgrey",fg="black",relief="raised",text="Logout",width="5",height="1",command=lambda: self.controller.logout(query))
        self.button2.config(font=LARGE_FONT)
        self.button2.place(x=950,y=0)
        
        self.button3=tk.Button(self,bg="lightgrey",fg="black",relief="raised",text="Back",width="5",height="1",command=lambda: self.controller.show_frame(Third))
        self.button3.config(font=LARGE_FONT)
        self.button3.place(x=1030,y=0)

    def get_events(self):

       

        self.c1 = tk.Label(self,text="Event Name",fg="white", bg="blue", width="16")
        self.c1.grid(row = 1, column = 0 ,pady = 5)
        self.c1.config(font=LARGE_FONT)
        self.c2 = tk.Label(self,text="Event Venue",fg="white", bg="blue", width="16")
        self.c2.grid(row = 1, column = 1 ,pady = 5)
        self.c2.config(font=LARGE_FONT)
        self.c3 = tk.Label(self,text="Event Date",fg="white", bg="blue", width="16")
        self.c3.grid(row = 1, column = 2 ,pady = 5)
        self.c3.config(font=LARGE_FONT)
        self.c4 = tk.Label(self,text="Event Time",fg="white", bg="blue", width="16")
        self.c4.grid(row = 1, column = 3 ,pady = 5)
        self.c4.config(font=LARGE_FONT)
        self.c5 = tk.Label(self,text="Participants",fg="white", bg="blue", width="16")
        self.c5.grid(row = 1, column = 4 ,pady = 5)
        self.c5.config(font=LARGE_FONT)

      
        

        global event_id
        

        user_for_events = str(user_id)

        sql_select_events = "SELECT * FROM events WHERE User_id = '" + user_for_events + "'"
        
        if(query.execute(sql_select_events)):
            db.commit
            results = query.fetchall()

            for row in results:

                self.id_list.append(row[0])
                self.name_list.append(row[1])
                self.date_list.append('{:%Y/%m/%d}'.format(row[2]))
                self.time_list.append(row[3])
                self.venue_list.append(row[4])
        else:
            tm.showerror("No events","There are no events created")
            return

            
        
        for i in range(0,len(results)): #Rows

           
             
            self.b = tk.Label(self,text = self.name_list[i], width="31")
            self.b.grid(row = i+2, column = 0, pady = 5)
            self.b = tk.Label(self,text = self.venue_list[i], width="31")
            self.b.grid(row = i+2, column = 1, pady = 5)
            self.b = tk.Label(self,text = self.date_list[i], width="31")
            self.b.grid(row = i+2, column = 2, pady = 5)
            self.b = tk.Label(self,text = self.time_list[i], width="31")
            self.b.grid(row = i+2, column = 3, pady = 5)

      
                

        for i in range(0,len(results)):
            
                button_view = tk.Button(self,bg="darkblue",fg="white",relief="raised",text="View Participants",width="30",height="1",command=lambda i=i,evt_id=self.id_list[i]:self.button3_do(evt_id)) 
                button_view.grid(row = i+2, column = 4)

        self.controller.show_frame(Fifth)

    def button3_do(self,evt_id):
                                        
        event_id = evt_id
        page = self.controller.get_page(Ninth)
        page.get_participants(event_id)
        


class Sixth(tk.Frame):
    def __init__(self,box,controller):
        tk.Frame.__init__(self,box)
        self.controller=controller

        self.lbl0=tk.Label(self,text="ADD PARTICIPANT DETAILS",fg="red",width="30",bg="darkblue")
        self.lbl1=tk.Label(self,text="Participant Name",fg="white",width="30",bg="darkblue")
        self.lbl2=tk.Label(self,text="Participant Email ID",fg="white",width="30",bg="darkblue")
        self.lbl3=tk.Label(self,text="Participant Mobile Number",fg="white",width="30",bg="darkblue")
        self.lbl4=tk.Label(self,text="Select Event",fg="white",width="30",bg="darkblue")        
        
       
        self.lbl0.config(font=K_FONT)
        self.lbl1.config(font=LARGE_FONT)
        self.lbl2.config(font=LARGE_FONT)
        self.lbl3.config(font=LARGE_FONT)
        self.lbl4.config(font=LARGE_FONT)
        
        self.entry_0=tk.Entry(self,width="45")
        self.entry_1=tk.Entry(self,width="45")
        self.entry_2=tk.Entry(self,width="45")
     
        self.entry_0.config(bg='lightgrey',fg='black')
        self.entry_1.config(bg='lightgrey',fg='black')
        self.entry_2.config(bg='lightgrey',fg='black')
     
   
        self.lbl0.place(x=50,y=50)
        self.lbl1.place(x=159,y=200)
        self.lbl2.place(x=170,y=270)
        self.lbl3.place(x=200,y=340)
        self.lbl4.place(x=230,y=410)
        
        
        self.entry_0.place(x=540,y=210)
        self.entry_1.place(x=540,y=280)
        self.entry_2.place(x=540,y=350)
        
     

        self.button1=tk.Button(self,bg="dodgerblue",fg="black",relief="raised",text="Submit",width="6",height="1",command=self.mess)
        self.button1.config(font=LARGE_FONT)
        self.button1.place(x=450,y=500)
        
        self.button2=tk.Button(self,bg="dodgerblue",fg="black",relief="raised",text="Add",width="6",height="1",command=self.add)
        self.button2.config(font=LARGE_FONT)
        self.button2.place(x=570,y=500)

        self.lbl5=tk.Label(self,fg="white",width="70",bg="darkblue",text="For importing csv file, enter file name. Please keep file name as your event name:")
        self.lbl5.config(font=LARGE_FONT)
        self.lbl5.place(x=100,y=580)

        self.entry_3=tk.Entry(self,width="30")
        self.entry_3.place(x=400,y=640)

        self.button3=tk.Button(self,bg="dodgerblue",fg="black",relief="raised",text="Import",width="6",height="1",command=self.import_participant)
        self.button3.config(font=LARGE_FONT)
        self.button3.place(x=600,y=625)
    
    
        self.button4=tk.Button(self,bg="lightgrey",fg="black",relief="raised",text="Logout",width="5",height="1",command=lambda:controller.logout(query))
        self.button4.config(font=LARGE_FONT)
        self.button4.place(x=950,y=0)
        
        self.button5=tk.Button(self,bg="lightgrey",fg="black",relief="raised",text="Back",width="5",height="1",command=lambda:controller.show_frame(Fifth))
        self.button5.config(font=LARGE_FONT)
        self.button5.place(x=1030,y=0)

        self.name_events = []
        self.id_events = []
        
        
        self.configure(bg="darkblue")

    def mess(self):
        tm.showinfo("Completed","Participants added successfully!")
        page4 = self.controller.get_page(Fifth)
        page4.get_events()

    def select_event(self): 

        
        
        user_for_events = str(user_id)

        sql_select_events = "SELECT Event_id,Event_name FROM events WHERE User_id = '" + user_for_events + "'"

        if(query.execute(sql_select_events)):
            db.commit
            results = query.fetchall()
            print(results)
            for row in results:
               
                self.name_events.append(row[1])


            self.variable=tk.StringVar()
            self.variable.set(self.name_events[0]) 

            self.select = tk.OptionMenu(self,self.variable,*self.name_events)

            self.select.place(x=540,y=410)
                
        self.controller.show_frame(Sixth)
        

    def add(self):

        self.participant_name = self.entry_0.get()
        self.participant_email = self.entry_1.get()
        self.participant_mobile_num = self.entry_2.get()
        self.participant_select_event = self.variable.get()

        if(len(self.participant_name) == 0 or len(self.participant_email) == 0 or len(self.participant_mobile_num) == 0 or len(self.participant_select_event) == 0):
            tm.showerror("Details error","Fill all the details")
            self.controller.show_frame(Fourth)
            return

        sql_select_id = "SELECT Event_id FROM events WHERE Event_name = '" + self.participant_select_event + "' AND User_id = '" + str(user_id) + "'"

        if(query.execute(sql_select_id)):
            db.commit
            result = query.fetchall()
            print(result)
            for row in result:
                self.participant_select_id = row[0]

       
        sql_participants = "INSERT INTO participants(Participant_name, Participant_email, Participant_mobno, Event_id, User_id)VALUES(%s, %s, %s, %s, %s)"
        args = (self.participant_name, self.participant_email, self.participant_mobile_num, str(self.participant_select_id), str(user_id)) 
       

        if(query.execute(sql_participants,args)):
            
            self.qr_code_generate()
            self.controller.show_frame(Sixth)
            return

        else:
            tm.showerror("Warning","Query error")

    def qr_code_generate(self):
        
        qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
        )
        qr.add_data(self.participant_email)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        img = qr.make_image()
        self.image = "qrcodes/" + self.participant_name + ".jpg"
        img.save(self.image)

        self.qr_code_email()

    def qr_code_email(self):
        
 
        fromaddr = "gangabagga@yahoo.in"
        toaddr = self.participant_email
 
        msg = MIMEMultipart()
 
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Registration confirmation for " + self.participant_select_event
 
        body = "Thank you so much for registering for " + self.participant_select_event + ". Please bring the following attatchment for the event"
 
        msg.attach(MIMEText(body, 'plain'))
 
        filename = self.image
        attachment = open(self.image, "rb")
 
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 
        msg.attach(part)
 
        
        server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
        server.starttls()
        
        server.login(fromaddr, "ppon lvao pthr gqkt")
        
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        print("mail send")
        server.quit()

        tm.showinfo("Success","Participant registered Successfully. Please ask him to check the confirmation mail")
        self.controller.show_frame(Sixth)


    def import_participant(self):

        self.participant_name = []
        self.participant_email = []
        self.participant_mobno = []
        participants_list = []
        result_list = []

        self.csv_name = self.entry_3.get()
        
        sql_events = "SELECT Event_id,Event_name FROM events WHERE User_id = '" + str(user_id) + "'"
        if(query.execute(sql_events)):
            results = query.fetchall()
            for match in results:
                if(self.csv_name == match[1]):
                    self.correct_csv_name = self.csv_name
                    self.csv_event_id = match[0]
                    break
                else:
                    tm.showerror("File not found error","File name doesnot match to any existing event. Please check the name or create a new event")
                    return

        try:
            
            participants = list(open("participants/" + self.correct_csv_name + ".csv", 'r').read().split('\n'))
            for i in participants:
                result_list.append(i.split(','))

            

            if(len(result_list)!=0):
                
                for each in result_list[:-1]:
                    
                    self.participant_name.append(each[0])
                    self.participant_email.append(each[1])
                    self.participant_mobno.append(each[2])

                for i in range(0,len(self.participant_name)):
                    
                    sql_participants = "INSERT INTO participants(Participant_name, Participant_email, Participant_mobno, Event_id, User_id)VALUES(%s, %s, %s, %s, %s)"
                    args = (self.participant_name[i], self.participant_email[i], self.participant_mobno[i], str(self.csv_event_id), str(user_id))

                    if(query.execute(sql_participants,args)):
                        pass
            

                    else:
                        tm.showerror("Warning","Adding of participants was unsuccessful")
                        return
                    
                tm.showinfo("Success","Participants added successfuly")


            else:
                tm.showerror("Record error","No participant found")
                return
            
        except FileNotFoundError:

            tm.showerror("File error","File not found")
            return
        
                


class Seventh(tk.Frame):
    def __init__(self,box,controller):
        tk.Frame.__init__(self,box)
        self.controller = controller

        self.button1=tk.Button(self,bg="dodgerblue",fg="black",relief="raised",text="Click here to scan qr code",width="45",height="1",command = self.scan_qr)
        self.button1.config(font=LARGE_FONT)
        self.button1.place(x=250,y=200)

        self.button1=tk.Label(self,fg="red",text="Please wait while webcam opens",width="45",height="1")
        self.button1.config(font=LARGE_FONT)
        self.button1.place(x=250,y=250)
        
        self.button2=tk.Button(self,bg="lightgrey",fg="black",relief="raised",text="Logout",width="5",height="1",command=lambda:controller.logout(query))
        self.button2.config(font=LARGE_FONT)
        self.button2.place(x=950,y=0)
        
        self.button3=tk.Button(self,bg="lightgrey",fg="black",relief="raised",text="Back",width="5",height="1",command=lambda:controller.show_frame(Sixth))
        self.button3.config(font=LARGE_FONT)
        self.button3.place(x=1030,y=0)
        

        

        

    def scan_qr(self):
        ap = argparse.ArgumentParser()
        ap.add_argument("-o", "--output", type=str, default="qrcodes.csv",
	help="path to output CSV file containing qrcodes")
        args = vars(ap.parse_args())

        #video capture
        video_capture = cv2.VideoCapture(0)
        time.sleep(1.0)

        cv2.namedWindow("QRcode Scanner")

        while True:
            ret, frame = video_capture.read()
    

            # find the barcodes in the frame and decode each of the barcodes
            qrcodes = pyzbar.decode(frame)
            # loop over the detected barcodes
            qrcodeData = " "
    
            for qrcode in qrcodes:
                # extract the bounding box location of the barcode and draw
                # the bounding box surrounding the barcode on the image
                (x, y, w, h) = qrcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
         
                # the barcode data is a bytes object so if we want to draw it
                # on our output image we need to convert it to a string first
        
                qrcodeData = qrcode.data.decode("utf-8")
                qrcodeType = qrcode.type
        
        
            cv2.imshow("QRcode Scanner", frame)
            data_participant = []

            #This breaks on 'q' key
    
            if (len(qrcodes)!=0):
                data_participant.append(qrcodeData)
                print(data_participant)
                break
            elif (cv2.waitKey(1) & 0xFF == ord('q')):
                break
            
        

        video_capture.release()
        cv2.destroyAllWindows()
       

        self.button1=tk.Button(self,bg="dodgerblue",fg="black",relief="raised",text="Click here to view present participants",width="45",height="1",command = lambda: self.button_do(qrcodeData))
        self.button1.config(font=LARGE_FONT)
        self.button1.place(x=250,y=300)
        
        self.controller.show_frame(Seventh)

    def button_do(self,data):
        
        data_participant = data
        page2 = self.controller.get_page(Eighth)
        page2.get_present_participants(data_participant)
        
    
        


class Eighth(tk.Frame):
    def __init__(self,box,controller):
        tk.Frame.__init__(self,box)
        
        self.controller = controller

        self.id_part = []
        self.name_part = []
        self.email_part = []
        self.mob_part = []
        self.event_name = []
        

    def get_present_participants(self,p_email):

        self.p_email = p_email
        

        self.label1 = tk.Label(self,text="Participants Present",fg="white", bg="darkblue",width = "35")
        self.label1.config(font=H_FONT)
        self.label1.grid(column = 0,columnspan=5,pady = 10)

        self.button2=tk.Button(self,bg="lightgrey",fg="black",relief="raised",text="Logout",width="5",height="1",command=lambda:self.controller.logout(query))
        self.button2.config(font=LARGE_FONT)
        self.button2.place(x=950,y=0)
        
        self.button3=tk.Button(self,bg="lightgrey",fg="black",relief="raised",text="Back",width="5",height="1",command=lambda:self.controller.show_frame(Seventh))
        self.button3.config(font=LARGE_FONT)
        self.button3.place(x=1030,y=0)

        self.c1 = tk.Label(self,text="Participant Name",fg="white", bg="blue", width="20")
        self.c1.grid(row = 1, column = 0 ,pady = 5)
        self.c1.config(font=LARGE_FONT)
        self.c2 = tk.Label(self,text="Participant Email",fg="white", bg="blue", width="20")
        self.c2.grid(row = 1, column = 1 ,pady = 5)
        self.c2.config(font=LARGE_FONT)
        self.c3 = tk.Label(self,text="Participant Number",fg="white", bg="blue", width="20")
        self.c3.grid(row = 1, column = 2 ,pady = 5)
        self.c3.config(font=LARGE_FONT)
        self.c4 = tk.Label(self,text="Attendance",fg="white", bg="blue", width="20")
        self.c4.grid(row = 1, column = 3 ,pady = 5)
        self.c4.config(font=LARGE_FONT)
       

        global event_id
        

        user_for_events = str(user_id)

        


        sql_select_events = "SELECT * FROM participants WHERE Participant_email = '" + self.p_email + "'"
        

        if(query.execute(sql_select_events)):

            result_total = query.fetchall()
            
            for row in result_total:

                sql_event_for_participant = "SELECT Event_name FROM events WHERE Event_id = '" + str(row[4]) + "'"
                if(query.execute(sql_event_for_participant)):
                    results = query.fetchall()
                    for match in results:
                        self.event_for_participant = match[0]
                csvRow = [row[0], row[1], row[2], row[3],self.event_for_participant]
                self.csvfile = "qrcodes_" + self.event_for_participant + ".csv"
                with open(self.csvfile, "a") as fp:
                    wr = csv.writer(fp, dialect='excel')
                    wr.writerow(csvRow)

                
       
        result_list = []      
        self.csvfile = "qrcodes_" + self.event_for_participant + ".csv"  
        l = list(open(self.csvfile, 'r').read().split('\n\n2'))
        
        for i in l:
            result_list.append(i.split(','))


        print(result_list)
        
            
        if(len(result_list)!=0):
            
            for each in result_list:
                
                self.id_part.append(each[0])
                self.name_part.append(each[1])
                self.email_part.append(each[2])
                self.mob_part.append(each[3])
                self.event_name.append(self.event_for_participant)
            
        
        for i in range(0,len(result_list)): #Rows

           
             
            self.b = tk.Label(self,text = self.name_part[i], width="35")
            self.b.grid(row = i+2, column = 0, pady = 5)
            self.b = tk.Label(self,text = self.email_part[i], width="35")
            self.b.grid(row = i+2, column = 1, pady = 5)
            self.b = tk.Label(self,text = self.mob_part[i], width="35")
            self.b.grid(row = i+2, column = 2, pady = 5)
            

      
                

        for i in range(0,len(result_list)):
            
                button_view = tk.Label(self,fg="green",relief="raised",text="PRESENT",width="32",height="1")
                button_view.grid(row = i+2, column = 3)

        self.controller.show_frame(Eighth)


class Ninth(tk.Frame):
    def __init__(self,box,controller):
        tk.Frame.__init__(self,box)
        self.controller = controller

   

        self.id_part = []
        self.name_part = []
        self.email_part = []
        self.num_part = []
        self.event_part = []

        self.label_b1 = []
        self.label_b2 = []
        self.label_b3 = []
        self.label_b4 = []

        

        self.label1 = tk.Label(self,text="Particpants List",fg="white", bg="darkblue",width = "15")
        self.label1.config(font=H_FONT)
        self.label1.grid(column = 0,columnspan=5,pady = 10)

        
        self.button2=tk.Button(self,bg="lightgrey",fg="black",relief="raised",text="Logout",width="5",height="1",command=lambda: self.controller.logout(query))
        self.button2.config(font=LARGE_FONT)
        self.button2.place(x=950,y=0)
        
        self.button3=tk.Button(self,bg="lightgrey",fg="black",relief="raised",text="Back",width="5",height="1",command=self.destroy_labels )
        self.button3.config(font=LARGE_FONT)
        self.button3.place(x=1030,y=0)

        self.button3=tk.Button(self,bg="lightgrey",fg="black",relief="raised",text="Add participants",width="20",height="1",command=self.add_participant)
        self.button3.config(font=LARGE_FONT)
        self.button3.place(x=30,y=0)

        self.c1 = tk.Label(self,text="Participant Name",fg="white", bg="blue", width="20")
        self.c1.grid(row = 1, column = 0 ,pady = 5, padx = 5)
        self.c1.config(font=LARGE_FONT)
        self.c2 = tk.Label(self,text="Participant Email",fg="white", bg="blue", width="20")
        self.c2.grid(row = 1, column = 1 ,pady = 5, padx = 5)
        self.c2.config(font=LARGE_FONT)
        self.c3 = tk.Label(self,text="Mobile Number",fg="white", bg="blue", width="20")
        self.c3.grid(row = 1, column = 2 ,pady = 5, padx = 5)
        self.c3.config(font=LARGE_FONT)
        self.c3 = tk.Label(self,text="Event Name",fg="white", bg="blue", width="20")
        self.c3.grid(row = 1, column = 3 ,pady = 5, padx = 5)
        self.c3.config(font=LARGE_FONT)


    def add_participant(self):
        page3 = self.controller.get_page(Sixth)
        page3.select_event()
        
 

    def get_participants(self,event_id):
       



        event_for_participant = event_id

        sql_event_for_participant = "SELECT Event_name FROM events WHERE Event_id = '" + str(event_for_participant) + "'"
        if(query.execute(sql_event_for_participant)):
            results = query.fetchall()
            for match in results:
                self.event_name_for_participant = match[0]
        

        sql_select_participants = "SELECT * FROM participants WHERE Event_id = '" + str(event_for_participant) + "' AND User_id = '" + str(user_id) + "'"
        
        if(query.execute(sql_select_participants)):
            db.commit
            self.result_list = query.fetchall()
            print(len(self.result_list))

                  
            
            for row in self.result_list:
                self.id_part.append(row[0])
                self.name_part.append(row[1])
                self.email_part.append(row[2])
                self.num_part.append(row[3])
                
          

            for i in range(0,len(self.result_list)): #Rows
                
                self.b1 = tk.Label(self, width="22")
                self.b2 = tk.Label(self, width="22")
                self.b3 = tk.Label(self, width="22")
                self.b4 = tk.Label(self, width="22")
                
                self.b1.grid(row = i+2, column = 0, pady = 5)
                self.b1.config(text=self.name_part[i])
                self.b2.grid(row = i+2, column = 1, pady = 5)
                self.b2.config(text=self.email_part[i])
                self.b3.grid(row = i+2, column = 2, pady = 5)
                self.b3.config(text=self.num_part[i])
                self.b4.grid(row = i+2, column = 3, pady = 5)
                self.b4.config(text=self.event_name_for_participant)

                self.label_b1.append(self.b1)
                self.label_b2.append(self.b2)
                self.label_b3.append(self.b3)
                self.label_b4.append(self.b4)
                
             
                
            
            self.controller.show_frame(Ninth)
            

        else:
            tm.showerror("Not Found","There are no participants registered for the event")
            self.controller.show_frame(Ninth)
            return


        
    def destroy_labels(self):
        print(len(self.label_b1))
        print(len(self.label_b2))
        print(len(self.label_b3))
        print(len(self.label_b4))
        
        self.id_part.clear()
        self.name_part.clear()
        self.email_part.clear()
        self.num_part.clear()
        self.event_part.clear()
        
        for l1 in self.label_b1:
            l1.destroy()
        for l2 in self.label_b2:
            l2.destroy()
        for l3 in self.label_b3:
            l3.destroy()
        for l4 in self.label_b4:
            l4.destroy()

        self.label_b1.clear()
        self.label_b2.clear()
        self.label_b3.clear()
        self.label_b4.clear()
        self.controller.show_frame(Fifth)



class Tenth(tk.Frame):
    
    def __init__(self,box,controller):
        tk.Frame.__init__(self,box)
        self.controller=controller


  

        self.button2=tk.Button(self,bg="lightgrey",fg="black",relief="raised",text="Logout",width="5",height="1",command=lambda:controller.show_frame(First))
        self.button2.config(font=LARGE_FONT)
        self.button2.place(x=950,y=0)
        
        self.button3=tk.Button(self,bg="lightgrey",fg="black",relief="raised",text="Back",width="5",height="1",command=lambda:controller.show_frame(Fifth))
        self.button3.config(font=LARGE_FONT)
        self.button3.place(x=1030,y=0)

        self.c1 = tk.Label(self,text="Event Name",fg="white", bg="blue", width="16")
        self.c1.grid(row = 1, column = 0 ,pady = 5)
        self.c1.config(font=LARGE_FONT)
        
        self.c2 = tk.Label(self,text="Event Venue",fg="white", bg="blue", width="16")
        self.c2.grid(row = 1, column = 1 ,pady = 5)
        self.c2.config(font=LARGE_FONT)
        
        self.c3 = tk.Label(self,text="Event Date",fg="white", bg="blue", width="16")
        self.c3.grid(row = 1, column = 2 ,pady = 5)
        self.c3.config(font=LARGE_FONT)
        
        self.c4 = tk.Label(self,text="Event Time",fg="white", bg="blue", width="16")
        self.c4.grid(row = 1, column = 3 ,pady = 5)
        self.c4.config(font=LARGE_FONT)


        self.id_list = []
        self.name_list = []
        self.date_list = []
        self.time_list = []
        self.venue_list = []
        self.event_ongoin = []
        self.check_name = " "

    def get_upcoming_events(self):


        

        global event_id

        user_for_events = str(user_id)
        now = datetime.now()
        now = now.strftime("%Y/%m/%d")
        print(now)

        sql_select_events = "SELECT * FROM events WHERE User_id = '" + user_for_events + "'"
        
        if(query.execute(sql_select_events)):
            db.commit
            results = query.fetchall()
            for row in results:
                if (('{:%Y/%m/%d}'.format(row[2])) > now):
                    
                    self.name_list.append(row[1])
                    self.id_list.append(row[0])
                    self.date_list.append('{:%Y/%m/%d}'.format(row[2]))
                    self.time_list.append(row[3])
                    self.venue_list.append(row[4])

                
                if (('{:%Y/%m/%d}'.format(row[2])) == now):
                    self.check_name = row[1]

                    
                
        print(self.check_name)
        self.label1 = tk.Label(self,text="Today's Event : " + self.check_name,fg="lightgreen",bg="darkblue",width = "20")
        self.label1.config(font=LARGE_FONT)
        self.label1.grid(row=0,column = 0,columnspan = 2,pady = 10)

        button_view2 = tk.Button(self,fg="green",text="View Attendance",width="20",height="1")
        button_view2.grid(row = 0, column = 2)

        button_view2 = tk.Button(self,fg="green",text="Take Attendance",width="20",height="1")
        button_view2.grid(row = 0, column = 3)

        
        for i in range(0,len(self.date_list)): #Rows

            
            self.b = tk.Label(self,text = self.name_list[i], width="25")
            self.b.grid(row = i+2, column = 0, pady = 5)
            self.b = tk.Label(self,text = self.venue_list[i], width="25")
            self.b.grid(row = i+2, column = 1, pady = 5)
            self.b = tk.Label(self,text = self.date_list[i], width="25")
            self.b.grid(row = i+2, column = 2, pady = 5)
            self.b = tk.Label(self,text = self.time_list[i], width="25")
            self.b.grid(row = i+2, column = 3, pady = 5)

      
                

        for i in range(0,len(self.date_list)):
            
                button_view1 = tk.Button(self,bg="darkblue",fg="white",text="View Participants",width="20",height="1",command=lambda i=i,evt_id=self.id_list[i]:self.button3_do(evt_id))
                button_view1.grid(row = i+2, column = 4)


        self.controller.show_frame(Tenth)
        return


    def button3_do(self,evt_id):
                                        
        event_id = evt_id
        page = self.controller.get_page(Ninth)
        page.get_participants(event_id)
        return

    def button6_do(self,event_name):
        
        page3 = self.controller.get_page(Eighth)
        page3.show_present_participants(event_name)
        

                    
     
        



root=Hello()
root.minsize(1100,800)
root.maxsize(1100,800)
root.mainloop()
