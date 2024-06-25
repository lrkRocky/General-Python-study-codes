from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import os					#Import modules about to be used.
import yagmail

PirPin = 17
LedPin = 2
LedPinOff = 3
LedPin2 = 4					#General variable declarations and value assignments.
movement_detected = 0
last_time_photo_taken = 0
Web_log_file_name = "/home/Rpi/camera/photo_web_log.txt"

email_app_password = ""
email_sender = 'Your_RaspberryPiEmail@gmail.com'
email_recipient = 'Your_Email_recipient@gmail.com'
password_location = "Your/Password/Location/Path"	#Variable declarations and value assignments for email configuration.

def update_photo_name_file(file_name):
    with open(Web_log_file_name, "a") as f:							#Opens photo file name document with permission to read and write
        f.write(file_name)											# and adds a new line with the last photo file name on it.
        f.write("\n")
def led2_blink():
    for i in range(2):
        GPIO.output(LedPin2, GPIO.LOW)
        time.sleep(0.2)
        GPIO.output(LedPin2, GPIO.HIGH)								#Makes a second output led blink to indicate photo is about to be taken.
        time.sleep(0.2)
        
def send_photo_by_email(file_name, email_recipient):
    yag.send(to = email_recipient,									#Sends email with indicated information.
     subject= "Movement detected.",
     contents="Hi Rocky, a movement was detected by your Raspberry Pi for 3 seconds consecutive, the image of it is attached to this email.",
     attachments= file_name)
    print("Photo succesfully sent to: " + str(email_recipient))		#Indicates that email was sent and to which recipient email.
    

print("Welcome.")										#Code start.
if os.path.exists(Web_log_file_name):					#In case a file with photos file names exists before, this remove it to create 
    os.remove(Web_log_file_name)						#	a new one wihtout any initial photo on it.

with open (password_location, "r") as f:
    email_app_password = f.read()
yag = yagmail.SMTP(email_sender, email_app_password)	#Configuration to prepair email to send photo using de app password located in a secret path.
print("Email configuration done.")

GPIO.setmode(GPIO.BCM)
GPIO.setup(PirPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(LedPin, GPIO.OUT)
GPIO.setup(LedPin2, GPIO.OUT)							#GPIO configuration for every output pin about to be used.
GPIO.setup(LedPinOff, GPIO.OUT)
GPIO.output(LedPinOff, GPIO.LOW)
print("GPIO ready. Configuring camera...")

camera = PiCamera()
camera.resolution = (720, 480)							#Camera parameters configuration.
camera.rotation = 180
time.sleep(2)
print("Camera configured.")

try:
    if os.path.exists("/home/Rpi/camera"):
        print("Directory used to save photos exists, continuing with process. Ready to take photo in case movement is detected during 3 seconds.")
        while True:
            time.sleep(0.01)						#Reduce CPU work.
            for i in range (12):					#Iteration cycle that allows 3 seconds of consecutive movement be detected.
                time.sleep(0.25)					#12*0.25sec = 3sec
                if GPIO.input(PirPin) == 1:
                    movement_detected += 1			#Counter of iterations in sequence in which movement was detected.
            #        print("Movements in sequence detected: " + str(movement_detected))  #(Line that can be use to test if movement is being detected).
                    GPIO.output(LedPin, GPIO.HIGH)	#Output led pin that indicates movement is being detected.
                else:
                    movement_detected = 0
                    GPIO.output(LedPin, GPIO.LOW)	#Turns off output led pin in case movement is not longer detected.
                    break							#Gets out of cicle to repeat counter from beggining in case movement is not detected.
            if movement_detected == 12:												#In case movement has been detected for 3 consecutive sec, starts process of taking photo and send by email.
                movement_detected = 0
                print ("Movement dectected for 3 seconds. Taking photo...")
                if time.time() - last_time_photo_taken  > 60:						#Limits to repeat process max every 60sec. 
                    led2_blink()													#Makes a second output led blink to indicate photo is about to be taken.
                    GPIO.output(LedPin2, GPIO.LOW)
                    file_name = ("/home/Rpi/camera/Photo_"+str(time.time())+".jpg")	#Creates a file name related with current time for photo.
                    camera.capture(file_name)										#Takes photo and saves it with preset file name.
                    last_time_photo_taken = time.time()								#Saves current time in which photo was taken on a variable for it.						
                    print("Photo taken and saved as " + str(file_name))
                    if os.path.exists(file_name):										#Confirms that photo taken file exists.
                        print("Confirmed that photo was taken and saved succesfully.")
                        send_photo_by_email(file_name, email_recipient)					#Sends email with indicated information.
                        update_photo_name_file(file_name)
                    else:
                        print("Error: Photo was not saved correctly.")					#Else cases indicate that something went wrong.
                else:
                    print("Photo cannot be taken since it is needed to wait at least 60 seconds int between photos taken.")
            else:
                pass
            movement_detected = 0														#Makes sure movement counter is reset in case movement is not detected.
    else:
        print("Directory used to save photo (/home/Rpi/camera) not founded, process stoped.")	#Indicates that something went wrong with file path to save the photo.

except KeyboardInterrupt:			#Allows programmer/user to stop the program to finish it and continue cleaning the GPIO of the board.
    print ("End of the program.")
GPIO.cleanup()						#Cleans GPIO at the end of the program.
print ("GPIO cleaned.")
 


