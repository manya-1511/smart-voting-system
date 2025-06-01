import cv2
import pickle
import numpy as np
import os
import csv

# Create data directory if it doesn't exist
if not os.path.exists('data/'):
    os.makedirs('data/')

video = cv2.VideoCapture(0)
face_detect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
faces_data = []

i = 0
name = input("Enter your name: ")
aadhar_num = input("Enter your Aadhar number: ")
framesTotal = 51
captureAfterFrame = 2

while True:
    ret, frame = video.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        crop_img = frame[y:y + h, x:x + w]
        resized_img = cv2.resize(crop_img, (50, 50))  # Color image (50x50x3 = 7500 features)

        if len(faces_data) <= framesTotal and i % captureAfterFrame == 0:
            faces_data.append(resized_img)
        i += 1

        cv2.putText(frame, str(len(faces_data)), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)

    cv2.imshow('Face Capture', frame)
    if cv2.waitKey(1) == ord('q') or len(faces_data) >= framesTotal:
        break

video.release()
cv2.destroyAllWindows()

# Convert and reshape data
faces_data = np.asarray(faces_data)
faces_data = faces_data.reshape((framesTotal, -1))  # Each image flattened to (7500,)

# Save Aadhar numbers
if 'num.pkl' not in os.listdir('data/'):
    num = [aadhar_num] * framesTotal
else:
    with open('data/num.pkl', 'rb') as f:
        num = pickle.load(f)
    num += [aadhar_num] * framesTotal

with open('data/num.pkl', 'wb') as f:
    pickle.dump(num, f)

# Save faces data
if 'faces_data.pkl' not in os.listdir('data/'):
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces_data, f)
else:
    with open('data/faces_data.pkl', 'rb') as f:
        existing_faces = pickle.load(f)
    faces = np.append(existing_faces, faces_data, axis=0)
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces, f)

# Save name and aadhar_num mapping in CSV for easy lookup during voting
labels_csv = 'data/labels.csv'
file_exists = os.path.isfile(labels_csv)
with open(labels_csv, mode='a', newline='') as file:
    writer = csv.writer(file)
    if not file_exists:
        writer.writerow(['NAME', 'AADHAR_NUM'])
    # Write the name and aadhar_num once (one row per person)
    writer.writerow([name, aadhar_num])

print(f"Face data for {name} (Aadhar: {aadhar_num}) saved successfully.")
