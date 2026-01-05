# SpecterPanel - Command and Control (C2) Platform

**SpecterPanel** is a professional, modular, and extensible Command and Control (C2) platform built for cybersecurity professionals, penetration testers, and red teams. Developed with Flask and SQLAlchemy, it provides a unified web-based interface for managing security operations, automating tasks, and conducting penetration testing activities with ease and precision.

---

## 🚀 Overview

SpecterPanel streamlines security workflows by integrating multiple operational modules into a single, cohesive system. Its modular architecture allows for easy customization and scaling, making it suitable for both individual professionals and security teams. The platform is designed with an emphasis on usability, security, and extensibility.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Architecture](#-architecture)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## ✨ Features

- **🔐 Secure Authentication** – User login, registration, and session management.
- **📊 Interactive Dashboard** – Centralized overview of all platform activities.
- **🔗 API Management** – Easily manage API endpoints and command execution.
- **💾 Database Control** – SQLAlchemy-powered models for users, commands, phishing data, and more.
- **🖥️ Web Terminal** – Built-in terminal for direct server interaction.
- **🧪 Code Playground** – Secure environment for testing and executing code snippets.
- **🌐 Network Utilities** – Includes tools like `netcat-v1.5.py` for advanced network operations.
- **⚙️ Settings Panel** – Configure application parameters and user preferences.
- **📄 Error Handling** – Custom error pages and event logging.

---

## 🛠 Installation

Follow these steps to set up SpecterPanel locally:

### 1. Clone the Repository
```bash
git clone https://github.com/omerKkemal/oh-tool-v2.git
cd oh-tool-v2
```

### 2. Create and Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize the Database
```bash
python initial_db.py
```

### 5. Run the Application
```bash
flask run
```

### 6. Access the Platform
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🧠 Usage

Once SpecterPanel is running:

1. **Log in** using the secure login interface.
2. Navigate the **Dashboard** for an overview of available modules.
3. Use the **API Management** section to configure and monitor API endpoints.
4. Explore the **Code Playground** for safe code execution.
5. Manage system settings and user profiles via the **Settings** panel.
6. Utilize the **Web Terminal** for direct command-line access.

---

## 🏗 Architecture

```
SpecterPanel/
├── app.py                  # Main Flask application
├── api/api.py              # API route definitions
├── db/modle.py             # SQLAlchemy models
├── view/view.py            # View controllers
├── templates/              # HTML templates
├── evet/event.py           # Error and event handlers
├── homePage/public.py      # Public routes (login, register)
├── utility/                # Helper scripts (DB control, settings)
├── static/                 # Static assets (CSS, JS, scripts)
└── initial_db.py           # Database initialization
```

---

## 📸 Screenshots

| Dashboard | API Management | Code Playground |
|-----------|----------------|-----------------|
| ![Dashboard](screen_shot/dashbord.png) | ![API Link Management](screen_shot/api_link.png) | ![Code Playground](screen_shot/code_ground.png) |

| Home Page | Login | Web Terminal |
|-----------|-------|--------------|
| ![Home Page](screen_shot/home.png) | ![Login](screen_shot/login.png) | ![Web Terminal](screen_shot/webTerminal.png) |

| Settings Panel |
|----------------|
| ![Settings](screen_shot/setting.png) |

---

## 🤝 Contributing

Contributions are welcome!  
Please fork the repository and submit a pull request with a clear description of your changes.

---

## 📜 License

This project is licensed under a **Proprietary License**.  
All rights reserved by **Omer Kemal**.

Unauthorized use, copying, modification, or distribution is strictly prohibited.  
For licensing inquiries, please contact: 📧 **omerkemal2019@gmail.com**.

See the [LICENSE](LICENSE) file for full details.

---

## 📬 Contact

**Author:** Omer Kemal  
**Email:** omerkemal2019@gmail.com  
**GitHub:** [omerKkemal](https://github.com/omerKkemal)

---

> ⚠️ **Disclaimer:** This tool is intended for **authorized security testing and educational purposes only**. Misuse of this software is strictly prohibited.

---
