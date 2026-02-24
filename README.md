# SpecterPanel – Advanced Command & Control (C2) Platform

**SpecterPanel** is a modular, web‑based Command and Control (C2) platform designed for cybersecurity professionals, penetration testers, and red teams. Built with Flask and SQLAlchemy, it provides a unified interface for managing security operations, automating tasks, and coordinating offensive security workflows in a controlled and extensible environment.

> **⚠️ IMPORTANT DISCLAIMER**  
> This tool is intended **solely for authorized security testing and educational purposes**. Use responsibly and in compliance with all applicable laws and regulations. Unauthorized use is strictly prohibited.

---

## 📚 Table of Contents

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

SpecterPanel delivers a comprehensive suite of tools for managing cybersecurity operations through a centralized dashboard. It integrates **API management**, **database control**, **user authentication**, **network utilities**, **modular attack panels**, and **encrypted communication** into a single platform, enabling security teams to streamline workflows, automate tasks, and maintain operational oversight.

The platform works in tandem with agents like **PhantomGate** (a cross‑platform remote administration tool) to provide a complete C2 ecosystem. All communication between the server and agents is **AES‑encrypted** to ensure confidentiality and integrity.

---

## 🚀 Key Features

- **Modular Architecture** – Easily extendable with Flask blueprints and dedicated modules.
- **Unified Dashboard** – Real‑time overview of all platform activities and connected systems.
- **Encrypted API Communication** – AES‑EAX encryption for all request/response payloads.
- **Database Integration** – SQLAlchemy‑powered models for users, commands, logs, targets, and more.
- **Web Terminal** – Built‑in browser‑based terminal for executing commands on remote targets.
- **Code Injection Panel** – Manage, upload, and inject custom Python payloads into target systems.
- **Botnet Management** – Dedicated panel for managing distributed agents and botnet actions (UDP flood, brute‑force, etc.).
- **User Instruction System** – Assign and manage per‑user instructions for targets (web, socket, botnet).
- **API Token Management** – Generate, revoke, and manage API tokens for agent authentication.
- **Event & Error Handling** – Custom error pages and detailed logging for improved debugging.
- **Responsive UI** – Modern interface with dynamic templates and static asset support.
- **Socket Management** – Configure socket‑based communication with targets for persistent access.

---

## 📁 Project Structure

```
SpecterPanel/
├── api/
│   └── api.py              # Encrypted API endpoints (blueprint)
├── db/
│   ├── modle.py             # SQLAlchemy ORM models
│   ├── mange_db.py          # Database engine & session helpers
│   └── info.json            # Database metadata (optional)
├── event/
│   └── event.py             # Error handlers (404, 500, etc.)
├── log/
│   └── log.txt              # Application log file (auto‑created)
├── static/
│   ├── css/                 # Stylesheets
│   ├── js/                  # JavaScript files
│   └── py/                  # Python payloads (e.g., netcat-v1.5.py)
├── utility/
│   ├── control_db.py        # Database control helpers
│   ├── email_temp.py        # Email templating utilities
│   ├── processer.py         # Data processing (JSON, lists, output handling)
│   └── setting.py           # Global configuration (encryption keys, paths, etc.)
├── view/                    # Flask blueprints for web interface
│   ├── botNet_manager.py    # Botnet management routes
│   ├── code_injection_panel.py  # Code injection routes
│   ├── public.py            # Public routes (home, login, register)
│   ├── user_setting.py      # User settings & profile
│   ├── view.py              # Main views (dashboard, socket pages)
│   └── web_terminal.py      # Web terminal routes
├── templates/               # Jinja2 HTML templates
├── app.py                   # Main Flask application (registers blueprints)
├── initial_db.py            # Database initialization script
├── requirements.txt         # Python dependencies
└── screen_shot/             # Screenshots for documentation
    ├── dashbord.png
    ├── api_link.png
    ├── code_ground.png
    ├── home.png
    ├── login.png
    ├── webTerminal.png
    └── setting.png
```

