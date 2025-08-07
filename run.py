import os
os.environ['TCL_LIBRARY'] = r'C:\Users\hacker\AppData\Local\Programs\Python\Python313\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\hacker\AppData\Local\Programs\Python\Python313\tcl\tk8.6'

import customtkinter as ctk
import threading
import webbrowser
from tkinter import simpledialog
from db.mange_db import _create_engine, create_all_db_tables
from app import app
from werkzeug.serving import make_server
from pyngrok import ngrok, conf


def ensure_ngrok_auth():
    config = conf.get_default()
    if not config.auth_token:
        # Prompt for auth token via GUI
        root = ctk.CTk()
        root.withdraw()  # Hide unused main window
        token = simpledialog.askstring("Ngrok Auth", "Enter your ngrok auth token:")
        if not token:
            raise ValueError("Ngrok auth token is required to start the server.")
        config.auth_token = token


class ServerWrapper:
    def __init__(self, flask_app):
        self.flask_app = flask_app
        self.server = None
        self.thread = None
        self.is_running = False
        self.public_url = None
        self.tunnel = None

    def start(self):
        ensure_ngrok_auth()

        if not self.is_running:
            self.server = make_server("127.0.0.1", 5000, self.flask_app)
            self.thread = threading.Thread(target=self.server.serve_forever)
            self.thread.daemon = True
            self.thread.start()

            self.tunnel = ngrok.connect(5000)
            self.public_url = self.tunnel.public_url
            self.is_running = True

    def stop(self):
        if self.is_running:
            self.server.shutdown()
            self.thread.join()
            ngrok.disconnect(self.public_url)
            ngrok.kill()
            self.is_running = False
            self.public_url = None


class FlaskServerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SpecterPanel Server")
        self.geometry("450x370")
        self.resizable(False, False)

        create_all_db_tables(_create_engine())
        self.server = ServerWrapper(app)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.label = ctk.CTkLabel(self, text="SpecterPanel Flask Server", font=ctk.CTkFont(size=18, weight="bold"))
        self.label.pack(pady=20)

        self.status_label = ctk.CTkLabel(self, text="Server Status: OFF", text_color="red")
        self.status_label.pack(pady=5)

        self.url_label = ctk.CTkLabel(self, text="", wraplength=400)
        self.url_label.pack(pady=5)

        self.start_button = ctk.CTkButton(self, text="Start Server", command=self.start_server)
        self.start_button.pack(pady=10)

        self.stop_button = ctk.CTkButton(self, text="Stop Server", command=self.stop_server, state="disabled")
        self.stop_button.pack(pady=5)

        self.open_browser_button = ctk.CTkButton(self, text="Open in Browser", command=self.open_browser, state="disabled")
        self.open_browser_button.pack(pady=5)

        self.quit_button = ctk.CTkButton(self, text="Quit", command=self.quit)
        self.quit_button.pack(pady=20)

    def start_server(self):
        try:
            if not self.server.is_running:
                self.server.start()
                self.status_label.configure(text="Server Status: RUNNING", text_color="green")
                self.url_label.configure(text=f"Public URL:\n{self.server.public_url}")
                self.start_button.configure(state="disabled")
                self.stop_button.configure(state="normal")
                self.open_browser_button.configure(state="normal")
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}", text_color="red")

    def stop_server(self):
        if self.server.is_running:
            self.server.stop()
            self.status_label.configure(text="Server Status: STOPPED", text_color="orange")
            self.url_label.configure(text="")
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            self.open_browser_button.configure(state="disabled")

    def open_browser(self):
        if self.server.public_url:
            webbrowser.open(self.server.public_url)

    def quit(self):
        if self.server.is_running:
            self.server.stop()
        self.destroy()


if __name__ == "__main__":
    app_gui = FlaskServerApp()
    app_gui.mainloop()
