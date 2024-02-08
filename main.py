import speech_recognition as sr
import pyaudio
import time
import threading

last_activity_time = time.time()
standby_mode = False
is_pause = False


def recognize_audio(audio_chunk, results, lock):
    try:
        recognizer = sr.Recognizer()
        text = recognizer.recognize_google(audio_chunk, language="en-in")
        with lock:
            results.append(text)
    except sr.UnknownValueError:
        pass  # Ignore if speech is not recognized
    except sr.RequestError as e:
        print(f"error:I'm sorry, I couldn't connect to the internet to process your request. Please check your network connection; {e}")
    except Exception as e:
        print(f"error:Oops! An unexpected error occurred. Please try again; {e}")

def takeCommand():
    global last_activity_time, standby_mode, is_pause
    r = sr.Recognizer()
    r.energy_threshold = 700
    r.pause_threshold = 2
    r.phrase_threshold = 0.1
    r.dynamic_energy_threshold = False
    r.non_speaking_duration = 2
    with sr.Microphone() as source:
        print("Listening...")
        silence_duration = 4  # adjust silence threshold as needed
        total_audio_duration = 0
        audio_chunks = []
        last_activity_time = time.time()
        is_pause = False
        results = []
        lock = threading.Lock()
        threads = []
        while True:
            # Adjust for ambient noise once per 5 seconds
            if time.time() - last_activity_time > 5:
                r.adjust_for_ambient_noise(source, duration=0.5)
                last_activity_time = time.time()

            start_time = time.time()  # Start the timer
            timeout = 5 if is_pause else 10

            try:
                audio = r.listen(source=source, timeout=timeout, phrase_time_limit=5)
            except sr.WaitTimeoutError:
                # Timeout occurred, check if it's due to pause duration
                if is_pause and time.time() - start_time > silence_duration:
                    print("Pause WaitTimeout")
                    break
                continue

            duration = len(audio.frame_data) / (audio.sample_rate * audio.sample_width)  # Calculate audio duration
            total_audio_duration += duration
            audio_chunks.append(audio)

            # Check if the pause duration has been exceeded
            if time.time() - start_time > silence_duration:
                is_pause = True

            thread = threading.Thread(target=recognize_audio, args=(audio, results, lock))
            thread.start()
            threads.append(thread)

            # Check for silence to initiate pause
            if time.time() - start_time < (silence_duration + 1):
                print("silence to initiate pause")
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

def play_audio(audio_data):
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(audio_data.sample_width),
                    channels=1,
                    rate=audio_data.sample_rate,
                    output=True)

    stream.write(audio_data.get_wav_data())

    stream.stop_stream()
    stream.close()

    p.terminate()

if __name__ == "__main__":
    while True:
        command, full_audio = takeCommand()
        if "exit" in command:
            break
        print(command)
        if full_audio:
            play_audio(full_audio)
