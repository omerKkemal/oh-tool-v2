# =========================================================================== #
# Author: Omer Kemal                                                          #
# Website: https://www.johndoe.com                                            #
# Social Media:                                                               #
#   - Facebook: https://www.facebook.com/johndoe                              #
#   - Telegram: https://t.me/johndoe                                          #
#   - Twitter: @JohnDoe                                                       #
#   - GitHub: https://github.com/johndoe                                      #
# =========================================================================== #

from datetime import datetime
import random
import string
import filelock
import os


class Setting:
    """
    The Setting class is responsible for storing application settings and
    providing utility methods for generating random identifiers, logging events,
    and managing configuration paths and database details.
    """

    def setting_var(self):
        """
        This function initializes various application settings, including:
        - Secret key for the application
        - Event and log message constants
        - Paths for log files and database files
        - Database connection URI
        - Admin user credentials
        - User roles and access levels
        - Folder paths for static files and templates

        These settings can be used across the application for consistent configuration.
        """
        # app setting
        self.SECRAT_KEY = ''.join(random.choices(
            string.ascii_uppercase + string.ascii_lowercase + string.digits, k=100
        ))


        # log dir path
        self.LOG_DIR = "utility/log/"
        self.LOG_FILE_NAME = "log.txt"

        # email setting
        self.ADMIN_EMAIL = 'omerkemal2019@gmail.com'
        self.EMAIL_PASSWORD = 'your password'
        self.EMAIL = 'your email(gmail)'
        self.SMTP_LINK = 'smtp.gmail.com'
        self.SMTP_PORT = 587
        self.EMAIL_TYPE = "html"

        # database config
        self.DB_NAME = "oh-tool.db"
        self.DB_DIR = 'db'
        self.DB_URI = f'sqlite:///{self.DB_DIR}/{self.DB_NAME}'

    def ID(self,n=5):
        """
        Generates a random alphanumeric ID of length 5. This ID can be used
        for creating unique identifiers for entities in the system, such as users,
        events, or records.

        Returns:
            str: A randomly generated 5-character string consisting of uppercase letters,
                 lowercase letters, and digits.
        """
        RandomID = ''.join(
            random.choices(
                string.ascii_uppercase + string.ascii_lowercase + string.digits, k=n
            )
        )
        return RandomID

    def log(self, event):
        """
        Records an event in the application log file with a timestamp.
        The event is appended to a log file with a date and time when it occurred.

        A file lock is used to prevent simultaneous access to the log file, ensuring
        thread safety when logging events.

        Args:
            event (str): The event message that describes the action or occurrence.
        """
        # Use file lock to prevent concurrent access to the log file
        lock = filelock.FileLock('counter.lock')
        event_rec = datetime.now()  # Capture the current timestamp

        with lock:
            # Open the log file in append mode and write the event with timestamp
            with open(self.LOG_DIR + self.LOG_FILE_NAME, "a") as f:
                f.write(f"[  {str(event_rec)}  ] : {str(event)}\n")

