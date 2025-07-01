# SpecterPanel (C2 Server)

**SpecterPanel** is an advanced online hacking tool designed to provide a comprehensive suite of functionalities for various hacking and penetration testing activities. The project is built using Flask and SQLAlchemy, and it includes multiple modules to handle different tasks.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Installation

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

## Usage

1. **Run the Application**
    ```bash
    flask run
    ```

2. **Access the Application**
    Open your web browser and navigate to `http://127.0.0.1:5000`

## Features

### Main Application (`app.py`)
- Initializes the Flask app.
- Registers various blueprints for handling different parts of the application.
- Sets the secret key for session management.

### API Handling (`api/api.py`)
- Defines routes for handling API commands.
- Uses a blueprint to organize the API routes.

### Database Models (`db/modle.py`)
- Defines the structure of the database tables using SQLAlchemy models.
- Includes models for users, API commands, API links, phishing data, and more.

### Views and Templates (`view/view.py`, `templates`)
- Handles the rendering of HTML templates for different routes.
- Includes routes for user profile, API commands, and other functionalities.

### Event Handling (`evet/event.py`)
- Defines routes for error handling pages (e.g., 404 and 500 errors).

### Database Initialization (`initial_db.py`)
- Contains scripts for initializing the database tables.

### Utility Functions (`utility/control_db.py`, `utility/setting.py`)
- Provides utility functions for database management and application settings.
- Includes a script for controlling an SQLite database and setting various configuration variables.

### Homepage and Public Pages (`homePage/public.py`)
- Defines routes for public pages like login, register, and information pages.
- Uses session management for user authentication.

### Static Files (`static/py/netcat-v1.5.py`)
- Contains a network utility script for various network operations.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request to contribute to the project.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
