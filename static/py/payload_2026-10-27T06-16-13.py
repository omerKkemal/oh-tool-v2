import subprocess
import sys

def run_cmd(cmd):
    try:
        subprocess.run(cmd, check=True)
        return True
    except FileNotFoundError:
        return False

def text_to_speech(text):
    if sys.platform.startswith('linux'):
        if run_cmd(['espeak-ng', text]):
            return
        if run_cmd(['espeak', text]):
            return
        if run_cmd(['spd-say', text]):
            return

    elif sys.platform == 'darwin':
        if run_cmd(['say', text]):
            return

    print("No working TTS engine found.")

text_to_speech("how are you muaz stupid , and what are you doing right now?")