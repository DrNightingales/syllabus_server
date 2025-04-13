# 📚 Syllabus App (Local Development Only)

A lightweight Flask-based application for managing course syllabi, tracking weekly progress, and organizing supplementary materials. Designed for **local use only** (not production-ready).

---

## 🚀 Features

- **Course Management**: Create, view, and delete courses.
- **Weekly Tracking**: Add theory, problems, challenges, and projects for each week.
- **Progress Monitoring**: Track completion status per week/course.
- **Modular Design**: Blueprint-based routing (`/courses`, `/progress`, `/weeks`).
- **SQLite Database**: Built-in DB for local persistence.

---

## ⚠️ Important Warning

**This project is intended for local development only.**  

- 🔒 No security features (e.g., authentication, HTTPS).
- 📂 Data is stored in local SQLite files (e.g., `syllabus.db`).

---

## 🛠 Setup

### Prerequisites

- Python 3.8+
- Flask (install via `requirements.txt`)

### Installation

1. Clone the repository:

```bash
   git clone <repo-url>
   cd syllabus-app

```

1. Install dependencies:

```bash
pip install -r requirements.txt
```

### Run the app locally

```bash
python run.py
```

Access at: <http://localhost:5000>

### 🤖 AI Assistance Note

This project was developed with the assistance of DeepSeek Coder AI (by DeepSeek Company). Human review was applied for adherence to project rules.
