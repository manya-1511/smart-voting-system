from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch

# Text-to-speech function
def speak(text):
    speaker = Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

# Initialize webcam
video = cv2.VideoCapture(0)

# Load face detection model
face_detect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Create data directory if not present
if not os.path.exists('data/'):
    os.makedirs('data/')

# Load face labels and features
with open('data/num.pkl', 'rb') as f:
    LABELS = pickle.load(f)
with open('data/faces_data.pkl', 'rb') as f:
    FACES = pickle.load(f)

# Train the KNN classifier
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

# Load background image
imgBackground = cv2.imread("bg.png")
if imgBackground is None:
    print("Error: Background image not found or path is incorrect!")

# CSV column headers
COL_NAME = ['NAME', 'AADHAR', 'VOTE', 'DATE', 'TIME']

# Function to check if person has already voted
def check_if_exists(value):
    try:
        with open("Votes.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row and row[0] == value:
                    return True
    except FileNotFoundError:
        pass
    return False

recognized_name = None

while True:
    ret, frame = video.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Resize frame to match background region size (640x480)
    frame = cv2.resize(frame, (640, 480))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        crop_img = frame[y:y + h, x:x + w]
        resized_img = cv2.resize(crop_img, (50, 50))
        face_array = resized_img.flatten().reshape(1, -1)

        try:
            output = knn.predict(face_array)
            recognized_name = output[0]
        except Exception as e:
            print("Prediction error:", e)
            continue

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
        cv2.putText(frame, str(recognized_name), (x, y - 10),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
        break  # process only first detected face

    # Show frame on background
    if imgBackground is not None:
        # Make a copy so original background stays intact for next frame
        imgShow = imgBackground.copy()
        imgShow[370:370 + 480, 225:225 + 640] = frame
        cv2.imshow('frame', imgShow)
    else:
        cv2.imshow('frame', frame)

    if recognized_name is not None:
        print(f"Recognized: {recognized_name}")
        speak(f"Hello {recognized_name}, please cast your vote.")
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video and close windows
video.release()
cv2.destroyAllWindows()

# Voting prompt in terminal
if recognized_name:
    if check_if_exists(recognized_name):
        speak("You have already voted. Thank you!")
        print("You have already voted.")
    else:
        print("Please cast your vote:")
        print("1 - BJP")
        print("2 - CONGRESS")
        print("3 - JDS")
        print("4 - NOTA")
        vote_choice = input("Enter your vote (1/2/3/4): ").strip()

        vote_map = {'1': "BJP", '2': "CONGRESS", '3': "JDS", '4': "NOTA"}

        if vote_choice in vote_map:
            vote_value = vote_map[vote_choice]
            ts = time.time()
            date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
            timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")

            file_exists = os.path.isfile("Votes.csv")
            with open("Votes.csv", "a", newline="") as csvfile:
                writer = csv.writer(csvfile)
                if not file_exists:
                    writer.writerow(COL_NAME)
                # Store Aadhar along with Name and vote
                writer.writerow([recognized_name, recognized_name, vote_value, date, timestamp])

            speak("Your vote has been recorded. Thank you for voting.")
            print("Vote recorded successfully.")
        else:
            speak("Invalid vote choice.")
            print("Invalid vote choice.")
else:
    print("No face recognized. Exiting.")
