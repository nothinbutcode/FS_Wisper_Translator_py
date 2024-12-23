import numpy as np
import sounddevice as sd
from pynput import keyboard
from faster_whisper import WhisperModel
import tempfile
from scipy.io.wavfile import write
import os
from deep_translator import GoogleTranslator
import subprocess

class FasterWhisperTranscriber:
    def __init__(self, model_size="large-v3", samplerate=16000, stero_or_audio=1):
        self.model_size = model_size
        self.sample_rate = samplerate
        self.model = WhisperModel(model_size, device="cuda", compute_type="int8")
        self.is_recording = True
        self.detected_language = None
        self.target_language = 'en'
        self.stero_or_audio = stero_or_audio
        self.recording = np.array([], dtype="float64").reshape(0, self.stero_or_audio)
        self.transcription_file = "transcription.txt"  # File to store transcription
    
    def on_press(self, key):
        if key == keyboard.Key.space:
            if not self.is_recording:
                self.is_recording = True
                print("Recording started...")

    def on_release(self, key):
        if key == keyboard.Key.space:
            if self.is_recording:
                self.is_recording = False
                print("Stopped recording.")
                return False
    
    def record_audio_chunk(self):
        frames_per_buffer = self.sample_rate * 4
        chunk = sd.rec(frames_per_buffer, samplerate=self.sample_rate, channels=self.stero_or_audio, dtype="float64")
        sd.wait()
        return chunk
    
    def save_temp_audio(self, recording):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                temp_filename = temp_file.name
                write(temp_filename, self.sample_rate, recording)
                #print(f"Temporary WAV file saved: {temp_filename}")
                return temp_filename
        except Exception as e:
            print(f"Error saving temporary audio file: {e}")
            return None
    
    def transcribe_audio(self, file_path):
        try:
            segments, info = self.model.transcribe(file_path, beam_size=5)
            self.detected_language = info.language
            full_transcription = ""
            for segment in segments:
                print(segment.text)
                full_transcription += segment.text + " "
            return full_transcription.strip()
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return None
        finally:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
                print(f"Temporary file removed: {file_path}")
    
    def write_transcription_to_file(self, transcription):
        try:
            with open(self.transcription_file, "a") as f:
                f.write(transcription + "\n")
            print(f"Transcription written to {self.transcription_file}")
        except Exception as e:
            print(f"Error writing transcription to file: {e}")
    
    def translate_text(self):
        try:
            while True:
                if os.path.exists(self.transcription_file):
                    with open(self.transcription_file, "r") as f:
                        lines = f.readlines()
                    if lines:
                        text_to_translate = lines[-1].strip()  # Get the latest line
                        if text_to_translate:
                            translator = GoogleTranslator(source=self.detected_language, target=self.target_language)
                            translated_text = translator.translate(text=text_to_translate)
                            print(f"Translated text: {translated_text}")
        except Exception as e:
            print(f"Translation error: {e}")
    
    def run(self):
        print("Hold spacebar to record")
        accumulated_transcription = ""
        # Start translation process in a separate terminal
        subprocess.Popen(['gnome-terminal', '--', 'python3', '-c', 'from this_script import FasterWhisperTranscriber; FasterWhisperTranscriber().translate_text()'])
        
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            while True:
                try:
                    if self.is_recording:
                        chunk = self.record_audio_chunk()
                        self.recording = np.vstack([self.recording, chunk])
                        file_path = self.save_temp_audio(self.recording)
                        if file_path:
                            transcription = self.transcribe_audio(file_path)
                            if transcription:
                                accumulated_transcription += " " + transcription
                                print(f"Accumulated Transcription: {accumulated_transcription}")
                                self.write_transcription_to_file(accumulated_transcription)
                    if not listener.running:
                        break
                except KeyboardInterrupt:
                    print("\nExiting...")
                    break
                except Exception as e:
                    print(f"Error: {e}")
                    continue

if __name__ == "__main__":
    transcriber = FasterWhisperTranscriber()
    transcriber.run()
