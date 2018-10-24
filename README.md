# PyZombies
### Attendance Management System 

Following are the libraries and softwares that need to be downloaded in order to run the software.
  1. MySQLdb
  2. validate_email
  3. datetime 
  4. cv2
  5. pyzbar 
  6. qrcode
  7. smtplib
  8. Xamp Local Server with sql

Below are the steps to be followed for executing the file:
  1. Open the attendance.py file, compile and run it.
  2. Log-in window will open. Enter your login details and click on login if already registered else use the register now option for new user registration.
  3. After logging in, 4 options are provided to the user:
     - Click on add event to add new event.
     - Click on view events to view the existing events created by the user.
     - Click on upcoming events to view the list of events that are going to be held in future or are going on in the present.
     - Click on Scan QR code option to scan QR codes of participants and take attendance of a particular event.
  4. For creating new event, fill in all the details of the event and click on submit. Automatically, the event will be added in the database under the user which is creating it.
  5. In view events, an option for viewing participants of a particular event and adding new participants to the event is also provided.
  6. To add new participants, click on view events -> view participants -> add participants. Fill in all the details  of the participant and click on submit or import csv file by writing the events name and clicking on import.
  7. To take attendance, click on scan QR code -> Click here to scan QR code and wait while the webcam open. Scan the QR code and then click on -> Click here to view present participants.
  8. Finally a logout and back button is provided on each frame from where we can directly logout to the login frame or can come back to the previous frame respectively.
