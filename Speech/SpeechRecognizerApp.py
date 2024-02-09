import tkinter as tk
from tkinter import messagebox
import pyaudio
import threading

from Speech.SpeechRecognizer import SpeechRecognizer


class SpeechRecognizerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Speech Recognizer App")
        self.master.geometry("400x500")

        self.recognizer = SpeechRecognizer(callback=self.update_recognized_text)

        self.create_widgets()

        self.chat_history = []
        self.listen_thread = None  # Initialize listen_thread attribute
        self.is_listening = False  # Flag to control the listening loop

    def update_recognized_text(self, text):
        self.recognized_text_label.config(text=f"Recognized Text: {text}")

    def create_widgets(self):
        self.label = tk.Label(self.master, text="Click 'Start Listening' to begin.")
        self.label.pack()

        self.chat_history_text = tk.Text(self.master, height=15, width=50)
        self.chat_history_text.pack()

        self.recognized_text_label = tk.Label(self.master, text="", wraplength=350)
        self.recognized_text_label.pack()

        self.start_button = tk.Button(self.master, text="Start Listening", command=self.start_listening)
        self.start_button.pack()

        self.stop_button = tk.Button(self.master, text="Stop Listening", command=self.stop_listening, state=tk.DISABLED)
        self.stop_button.pack()

    def start_listening(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.is_listening = True
        # Create a thread to handle listening to speech input
        self.listen_thread = threading.Thread(target=self.listen_and_recognize)
        self.listen_thread.start()

    def listen_and_recognize(self):
        while self.is_listening:
            command, full_audio = self.recognizer.take_command()
            if "exit" in command:
                break
            print(command)
            self.update_chat_history_text(command)
            if full_audio:
                self.play_audio(full_audio)

        # After listening loop ends, update GUI to reflect state
        self.master.after(0, self.update_after_listen_thread_ends)

    def update_chat_history_text(self, text):
        self.chat_history.append(text)
        self.update_chat_history()

    def update_chat_history(self):
        self.chat_history_text.delete(1.0, tk.END)
        for message in self.chat_history:
            self.chat_history_text.insert(tk.END, f"{message}\n")
        self.chat_history_text.see(tk.END)

    def update_after_listen_thread_ends(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def stop_listening(self):
        messagebox.showinfo("Info", "Listening stopped.")
        self.is_listening = False
        if self.listen_thread and self.listen_thread.is_alive():
            self.listen_thread.join()  # Wait for the listening thread to finish
        self.master.quit()

    def play_audio(self, audio_data):
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(audio_data.sample_width),
                        channels=1,
                        rate=audio_data.sample_rate,
                        output=True)

        stream.write(audio_data.get_wav_data())

        stream.stop_stream()
        stream.close()

        p.terminate()