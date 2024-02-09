import speech_recognition as sr
import threading
import time


class SpeechRecognizer:
    def __init__(self, callback=None):
        self.last_activity_time = time.time()
        self.is_pause = False
        self.callback = callback

    def recognize_audio(self, audio_chunk, results, lock):
        try:
            recognizer = sr.Recognizer()
            recognizer.operation_timeout = 5
            text = recognizer.recognize_google(audio_chunk, language="en-in")
            with lock:
                print(f"User Said: {text}")
                results.append(text)
                if self.callback:
                    self.callback(text)  # Notify the GUI with the recognized text
        except sr.UnknownValueError:
            pass  # Ignore if speech is not recognized
        except sr.RequestError as e:
            print(
                f"error: I'm sorry, I couldn't connect to the internet to process your request. Please check your network connection; {e}")
        except Exception as e:
            print(f"error: Oops! An unexpected error occurred. Please try again; {e}")

    def take_command(self):
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 700
        recognizer.pause_threshold = 2
        recognizer.phrase_threshold = 0.1
        recognizer.dynamic_energy_threshold = False
        recognizer.non_speaking_duration = 2
        with sr.Microphone() as source:
            silence_duration = 2  # adjust silence threshold as needed
            total_audio_duration = 0
            audio_chunks = []
            self.last_activity_time = time.time()
            self.is_pause = False
            results = []
            lock = threading.Lock()
            threads = []
            while True:
                # Adjust for ambient noise once per 5 seconds
                if time.time() - self.last_activity_time > 5:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    self.last_activity_time = time.time()

                start_time = time.time()  # Start the timer
                timeout = 2 if self.is_pause else 10

                try:
                    audio = recognizer.listen(source=source, timeout=timeout, phrase_time_limit=5)
                except sr.WaitTimeoutError:
                    # Timeout occurred, check if it's due to pause duration
                    if self.is_pause and time.time() - start_time > silence_duration:
                        break
                    continue

                duration = len(audio.frame_data) / (audio.sample_rate * audio.sample_width)  # Calculate audio duration
                total_audio_duration += duration
                audio_chunks.append(audio)

                # Check if the pause duration has been exceeded
                if time.time() - start_time > silence_duration:
                    self.is_pause = True

                thread = threading.Thread(target=self.recognize_audio, args=(audio, results, lock))
                thread.start()
                threads.append(thread)

                # Check for silence to initiate pause
                if time.time() - start_time < (silence_duration + 1):
                    break

        try:
            # Wait for all threads to finish
            for thread in threads:
                thread.join()

            # Combine all audio chunks into a single AudioData
            full_audio_data = b"".join([chunk.get_wav_data() for chunk in audio_chunks])
            full_audio = sr.AudioData(full_audio_data, source.SAMPLE_RATE, source.SAMPLE_WIDTH)

            return ' '.join(results).lower(), full_audio
        except Exception as e:
            return "", None