---

## ⚙️ Installation

### Prerequisites
- Python 3.8+
- pip
- git
- (Optional) Virtual environment tool (venv, virtualenv)

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
   This creates the necessary SQLite database tables.

5. **Run the Application**
   ```bash
   flask run
   ```
   The server will start at [http://127.0.0.1:5000](http://127.0.0.1:5000).

6. **(Optional) Change Encryption Key**  
   Edit `utility/setting.py` and modify `ENCRYPTION_KEY` to a secure 16‑byte key.

---

## 🖥️ Usage

After starting the server, navigate to the homepage and register a new account. Once logged in, you can access the full suite of features:

- **Dashboard** – Overview of registered targets, their connection types (local, Wi‑Fi, Ethernet), and quick access to the web terminal.
- **Web Terminal** – Select a target and execute shell commands. Output is displayed in real‑time and stored in the database.
- **API Management** – Generate and manage API tokens for agents; all agent communication is encrypted.
- **Botnet Manager** – Add, update, or delete botnet instructions (UDP flood, brute‑force) for specific targets.
- **Code Injection Panel** – Upload Python scripts, edit them directly in the browser, and inject them into target systems. View execution outputs.
- **Socket Management** – Configure socket‑based backdoor connections (host/port) for targets.
- **User Settings** – Update your email/password, generate new API tokens, and delete your account (with data cleanup).

---

## 🧩 Modules & Components

| Module | Description |
|--------|-------------|
| **`app.py`** | Main Flask application; registers all blueprints and configures session security. |
| **`api/api.py`** | Encrypted API endpoints used by agents (PhantomGate) to fetch commands, report output, and retrieve botnet instructions. |
| **`db/modle.py`** | Defines SQLAlchemy models: `Users`, `Targets`, `APICommand`, `APILink`, `Instraction`, `Instruction_Detail`, `BotNet`, `code_injection_payloads`, and more. |
| **`view/`** | Blueprints handling all web interface routes (dashboard, terminal, settings, etc.). |
| **`utility/`** | Helper modules: `processer.py` (JSON read/write, list formatting), `setting.py` (configuration), `email_temp.py` (email templates). |
| **`event/event.py`** | Global error handlers (404, 500) and logging. |
| **`static/`** | Frontend assets and Python payloads for code injection. |
| **`templates/`** | Jinja2 HTML templates for all pages. |

---

## 🔐 API Endpoints

All API endpoints use **AES‑EAX encryption** for request/response payloads. Agents must include a valid API token in every request.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1.2/ApiCommand/<target_name>` | GET | Retrieve all pending commands for the specified target. |
| `/api/v1.2/Apicommand/save_output` | POST | Save command outputs from a target. |
| `/api/v1.2/BotNet/<target_name>` | GET | Fetch botnet instructions (UDP flood, brute‑force) for the target. |
| `/api/v1.2/registor_target` | POST | Register a new target with the system (creates default instructions). |
| `/api/v1.2/get_instraction/<target_name>` | GET | Retrieve high‑level operational instructions (web, socket, botnet) and user‑defined commands. |
| `/api/v1.2/injection/lib/<target_name>` | GET | Serve a Python payload file for remote code injection. |
| `/api/v1.2/injection/code_output_save/<target_name>` | POST | Save the output of an executed injected payload. |

All requests and responses are wrapped in an encrypted envelope. Example encrypted payload structure:
```json
{
    "nonce": "base64...",
    "ciphertext": "base64...",
    "tag": "base64..."
}
```

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
- **Project Repository**: [oh-tool-v2](https://github.com/omerKkemal/oh-tool-v2)

---

> ⚠️ **Disclaimer**: This tool is intended for **authorized security testing and educational purposes only**. Use responsibly and in compliance with applicable laws and regulations. The author assumes no liability for misuse.
