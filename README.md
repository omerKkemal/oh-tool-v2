# SpecterPanel (C2 Server)

**SpecterPanel** is a sophisticated Command and Control (C2) platform designed to deliver a comprehensive suite of functionalities for cybersecurity professionals and penetration testers. Developed with Flask and SQLAlchemy, SpecterPanel features a modular architecture that facilitates seamless management of various operational tasks.

## Explanation

SpecterPanel provides an all-in-one web-based interface for managing security operations and conducting penetration testing activities. It streamlines workflows by integrating multiple modules—such as API management, database control, user authentication, and network utilities—into a unified system. Designed for flexibility and extensibility, SpecterPanel enables users to efficiently oversee and automate complex security operations, making it a valuable tool for security teams and professionals.

## Table of Contents

- [Explanation](#explanation)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

---

## Installation

To set up SpecterPanel on your system, follow these steps:

1. **Clone the Repository**
    ```bash
    git clone https://github.com/omerKkemal/oh-tool-v2.git
    cd oh-tool-v2
    ```

2. **Create a Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Initialize the Database**
    ```bash
    python initial_db.py
    ```

---

## Usage

1. **Start the Application**
    ```bash
    flask run
    ```

2. **Access the Dashboard**
    Open your web browser and navigate to: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Features

SpecterPanel is designed with extensibility and user experience in mind. The following modules are included:

### Main Application (`app.py`)
- Initializes the Flask application.
- Registers modular blueprints for different functionalities.
- Configures session management and application security.

### Dashboard Overview
The dashboard provides a comprehensive overview and access to all main functionalities of SpecterPanel.
![Dashboard](screen_shot/dashbord.png)

### API Handling (`api/api.py`)
- Organizes and defines API routes for command execution.
- Utilizes Flask blueprints for scalable API development.

#### API Link Management
Efficiently manage API connections and endpoints through the dedicated API Link Management interface.
![API Link Management](screen_shot/api_link.png)

### Database Models (`db/modle.py`)
- Implements database schema using SQLAlchemy ORM.
- Defines models for users, API commands, API links, phishing data, and more.

### Views and Templates (`view/view.py`, `templates`)
- Renders dynamic HTML templates for all major user-facing routes.
- Includes user profile management, command execution, and additional web interfaces.

#### Code Playground
Experiment, test, and execute code snippets in a secure playground environment.
![Code Playground](screen_shot/code_ground.png)

### Event Handling (`evet/event.py`)
- Manages application-level error handling (e.g., 404, 500 error pages).

### Database Initialization (`initial_db.py`)
- Provides automated scripts for initial database setup.

### Utility Functions (`utility/control_db.py`, `utility/setting.py`)
- Contains helper scripts for database management and application configuration.
- Facilitates streamlined SQLite operations and environment settings.

### Homepage and Public Pages (`homePage/public.py`)
- Handles authentication processes including login and registration.
- Manages public informational pages with secure session handling.

#### Home Page
The home page serves as the entry point to the platform, providing access to key features and modules.
![Home Page](screen_shot/home.png)

#### Login Interface
Secure user authentication is provided through a streamlined login interface.
![Login](screen_shot/login.png)

### Application Settings
Configure various operational parameters and preferences in the settings section.
![Settings](screen_shot/setting.png)

### Static Files (`static/py/netcat-v1.5.py`)
- Includes a robust network utility script for advanced network operations.

### Web Terminal
Interact with the server environment through a built-in web terminal.
![Web Terminal](screen_shot/webTerminal.png)

---

## Contributing

We welcome contributions from the community! To contribute, please open an issue or submit a pull request with detailed information about your changes.

---

## License

This project is licensed under the GNU License. For more information, please refer to the [LICENSE](LICENSE) file.
