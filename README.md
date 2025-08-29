# 🧠🗳️ Smart Voting System | AI-Powered Face Recognition Based Voting

**Smart Voting System** is a secure, AI-driven election platform that uses **facial recognition** for voter authentication. It ensures **no duplicate votes**, provides **voice-guided assistance**, and maintains full **transparency** by logging each vote with **voter details and timestamps**.

This solution makes the voting process **safer**, **smarter**, and more **accessible** for all.

---

## 🌟 Features

- 👁️ **Real-time Face Detection & Recognition**  
  Utilizes OpenCV and **K-Nearest Neighbors (KNN)** classifier for accurate face recognition.

- 🔐 **Duplicate Vote Prevention**  
  Automatically detects if a voter has already voted — ensuring fair elections.

- 🗣️ **Voice Feedback Support**  
  Uses **Windows SAPI Text-to-Speech** to guide voters throughout the process.

- 📝 **Easy Voter Registration**  
  Captures face data and links it to a unique **Aadhar number**.

- 🧾 **Secure Vote Logging**  
  Records **voter info**, **vote choice**, and **timestamp** in a secure CSV file for auditing.

- 🎥 **User-Friendly Interface**  
  Live webcam feed on a **custom UI background** for a clean and intuitive experience.

---

## 🧠 Technologies Used

- **Python** (Backend Logic & Scripting)  
- **OpenCV** (Face Detection & Recognition)  
- **Scikit-learn** (KNN Classification)  
- **PyWin32** (Text-to-Speech via SAPI)  
- **NumPy & Pandas** (Data Handling & Storage)  
- **CSV** (Vote and Voter Data Storage)

---

## ⚙️ How It Works

### 1. 🧍 Voter Registration (`add_face.py`)
- Activates the webcam to capture multiple facial images.
- Stores face data along with **voter's name** and **Aadhar number** for future authentication.

### 2. 🗳️ Voting Process (`give_vote.py`)
- Starts webcam and detects voter face in real-time.
- Checks if the voter has already voted using stored records.
- If not voted:
  - Guides user through voice instructions.
  - Accepts and records the vote choice.
  - Logs the vote with **voter details** and **timestamp** into `votes.csv`.

---

## 🚀 Installation & Setup

### ✅ Prerequisites
Make sure **Python 3.x** is installed on your machine.

### 📦 Install Required Packages

```bash
pip install opencv-python scikit-learn numpy pywin32
