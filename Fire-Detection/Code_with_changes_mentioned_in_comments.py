# """Open terminal and install the following three modules by pressing these commands with pip:
#    pip install playsound
#    pip install opencv-python
#    pip install opencv-contrib-python """



import cv2 
import threading
import playsound
import requests
fire_cascade = cv2.CascadeClassifier(rf"C:\Users\mdabd\OneDrive\Desktop\Fire Detection\fire_detectionDataset.xml")
#Change this file path by right clicking on the file select copy as path and paste it from rf

vid = cv2.VideoCapture(0)
runOnce = False 

def play_alarm_sound_function():
    playsound.playsound(r"C:\Users\mdabd\OneDrive\Desktop\Fire Detection\audio.mp3",True)
#Change this file path by right clicking on the file select copy as path and paste it from r
    print("Fire alarm end")
def alert_message_function():
    querystring = {"apikey":"CZNT2KLOQJP8LZVA981","number":"","text":"EMERGENCY!!! FIRE Accident Took Place AT ABC Rubber Factory,Nampally X Roads,Hyderabad,Telangana.PLEASE SEND FIRE FIGHTERS AND FIRE ENGINES AT THE LOCATION. "}
    url = "https://panel.rapiwha.com/send_message.php"

    #Change the apikey change to the key shown in your rapiwha account
    # Please change the apikey as its linked to my account

    #beside number: 91 is India code and any 10digit mobile no.; beside text in double inverted commas u can change it as your msg according to ur requirement
    response = requests.request("GET", url, params=querystring)

    print(response.text)

    #the below 3 lines of code is used to send alert message to one more number
    
    #querystring1 = {"apikey":"CZNT2KLOQJP8LZVA98E1","number":"","text":"SEND FIRE ENGINES AT NGIT"}

   # response1 = requests.request("GET", url, params=querystring1)
    #print(response1.text)

   
   #to add another number uncomment above code and make changes as required


