#!/usr/bin/python

import MySQLdb

db = MySQLdb.connect("localhost","root","","pyzombies")

# prepare a cursor object using cursor() method
query = db.cursor()

# login

loop = 'true'
while(loop == 'true'):
    username = input("Enter username : ")
    password = input("Enter password : ")
    sql_login = "SELECT * FROM users WHERE Username = '" + username + "' AND Password = '" + password + "'"
    if(query.execute(sql_login)):
        db.commit()
        print ("logged in")
        results = query.fetchall()
        event_name = input("Enter event name : ")
        event_date = input("Enter date in format YYYY-MM-DD : ")
        event_venue = input("Enter venue : ")
        for row in results:
            user_id = row[0]
        print(user_id)
        sql_add_event = "INSERT INTO events (Event_name, Event_date, Event_venue, User_id) VALUES('" + event_name + "','" + event_date + "','" + event_venue + "','" + str(user_id) + "')"
        if(query.execute(sql_add_event)):
            db.commit()
            print ("Event added")
        else:
            db.commit()
            print ("Event not added")
            
    else:
        db.commit()
        print ("failure")
        




# disconnect from server
db.close()
