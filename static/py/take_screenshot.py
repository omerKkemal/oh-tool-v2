from pathlib import Path
import queue
import random
import tempfile
import wave
import base64
from PIL import ImageGrab
from datetime import datetime
import time
import os
import threading

# Try importing audio libraries
try:
    import pyaudio
    USE_PYAUDIO = True
    print("✅ Using PyAudio")
except ImportError:
    USE_PYAUDIO = False
    print("⚠️  PyAudio not found, trying sounddevice...")

try:
    import sounddevice as sd
    import numpy as np
    import scipy.io.wavfile as wav
    USE_SOUNDDEVICE = True
    print("✅ Using sounddevice")
except ImportError:
    USE_SOUNDDEVICE = False
    print("⚠️  sounddevice not found, audio recording disabled")

class Recorder:
    def __init__(self, duration=300, screenshot_interval=30, audio_interval=(15, 30)):
        self.duration = duration
        self.screenshot_interval = screenshot_interval
        self.audio_interval = audio_interval
        self.audio_queue = queue.Queue()
        self.running = True
        
        # Setup directories
        self.pictures_dir = Path.home() / "Pictures" / "recordings"
        self.pictures_dir.mkdir(parents=True, exist_ok=True)
        
        self.audio_dir = Path.home() / "Audio" / "recordings"
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n📁 Screenshots: {self.pictures_dir}")
        print(f"📁 Audio clips: {self.audio_dir}")
        print(f"⏱️  Duration: {duration} seconds")
        print("🔄 Press Ctrl+C to stop\n")
    
    def record_audio_pyaudio(self):
        """Record using PyAudio"""
        try:
            # Random duration between 10-20 seconds
            duration = random.uniform(10, 20)
            
            pa = pyaudio.PyAudio()
            
            # List available devices for debugging
            # for i in range(pa.get_device_count()):
            #     dev = pa.get_device_info_by_index(i)
            #     if dev['maxInputChannels'] > 0:
            #         print(f"Input device {i}: {dev['name']}")
            
            stream = pa.open(
                format=pyaudio.paInt16,  # Use pyaudio.paInt16
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=1024,
                input_device_index=None  # Use default input device
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
            
            # Save to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = self.audio_dir / f"audio_{timestamp}.wav"
            
            with wave.open(str(filename), 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(44100)
                wf.writeframes(b''.join(frames))
            
            # Read and encode
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
            
            # Record
            recording = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=1,
                dtype='int16'
            )
            sd.wait()
            
            # Save to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = self.audio_dir / f"audio_{timestamp}.wav"
            
            wav.write(str(filename), sample_rate, recording)
            
            # Encode
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
        if USE_PYAUDIO:
            return self.record_audio_pyaudio()
        elif USE_SOUNDDEVICE:
            return self.record_audio_sounddevice()
        else:
            print("❌ No audio library available")
            return None
    
    def take_screenshot(self):
        """Take screenshot"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = self.pictures_dir / f"screenshot_{timestamp}.png"
            
            # Try PIL
            try:
                img = ImageGrab.grab()
                img.save(filename)
                print(f"📸 Screenshot: {filename.name}")
                return filename
            except:
                # Try mss fallback
                try:
                    import mss
                    with mss.mss() as sct:
                        sct.shot(output=str(filename))
                    print(f"📸 Screenshot: {filename.name}")
                    return filename
                except:
                    print("❌ Screenshot failed")
                    return None
                    
        except Exception as e:
            print(f"❌ Screenshot error: {e}")
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
        # Check if audio is available
        if not (USE_PYAUDIO or USE_SOUNDDEVICE):
            print("❌ No audio library available. Install with:")
            print("  pip install pyaudio  # or")
            print("  pip install sounddevice scipy")
            return
        
        # Start threads
        screenshot_thread = threading.Thread(target=self.screenshot_loop, daemon=True)
        audio_thread = threading.Thread(target=self.audio_loop, daemon=True)
        
        screenshot_thread.start()
        audio_thread.start()
        
        print("✅ Recording started!\n")
        
        # Run for duration
        try:
            time.sleep(self.duration)
        except KeyboardInterrupt:
            print("\n⏹️  Stopped by user")
        
        self.running = False
        print(f"\n✅ Recording complete!")
        
        # Count files
        screenshots = list(self.pictures_dir.glob('*.png'))
        audio_files = list(self.audio_dir.glob('*.wav'))
        print(f"📊 Screenshots: {len(screenshots)}")
        print(f"📊 Audio clips: {len(audio_files)}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Record audio and screenshots")
    parser.add_argument("-d", "--duration", type=int, default=300,
                       help="Total duration in seconds")
    parser.add_argument("-s", "--screenshot-interval", type=int, default=30,
                       help="Seconds between screenshots")
    parser.add_argument("-a", "--audio-interval", type=int, default=20,
                       help="Average seconds between audio clips")
    parser.add_argument("--single", action="store_true",
                       help="Take a single screenshot")
    parser.add_argument("--audio-only", action="store_true",
                       help="Only record audio")
    
    args = parser.parse_args()
    
    if args.single:
        take_screenshot()
    elif args.audio_only:
        rec = Recorder(duration=60, screenshot_interval=9999)
        rec.record_audio()
    else:
        rec = Recorder(
            duration=args.duration,
            screenshot_interval=args.screenshot_interval,
            audio_interval=(15, args.audio_interval)
        )
        rec.run()

if __name__ == "__main__":
    main()