"""
Mobile Recorder for Termux
Works on Android with Termux
"""

from pathlib import Path
import queue
import random
import tempfile
import wave
import base64
from datetime import datetime
import time
import os
import threading
import subprocess
import sys

# Try importing audio libraries
try:
    import pyaudio
    USE_PYAUDIO = True
    print("✅ Using PyAudio")
except ImportError:
    USE_PYAUDIO = False
    print("⚠️ PyAudio not found, trying other methods...")

try:
    import sounddevice as sd
    import numpy as np
    import scipy.io.wavfile as wav
    USE_SOUNDDEVICE = True
    print("✅ Using sounddevice")
except ImportError:
    USE_SOUNDDEVICE = False
    print("⚠️ sounddevice not found")

# For Termux, try using termux-api for audio
try:
    import termux
    USE_TERMUX = True
    print("✅ Using termux-api")
except ImportError:
    USE_TERMUX = False
    print("⚠️ termux-api not found")

class MobileRecorder:
    def __init__(self, duration=300, screenshot_interval=30, audio_interval=(15, 30)):
        self.duration = duration
        self.screenshot_interval = screenshot_interval
        self.audio_interval = audio_interval
        self.audio_queue = queue.Queue()
        self.running = True
        
        # Setup directories (Android-friendly paths)
        self.base_dir = Path("/sdcard") / "Documents" / "recordings"
        self.pictures_dir = Path("/sdcard") / "Pictures" / "recordings"
        self.audio_dir = Path("/sdcard") / "Music" / "recordings"
        
        # Fallback to internal storage if SD card not available
        if not self.base_dir.exists():
            self.base_dir = Path.home() / "storage" / "shared" / "Documents" / "recordings"
            self.pictures_dir = Path.home() / "storage" / "shared" / "Pictures" / "recordings"
            self.audio_dir = Path.home() / "storage" / "shared" / "Music" / "recordings"
        
        # Create directories
        self.pictures_dir.mkdir(parents=True, exist_ok=True)
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n📁 Screenshots: {self.pictures_dir}")
        print(f"📁 Audio clips: {self.audio_dir}")
        print(f"⏱️ Duration: {duration} seconds")
        print("🔄 Press Ctrl+C to stop\n")
    
    def check_permissions(self):
        """Check and request permissions on Android"""
        if os.name == 'posix' and 'android' in os.uname().release.lower():
            try:
                # Check if we have storage permissions
                test_file = Path("/sdcard/test.txt")
                try:
                    test_file.write_text("test")
                    test_file.unlink()
                    print("✅ Storage permissions OK")
                except:
                    print("⚠️ Storage permissions needed")
                    print("Run: termux-setup-storage")
                    return False
                
                # Check if we can access microphone
                try:
                    subprocess.run(['termux-microphone-record', '-h'], 
                                 capture_output=True, check=True)
                    print("✅ Microphone permissions OK")
                except:
                    print("⚠️ Microphone permissions needed")
                    print("Run: termux-microphone-record -h")
                    return False
                
                return True
            except:
                return False
        return True
    
    def capture_screenshot_termux(self):
        """Take screenshot using termux-api"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = self.pictures_dir / f"screenshot_{timestamp}.png"
            
            # Use termux-screenshot
            cmd = ['termux-screenshot', str(filename)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and filename.exists():
                print(f"📸 Screenshot: {filename.name}")
                return filename
            else:
                print(f"❌ Screenshot failed: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ Screenshot error: {e}")
            return None
    
    def capture_screenshot_pil(self):
        """Take screenshot using PIL (fallback)"""
        try:
            from PIL import ImageGrab
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = self.pictures_dir / f"screenshot_{timestamp}.png"
            
            img = ImageGrab.grab()
            img.save(filename)
            print(f"📸 Screenshot: {filename.name}")
            return filename
            
        except Exception as e:
            print(f"❌ Screenshot error: {e}")
            return None
    
    def take_screenshot(self):
        """Take screenshot using available method"""
        # Try termux-api first (Android)
        if USE_TERMUX or os.name == 'posix':
            result = self.capture_screenshot_termux()
            if result:
                return result
        
        # Fallback to PIL
        return self.capture_screenshot_pil()
    
    def record_audio_termux(self):
        """Record audio using termux-api"""
        try:
            duration = random.uniform(10, 20)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = self.audio_dir / f"audio_{timestamp}.wav"
            
            print(f"🎤 Recording {duration:.1f}s...", end="")
            
            # Use termux-microphone-record
            cmd = [
                'termux-microphone-record',
                '-d', str(int(duration)),
                '-f', str(filename)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and filename.exists():
                # Read and encode
                with open(filename, 'rb') as f:
                    encoded = base64.b64encode(f.read()).decode()
                
                self.audio_queue.put(("AUDIO", encoded, str(filename)))
                print(f" ✅ Audio saved: {filename.name}")
                return filename
            else:
                print(f" ❌ Audio failed: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ Termux audio error: {e}")
            return None
    
    def record_audio_pyaudio(self):
        """Record using PyAudio"""
        try:
            duration = random.uniform(10, 20)
            
            pa = pyaudio.PyAudio()
            
            stream = pa.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=1024,
                input_device_index=None
            )
            
            frames = []
            frames_to_read = int(44100 / 1024 * duration)
            
            for _ in range(frames_to_read):
                try:
                    data = stream.read(1024, exception_on_overflow=False)
                    frames.append(data)
                except Exception as e:
                    print(f"Read error: {e}")
                    break
            
            stream.stop_stream()
            stream.close()
            pa.terminate()
            
            if not frames:
                return None
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = self.audio_dir / f"audio_{timestamp}.wav"
            
            with wave.open(str(filename), 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(44100)
                wf.writeframes(b''.join(frames))
            
            with open(filename, 'rb') as f:
                encoded = base64.b64encode(f.read()).decode()
            
            self.audio_queue.put(("AUDIO", encoded, str(filename)))
            print(f"🎵 Audio saved: {filename.name} ({duration:.1f}s)")
            return filename
            
        except Exception as e:
            print(f"❌ PyAudio error: {e}")
            return None
    
    def record_audio_sounddevice(self):
        """Record using sounddevice"""
        try:
            duration = random.uniform(10, 20)
            sample_rate = 44100
            
            print(f"🎤 Recording {duration:.1f}s...", end="")
            
            recording = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=1,
                dtype='int16'
            )
            sd.wait()
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = self.audio_dir / f"audio_{timestamp}.wav"
            
            wav.write(str(filename), sample_rate, recording)
            
            with open(filename, 'rb') as f:
                encoded = base64.b64encode(f.read()).decode()
            
            self.audio_queue.put(("AUDIO", encoded, str(filename)))
            print(f" ✅ Audio saved: {filename.name}")
            return filename
            
        except Exception as e:
            print(f" ❌ Sounddevice error: {e}")
            return None
    
    def record_audio(self):
        """Record audio using available method"""
        # Try termux-api first (Android)
        if USE_TERMUX:
            result = self.record_audio_termux()
            if result:
                return result
        
        # Try PyAudio
        if USE_PYAUDIO:
            result = self.record_audio_pyaudio()
            if result:
                return result
        
        # Try sounddevice
        if USE_SOUNDDEVICE:
            result = self.record_audio_sounddevice()
            if result:
                return result
        
        print("❌ No audio recording method available")
        print("Install termux-api or pyaudio")
        return None
    
    def screenshot_loop(self):
        """Loop for screenshots"""
        while self.running:
            self.take_screenshot()
            time.sleep(self.screenshot_interval)
    
    def audio_loop(self):
        """Loop for audio recording"""
        while self.running:
            wait_time = random.uniform(*self.audio_interval)
            time.sleep(wait_time)
            self.record_audio()
    
    def run(self):
        """Start recording"""
        # Check permissions
        if not self.check_permissions():
            print("\n⚠️ Please grant permissions first!")
            print("Run these commands in Termux:")
            print("  termux-setup-storage")
            print("  termux-microphone-record -h")
            print("\nThen run this script again.")
            return
        
        # Check if any audio method is available
        if not (USE_PYAUDIO or USE_SOUNDDEVICE or USE_TERMUX):
            print("\n❌ No audio library available. Install with:")
            print("  pip install pyaudio  # or")
            print("  pip install sounddevice scipy  # or")
            print("  Use termux-api with: pkg install termux-api")
            print("\nContinuing with screenshots only...")
        
        # Start threads
        screenshot_thread = threading.Thread(target=self.screenshot_loop, daemon=True)
        audio_thread = threading.Thread(target=self.audio_loop, daemon=True)
        
        screenshot_thread.start()
        audio_thread.start()
        
        print("✅ Recording started!\n")
        
        # Run for duration
        try:
            start_time = time.time()
            while self.running and (time.time() - start_time) < self.duration:
                time.sleep(1)
                # Print progress every 30 seconds
                elapsed = int(time.time() - start_time)
                remaining = self.duration - elapsed
                if elapsed % 30 == 0 and elapsed > 0:
                    print(f"⏱️ Progress: {elapsed}/{self.duration}s remaining: {remaining}s")
                    
        except KeyboardInterrupt:
            print("\n⏹️ Stopped by user")
        
        self.running = False
        print(f"\n✅ Recording complete!")
        
        # Count files
        screenshots = list(self.pictures_dir.glob('*.png'))
        audio_files = list(self.audio_dir.glob('*.wav'))
        print(f"📊 Screenshots: {len(screenshots)}")
        print(f"📊 Audio clips: {len(audio_files)}")
        print(f"📁 Files saved in: {self.base_dir}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Mobile Recorder for Termux")
    parser.add_argument("-d", "--duration", type=int, default=300,
                       help="Total duration in seconds (default: 300)")
    parser.add_argument("-s", "--screenshot-interval", type=int, default=30,
                       help="Seconds between screenshots (default: 30)")
    parser.add_argument("-a", "--audio-interval", type=int, default=20,
                       help="Average seconds between audio clips (default: 20)")
    parser.add_argument("--audio-only", action="store_true",
                       help="Only record audio")
    parser.add_argument("--screenshot-only", action="store_true",
                       help="Only take screenshots")
    parser.add_argument("--single", action="store_true",
                       help="Take a single screenshot")
    
    args = parser.parse_args()
    
    if args.single:
        rec = MobileRecorder()
        rec.take_screenshot()
        return
    
    if args.audio_only:
        rec = MobileRecorder(duration=60, screenshot_interval=9999)
        rec.record_audio()
        return
    
    if args.screenshot_only:
        rec = MobileRecorder(duration=args.duration, 
                           screenshot_interval=args.screenshot_interval,
                           audio_interval=(9999, 9999))
        rec.run()
        return
    
    # Normal recording
    rec = MobileRecorder(
        duration=args.duration,
        screenshot_interval=args.screenshot_interval,
        audio_interval=(max(10, args.audio_interval - 5), 
                       args.audio_interval + 5)
    )
    rec.run()

if __name__ == "__main__":
    main()