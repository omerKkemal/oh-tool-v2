# SpecterPanel – Advanced Command & Control (C2) Platform

**SpecterPanel** is a modular, web-based Command and Control (C2) platform designed for cybersecurity professionals, penetration testers, and red teams. Built with Flask and SQLAlchemy, it provides a unified interface for managing security operations, automating tasks, and coordinating offensive security workflows in a controlled and extensible environment.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Modules & Components](#modules--components)
- [API Endpoints](#api-endpoints)
- [Screenshots](#screenshots)
- [License](#license)
- [Contact](#contact)

---

## 📖 Overview

SpecterPanel delivers a comprehensive suite of tools for managing cybersecurity operations through a centralized dashboard. It integrates API management, database control, user authentication, network utilities, modular attack panels, and encrypted communication into a single platform, enabling security teams to streamline workflows, automate tasks, and maintain operational oversight.

---

## 🚀 Key Features

- **Modular Architecture** – Easily extendable with Flask blueprints and dedicated modules.
- **Unified Dashboard** – Real-time overview of all platform activities and connected systems.
- **Encrypted API Communication** – AES-encrypted payloads for secure command and data exchange.
- **Database Integration** – SQLAlchemy-powered models for users, commands, logs, targets, and more.
- **Web Terminal** – Built-in browser-based terminal for server interaction and command execution.
- **Code Injection Panel** – Manage and inject custom payloads into target systems.
- **Botnet Management** – Dedicated panel for managing distributed systems and agents.
- **Phishing & Injection Tools** – Integrated modules for social engineering and code injection tests.
- **User Instruction System** – Assign and manage per-user instructions for targets.
- **Event & Error Handling** – Custom error pages and logging for improved debugging.
- **Responsive UI** – Modern interface with dynamic templates and static asset support.

---

## 📁 Project Structure

```
SpecterPanel/
├── api/
│   └── api.py              # API route definitions and blueprint (encrypted endpoints)
├── db/
│   ├── modle.py            # SQLAlchemy models
│   ├── mange_db.py         # Database management utilities
│   └── info.json           # Database metadata or configuration
├── event/
│   └── event.py            # Error and event handlers (404, 500, etc.)
├── log/
│   └── log.txt             # Application log file
├── static/
│   ├── css/                # Stylesheets
│   ├── js/                 # JavaScript files
│   └── py/                 # Python utilities and payloads (e.g., netcat-v1.5.py)
├── utility/
│   ├── control_db.py       # Database control helpers
│   ├── email_temp.py       # Email templating utilities
│   ├── processer.py        # Data processing scripts
│   └── setting.py          # Application configuration
├── view/
│   ├── botNet_manager.py   # Botnet management interface
│   ├── code_injection_panel.py  # Code injection testing panel
│   ├── public.py           # Public routes (login, register, homepage)
│   ├── user_setting.py     # User profile and settings
│   ├── view.py             # Main view controllers (dashboard, socket pages)
│   └── web_terminal.py     # Web terminal interface
├── templates/              # HTML templates (Jinja2)
├── app.py                  # Main Flask application
├── initial_db.py           # Database initialization script
└── requirements.txt        # Python dependencies
```

---

## ⚙️ Installation

### Prerequisites
- Python 3.8+
- pip
- git

### Steps
1. **Clone the Repository**
   ```bash
   git clone https://github.com/omerKkemal/oh-tool-v2.git
   cd oh-tool-v2
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database**
   ```bash
   python initial_db.py
   ```

5. **Run the Application**
   ```bash
   flask run
   ```
   Access the dashboard at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🖥️ Usage

After starting the server, log in through the web interface to access:

- **Dashboard** – Overview of active targets, connection types, and system status.
- **Web Terminal** – Execute shell commands and monitor outputs for specific targets.
- **API Management** – Configure and monitor encrypted API endpoints.
- **Botnet Manager** – Control and monitor connected agents and distributed tasks.
- **Code Injection Panel** – Upload, edit, and inject custom payloads into targets.
- **Socket Management** – Configure socket-based communication with targets.
- **Settings** – Manage API tokens, user instructions, and account preferences.

---

## 🧩 Modules & Components

| Module | Description |
|--------|-------------|
| **`app.py`** | Main Flask app, registers blueprints and configures security. |
| **`api/api.py`** | Encrypted API routes for remote command execution, target registration, and data exchange. |
| **`db/modle.py`** | SQLAlchemy models (User, Target, APICommand, BotNet, Instruction, etc.). |
| **`view/`** | Contains all web interface controllers (dashboard, terminal, socket, etc.). |
| **`utility/`** | Helper scripts for DB control, email templating, settings, and payload processing. |
| **`event/event.py`** | Handles HTTP errors and application events. |
| **`static/`** | Frontend assets (CSS, JS) and payload files. |
| **`templates/`** | HTML templates for all pages. |

---

## 🔐 API Endpoints

All API endpoints use **AES encryption** for request/response payloads.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1.2/ApiCommand/<target_name>` | GET | Retrieve pending commands for a target. |
| `/api/v1.2/Apicommand/save_output` | POST | Save command outputs from targets. |
| `/api/v1.2/BotNet/<target_name>` | GET | Fetch botnet instructions for a target. |
| `/api/v1.2/registor_target` | POST | Register a new target with the system. |
| `/api/v1.2/get_instraction/<target_name>` | GET | Retrieve system/user instructions for a target. |
| `/api/v1.2/injection/lib/<target_name>` | GET | Serve static payload files (e.g., JS libraries). |
| `/api/v1.2/injection/code_output_save/<target_name>` | POST | Save output from executed injected code. |

---

## 📸 Screenshots

| Dashboard | API Link Management | Code Playground |
|-----------|---------------------|-----------------|
| ![Dashboard](screen_shot/dashbord.png) | ![API Link Management](screen_shot/api_link.png) | ![Code Playground](screen_shot/code_ground.png) |

| Home Page | Login Interface | Web Terminal |
|-----------|-----------------|--------------|
| ![Home Page](screen_shot/home.png) | ![Login](screen_shot/login.png) | ![Web Terminal](screen_shot/webTerminal.png) |

| Settings Panel |
|----------------|
| ![Settings](screen_shot/setting.png) |

---

## 📜 License

This project is licensed under a **Proprietary License**. All rights reserved by **Omer Kemal**.

Unauthorized use, copying, modification, or distribution is strictly prohibited.  
For licensing inquiries, contact: 📧 **omerkemal2019@gmail.com**.

---

## 📬 Contact

- **Author**: Omer Kemal  
- **Email**: omerkemal2019@gmail.com  
- **GitHub**: [omerKkemal](https://github.com/omerKkemal)  

---

> ⚠️ **Disclaimer**: This tool is intended for **authorized security testing and educational purposes only**. Use responsibly and in compliance with applicable laws and regulations.
