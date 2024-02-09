import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pyaudio
import threading
import time

from Speech.SpeechRecognizerApp import SpeechRecognizerApp


def main():
    root = tk.Tk()
    app = SpeechRecognizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
