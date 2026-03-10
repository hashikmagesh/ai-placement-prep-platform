# 🚀 AI Placement Preparation Platform

An **AI-powered placement preparation platform** built with **Django** that helps students prepare for technical interviews, coding rounds, and aptitude tests using AI assistance.

---

# 📌 Features

### 🤖 AI Roadmap Generator

Generates a personalized preparation roadmap based on:

* Target domain
* Target company
* Preparation timeline

### 📄 AI Resume Analyzer (ATS Based)

Analyzes your resume against a **Job Description** and provides:

* Missing keywords
* Resume improvements
* ATS score insights

### 💻 Coding Practice

AI generates **coding questions** tailored to:

* Your target company
* Your domain

### 🧠 Aptitude Practice

Practice aptitude questions generated dynamically for interview preparation.

### 🎤 Interview Preparation

AI generates **technical interview questions with answers**.

### 🤖 AI Chat Assistant

Ask any career or technical question and get AI assistance.

### 📊 Placement Progress Dashboard

Track your preparation progress including:

* Coding
* Aptitude
* Interview readiness

### 👤 Profile System

User profile includes:

* Resume upload
* LinkedIn
* GitHub
* Portfolio
* Profile completion tracker

### 🔥 Login Streak Tracker

Tracks your **daily preparation streak**.

---

# 🛠 Tech Stack

**Backend**

* Django
* Python

**AI Integration**

* Google Gemini API

**Frontend**

* HTML
* CSS
* JavaScript
* Django Templates

**Database**

* SQLite (development)

---

# 📂 Project Structure

```
placement_prep/
│
├── manage.py
├── requirements.txt
├── placement/        # Django project settings
│
├── prep/             # Main application
│   ├── views.py
│   ├── models.py
│   ├── forms.py
│   ├── ai_service.py
│   ├── urls.py
│   ├── templates/
│   └── static/
```

---

# ⚙️ Installation

### 1️⃣ Clone Repository

```
git clone https://github.com/hashikmagesh/ai-placement-prep-platform.git
```

### 2️⃣ Navigate to Project

```
cd ai-placement-prep-platform
```

### 3️⃣ Create Virtual Environment

```
python -m venv venv
```

### 4️⃣ Activate Environment

Windows

```
venv\Scripts\activate
```

### 5️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root.

Example:

```
GEMINI_API_KEY=your_api_key_here
```

---

# ▶️ Run the Project

```
python manage.py migrate
python manage.py runserver
```

Open in browser:

```
http://127.0.0.1:8000/
```

---

# 📈 Future Improvements

* Leaderboard system
* AI mock interviews
* Resume scoring system
* Company-specific preparation tracks
* Deployment with Docker

---

# 👨‍💻 Author

**Hashik Magesh**

GitHub
https://github.com/hashikmagesh

---

⭐ If you like this project, consider giving it a **star**!