while(True):
    ret, frame = vid.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fire = fire_cascade.detectMultiScale(frame,1.2, 10)#(1.2,10)(2.0,10)

    for (x,y,w,h) in fire:
        cv2.rectangle(frame,(x-20,y-20),(x+w+20,y+h+20),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        print("Fire alarm initiated")
        threading.Thread(target=play_alarm_sound_function).start()
        
        if runOnce == False:
            print("Alert Initiated")
            threading.Thread(target=alert_message_function).start()
            runOnce=True
        if runOnce == True:
            print("Alert message already sent")
            runOnce =True
        

    cv2.imshow("Fire Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# import cv2 
# import threading
# import pygame
# import requests
# import time
# import mysql.connector
# from datetime import datetime

# # Initialize Pygame mixer
# pygame.mixer.init()

# # Configuration
# CASCADE_PATH = r"C:\Users\mdabd\OneDrive\Desktop\Fire Detection\fire_detection.xml"
# ALARM_SOUND_PATH = r"audio.mp3"
# OUTPUT_VIDEO_PATH = r"C:\Users\mdabd\OneDrive\Desktop\Fire Detection\Videos"  # Change this to your desired path
# DATABASE_HOST = 'localhost'
# DATABASE_USER = 'root'
# DATABASE_PASSWORD = 'kmit'
# DATABASE_NAME = 'fire_detection'
# API_URL = "https://panel.rapiwha.com/send_message.php"
# API_KEY = "CZNT2KLOQJP8LZVA98E1"
# PHONE_NUMBER = "912261445050"

# # Connect to the MySQL database
# conn = mysql.connector.connect(
#     host=DATABASE_HOST,
#     user=DATABASE_USER,
#     password=DATABASE_PASSWORD,
#     database=DATABASE_NAME
# )
# cursor = conn.cursor()

# # Create tables if they don't exist
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS fires (
#         fire_id INT PRIMARY KEY AUTO_INCREMENT,
#         timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#         location VARCHAR(255),
#         description TEXT,
#         image_path VARCHAR(255)
#     )
# ''')

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS videos (
#         video_id INT PRIMARY KEY AUTO_INCREMENT,
#         fire_id INT,
#         start_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#         end_timestamp TIMESTAMP,
#         video_path VARCHAR(255),
#         FOREIGN KEY (fire_id) REFERENCES fires(fire_id)
#     )
# ''')

# # Commit changes to the database
# conn.commit()

# fire_cascade = cv2.CascadeClassifier(CASCADE_PATH)
# vid = cv2.VideoCapture(0)
# out = None
# runOnce = False
# fire_id = None

# def play_alarm_sound_function():
#     pygame.mixer.music.load(ALARM_SOUND_PATH)
#     pygame.mixer.music.play()
#     while pygame.mixer.music.get_busy():
#         pygame.time.Clock().tick(10)
#     print("Fire alarm end")

# def alert_message_function():
#     querystring = {
#         "apikey": API_KEY,
#         "number": PHONE_NUMBER,
#         "text": "EMERGENCY!!! FIRE Accident Took Place AT ABC Rubber Factory,Nampally X Roads,Hyderabad,Telangana.PLEASE SEND FIRE FIGHTERS AND FIRE ENGINES AT THE LOCATION."
#     }
#     response = requests.request("GET", API_URL, params=querystring)
#     print(response.text)

# def initialize_video_writer(frame_width, frame_height, fire_id):
#     current_time = time.strftime("%Y%m%d%H%M%S")
#     filename = f'{OUTPUT_VIDEO_PATH}\\{fire_id}_{current_time}.avi'  # Updated path
#     fourcc = cv2.VideoWriter_fourcc(*'XVID')
#     return cv2.VideoWriter(filename, fourcc, 20.0, (int(frame_width), int(frame_height)))

# while True:
#     ret, frame = vid.read()
    
#     if not ret:
#         print("Error: Unable to capture video.")
#         break

#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     fire = fire_cascade.detectMultiScale(frame, 1.2, 10)

#     for (x, y, w, h) in fire:
#         cv2.rectangle(frame, (x-20, y-20), (x+w+20, y+h+20), (255, 0, 0), 2)
        
#         if out is None:
#             # Insert a new fire record into the database
#             cursor.execute('''
#                 INSERT INTO fires (location, description, image_path)
#                 VALUES (%s, %s, %s)
#             ''', ('YourLocation', 'FireDescription', 'path/to/image.jpg'))
            
#             # Get the fire_id of the newly inserted record
#             fire_id = cursor.lastrowid
            
#             # Specify the video file path
#             video_file_path = f'{OUTPUT_VIDEO_PATH}\\{fire_id}_{time.strftime("%Y%m%d%H%M%S")}.avi'  # Updated path
            
#             # Insert a new video record into the database
#             cursor.execute('''
#                 INSERT INTO videos (fire_id, start_timestamp, video_path)
#                 VALUES (%s, %s, %s)
#             ''', (fire_id, datetime.now(), video_file_path))
            
#             # Commit changes to the database
#             conn.commit()
            
#             # Initialize video writer with the correct filename and fire_id
#             out = initialize_video_writer(vid.get(3), vid.get(4), fire_id)
            
#             print("Alert Initiated")
#             threading.Thread(target=alert_message_function).start()
#             runOnce = True
#         else:
#             print("Alert message already sent")

#         threading.Thread(target=play_alarm_sound_function).start()
#         out.write(frame)

#     cv2.imshow("Fire Detector", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release resources
# vid.release()

# # Release video writer at the end of the loop
# if out is not None:
#     # Update end_timestamp when video recording ends
#     cursor.execute('''
#         UPDATE videos
#         SET end_timestamp = %s
#         WHERE fire_id = %s
#     ''', (datetime.now(), fire_id))
#     conn.commit()
    
#     out.release()

# # Close the database connection
# conn.close()
# cv2.destroyAllWindows()

# import cv2 
# import threading
# import pygame
# import requests
# import time

# # Initialize Pygame mixer
# pygame.mixer.init()

# # Configuration
# CASCADE_PATH = r"C:\Users\mdabd\OneDrive\Desktop\Fire Detection\fire_detection.xml"
# ALARM_SOUND_PATH = r"audio.mp3"
# OUTPUT_VIDEO_PATH = 'output'
# API_URL = "https://panel.rapiwha.com/send_message.php"
# API_KEY = "CZNT2KLOQJP8LZVA98E1"
# PHONE_NUMBER = "912261445050"

# fire_cascade = cv2.CascadeClassifier(CASCADE_PATH)
# vid = cv2.VideoCapture(0)
# out = None
# runOnce = False

# def play_alarm_sound_function():
#     pygame.mixer.music.load(ALARM_SOUND_PATH)
#     pygame.mixer.music.play()
#     while pygame.mixer.music.get_busy():
#         pygame.time.Clock().tick(10)
#     print("Fire alarm end")

# def alert_message_function():
#     querystring = {
#         "apikey": API_KEY,
#         "number": PHONE_NUMBER,
#         "text": "EMERGENCY!!! FIRE Accident Took Place AT ABC Rubber Factory,Nampally X Roads,Hyderabad,Telangana.PLEASE SEND FIRE FIGHTERS AND FIRE ENGINES AT THE LOCATION."
#     }
#     response = requests.request("GET", API_URL, params=querystring)
#     print(response.text)

# def initialize_video_writer(frame_width, frame_height):
#     current_time = time.strftime("%Y%m%d%H%M%S")
#     filename = f'{OUTPUT_VIDEO_PATH}_{current_time}.avi'
#     fourcc = cv2.VideoWriter_fourcc(*'XVID')
#     return cv2.VideoWriter(filename, fourcc, 20.0, (int(frame_width), int(frame_height)))

# while True:
#     ret, frame = vid.read()
    
#     if not ret:
#         print("Error: Unable to capture video.")
#         break

#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     fire = fire_cascade.detectMultiScale(frame, 1.2, 10)

#     for (x, y, w, h) in fire:
#         cv2.rectangle(frame, (x-20, y-20), (x+w+20, y+h+20), (255, 0, 0), 2)
        
#         if out is None:
#             out = initialize_video_writer(vid.get(3), vid.get(4))
            
#             if not runOnce:
#                 print("Alert Initiated")
#                 threading.Thread(target=alert_message_function).start()
#                 runOnce = True
#             else:
#                 print("Alert message already sent")

#         threading.Thread(target=play_alarm_sound_function).start()
#         out.write(frame)

#     cv2.imshow("Fire Detector", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release resources
# vid.release()
# if out:
#     out.release()
# cv2.destroyAllWindows()
