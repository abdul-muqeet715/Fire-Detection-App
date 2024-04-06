import cv2
import threading
import playsound
import requests
import datetime
import os
import mysql.connector
import boto3
from twilio.rest import Client
from dotenv import load_dotenv


load_dotenv()

# Path to Haar Cascade classifier XML file
fire_cascade_path = "fire_detection.xml"

# Path to audio file for alarm
audio_path = "audio.mp3"

# Your Rapiwha API key
rapiwha_api_key = os.getenv("RAPIWHA_API_KEY")

# Your mobile number for sending alerts
owner_mobile_number = os.getenv("OWNER_MOBILE_NUMBER")

address = os.getenv("OWNER_ADDRESS")

latitude = os.getenv("OWNER_LATITUDE")

longitude = os.getenv("OWNER_LONGITUDE")

# S3 bucket configuration
S3_BUCKET = os.getenv("S3_BUCKET")

S3_ACCESS_POINT = 'video-storage-servic-s7n4z46jtiygezqny8phutj6mj6w6use2b-s3alias'

#S3 Access Key
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")

#S3 Secret Key
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")

DISTRIBUTION_DOMAIN_NAME = os.getenv("DISTRIBUTION_DOMAIN_NAME")

account_sid = os.getenv("ACCOUNT_SID")

auth_token = os.getenv("AUTH_TOKEN")

client = Client(account_sid, auth_token)

s3 = boto3.client('s3', aws_access_key_id=S3_ACCESS_KEY, aws_secret_access_key=S3_SECRET_KEY)

conn = mysql.connector.connect(
    host = os.getenv("HOST"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD"),
    database = os.getenv("DATABASE")
)

# SQLite database configuration
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS fire_incidents (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        location TEXT,
        start_time DATETIME,
        end_time DATETIME,
        duration INTEGER,
        mobile_number TEXT,
        latitude TEXT,
        longitude TEXT,
        video_url TEXT
    )
''')
conn.commit()

no_of_no_fire_detected = 0

fire_cascade = cv2.CascadeClassifier(fire_cascade_path)

vid = cv2.VideoCapture(0)
runOnce = False
recording = False
video_writer = None
start_time = None
file_name = ""

def play_alarm_sound_function():
    playsound.playsound(audio_path, True)

def alert_message_function(location, mobile_number):
    message = f"EMERGENCY!!! FIRE Accident Took Place AT {location}. PLEASE SEND FIRE FIGHTERS AND FIRE ENGINES AT THE LOCATION."
    querystring = {"apikey": rapiwha_api_key, "number": mobile_number, "text": message}
    url = "https://panel.rapiwha.com/send_message.php"
    response = requests.request("GET", url, params=querystring)
    print(response.text)

def alert_call_function(location,mobile_number):
    message = f"EMERGENCY!!! FIRE Accident Took Place AT {location}. PLEASE SEND FIRE FIGHTERS AND FIRE ENGINES AT THE LOCATION."
    print("calling the owner")
    call = client.calls.create(
                        twiml='<Response><Say>Emergency Fire took place at Azim home please send fire fighters</Say></Response>',
                        to='+917893209954',
                        from_="15409082473"
                    )
    print(call.sid)

def upload_to_s3(file_path, s3_bucket, s3_access_point):
    global DISTRIBUTION_DOMAIN_NAME
    file_name = os.path.basename(file_path)
    s3.upload_file(file_path, s3_bucket, file_name,ExtraArgs={'ContentType': 'video/mp4'})
    video_url = f"{DISTRIBUTION_DOMAIN_NAME}/{file_name}"
    return video_url

def save_to_database(location, start_time, end_time, duration, mobile_number, latitude, longitude, video_url):
    cursor.execute('''
        INSERT INTO fire_incidents (location, start_time, end_time, duration, mobile_number, latitude, longitude, video_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (location, start_time, end_time, duration, mobile_number, latitude, longitude, video_url))
    conn.commit()


def start_recording():
    global recording, video_writer, start_time , vid , file_name
    recording = True
    vid = cv2.VideoCapture(0)
    start_time = datetime.datetime.now()
    formatted_time = start_time.strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{formatted_time}_output.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use MP4 codec
    video_writer = cv2.VideoWriter(file_name, fourcc, 20.0, (640, 480))

def stop_recording():
    global recording, video_writer, start_time
    recording = False
    video_writer.release()
    vid.release()
    print(f"Video recording stopped. Duration: {datetime.datetime.now() - start_time}")

def process_fire_incident():
    location = "ABC Rubber Factory, Nampally X Roads, Hyderabad, Telangana"
    mobile_number = owner_mobile_number
    end_time = datetime.datetime.now()
    duration = (end_time - start_time).seconds
    location_latitude = latitude
    location_longitude = longitude

    # Upload video to S3
    video_url = upload_to_s3(file_name, S3_BUCKET, S3_ACCESS_POINT)
    
    # Save details to database
    save_to_database(location, start_time, end_time, duration, mobile_number, location_latitude, location_longitude ,video_url)

while(True):
    ret, frame = vid.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fire = fire_cascade.detectMultiScale(frame,1.2, 10)#(1.2,10)(2.0,10)
      # if already recording the continue recording
    if recording:
        video_writer.write(frame)
    
    if len(fire) > 0:
        print('Length of fire')
        print(len(fire))
        no_of_no_fire_detected = 0
        for (x,y,w,h) in fire:
            cv2.rectangle(frame,(x-20,y-20),(x+w+20,y+h+20),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

            if not runOnce:
                print("Fire alarm initiated")
                threading.Thread(target=play_alarm_sound_function).start()

                # if not already recording then start recording
                if not recording:
                    start_recording()
                location = "ABC Rubber Factory, Nampally X Roads, Hyderabad, Telangana"
                mobile_number = owner_mobile_number
                start_time = datetime.datetime.now()
                runOnce = True

                print("Alert Initiated")
                threading.Thread(target=alert_message_function, args=(location, mobile_number)).start()
                alert_call_function(location,mobile_number)
                threading.Thread(target=alert_call_function, args=(location, mobile_number)).start()
            if runOnce:
                print("Alert message already sent")

    else :
        no_of_no_fire_detected += 1
        print(no_of_no_fire_detected)
        if recording and no_of_no_fire_detected > 100:
            print("Stopping video recording...")
            threading.Thread(target=stop_recording).start()
            runOnce = False
            # Process fire incident details (upload to S3 and save to database)
            threading.Thread(target=process_fire_incident).start()

    cv2.imshow("Fire Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
if recording:
    stop_recording()
cv2.destroyAllWindows()