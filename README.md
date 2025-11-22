# ResearchHub — Research Paper Management System

ResearchHub is a role-based academic publishing and peer-review workflow platform.  
Authors submit papers, editors assign reviewers, and reviewers provide evaluations.  
Designed to streamline conferences, journals, and institutional research reviews.

---

## ✅ Features
- Author paper submission & tracking  
- Editor dashboard, reviewer assignment & decisions  
- Reviewer feedback, scoring & commenting  
- Role-based authentication and permissions  
- Status updates & clean UI dashboards  

---

## 🛠️ Tech Stack
- **Backend:** Django, Python  
- **Database:** SQLite/PostgreSQL  
- **Frontend:** Django Templates, HTML, CSS  
- **Auth:** Django built-in authentication  

---

## 📌 Prerequisites
Make sure the following are installed:

- Python 3.9+
- Git
- pip

---

## 📂 Clone the Repository
```sh
git clone https://github.com/muthukumar9360/PaperReview_Portal.git
cd PaperReview_Portal
```

---

## 🧰 Create & Activate Virtual Environment

### Windows
```sh
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux
```sh
python3 -m venv venv
source venv/bin/activate
```
---

## 🗄️ Database Setup
```sh
python manage.py migrate
```

---

## 👑 Create Superuser
```sh
python manage.py createsuperuser
```

---

## ▶️ Run the Project
```sh
python manage.py runserver
```

Now visit:
```
http://127.0.0.1:8000/
```

---

## 🔑 User Roles
- **Author** → Upload and track research papers  
- **Reviewer** → Review assigned papers  
- **Editor** → Manage submissions and decisions  

---

## 🚀 Project Structure
```
PaperReview_Portal/
 ├─ media/
 ├─ reviews/
 ├─ templates/
 ├─ static/
 ├─ manage.py
```

---

✅ Fully scalable for institutions  
💡 Easy to customize and extend  
🚀 Ideal for academic events & journals
