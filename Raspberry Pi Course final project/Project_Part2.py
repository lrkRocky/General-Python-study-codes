from flask import Flask
import os				#Import modules about to be used.

camera_folder_path = "/home/Rpi/camera"
app = Flask(__name__, static_url_path= camera_folder_path, static_folder= camera_folder_path)
Web_log_file_name = "/home/Rpi/camera/photo_web_log.txt"
email_recipient = 'Your_Email_recipient@gmail.com'		#Declare names, paths, email and some of the information about to be used.
photo_counter = 0

#Create routes

@app.route("/")
def index():
    return "Hi Rocky! Good afternoon (I hope it is afternoon now)." #Welcomes to user in the main web page.

@app.route("/check-movement")
def check_movement():							#Defines function for secondary route on the web server.
    lines = 0
    message = ""								#Prepares variable about to be used.
    last_photo_file_name = ""
    if os.path.exists(Web_log_file_name):		#Just in case there is a photo taken and saved by the project part 1, continue showing details about it.
        with open(Web_log_file_name, "r") as f:	#Opens text file with photos file names with permission to read only.
            for line in f:
                lines += 1						#Counts the lines in the photos file text (content).
                last_photo_file_name = line		#Keeps updating photos file name until the last one is the only one that stays on the variable.
        global photo_counter
        new_photos = lines - photo_counter		#Claculate difference to know how many photos were taken since page was for last time loaded.
        photo_counter = lines					#Updates the total of photos taken using the number of photos file lines.
        message = "Hi Rocky. \n There are "+str(new_photos)+" new photos taken since last checked (also sent to "+email_recipient+")."
        message += "<br/><br/> Last photo taken: "+last_photo_file_name		#Shows number of photos taken since last time checked, email recipient, 
        message += "<br/><br/> <img src=\""+last_photo_file_name+"\">"		#	photo file name and image of photo taken on the web page/server.
    else:
        message = "No previous photos founded."   							#in case no previous photos were saved or taken, a message indicates it.
    return message


app.run(host = "0.0.0.0", port=8250)										#Assign web page address with port indicated.