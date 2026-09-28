# SpeakUp – Public Complaint Management System

## 📌 Project Overview

SpeakUp is a web-based complaint management system built using **Django**.
It allows citizens to submit complaints about public issues such as road damage, garbage, street lights, etc., and track their status.

The system also provides an **admin dashboard** for managing complaints and monitoring reported issues.

---

## 🚀 Features

* User registration and login
* Submit complaints with images
* View and track complaint status
* Edit complaints
* Public complaint map (Public Eye)
* Notification system
* User profile management
* Admin dashboard for complaint monitoring
* Admin can manage and review complaints

---

## 🛠 Tech Stack

* **Backend:** Django (Python)
* **Frontend:** HTML, CSS, JavaScript
* **Database:** SQLite
* **Version Control:** Git & GitHub

---

## 📂 Project Structure

```
SpeakUp_Project
│
├── complaints/        # Complaint app
├── speakup/           # Django project settings
├── media/             # Uploaded complaint images
├── manage.py
└── db.sqlite3
```

---

## ▶️ How to Run the Project

1. Clone the repository

```
git clone https://github.com/kjoshna7/speakup-complaint-system.git
```

2. Go to the project folder

```
cd speakup-complaint-system
```

3. Activate virtual environment

Windows:

```
venv\Scripts\activate
```

4. Install dependencies

```
pip install django
```

5. Run the server

```
python manage.py runserver
```

6. Open in browser

```
http://127.0.0.1:8000/
```

---

## 👨‍💻 Author

Joshna K

---

## 📷 Future Improvements

* Email notifications
* Complaint priority automation
* Government department integration
* Mobile responsive design
