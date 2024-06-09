import speech_recognition as sr
import os
import cv2
import webview
import asyncio
import concurrent.futures
import threading
import time
# Global variable to track if video is playing
video_playing = True
webview_running = threading.Event()

def destroy(window):
    # show the window for a few seconds before destroying it:

    time.sleep(5)
    print('Destroying window..')
    window.destroy()
    print('Destroyed!')


def play_video(video_path):
    global video_playing, webview_running
    cap = cv2.VideoCapture(video_path)

    while(cap.isOpened()):
        ret, frame = cap.read()

        if ret:
            cv2.imshow('Video', frame)
            cv2.setWindowProperty('Video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            if not video_playing:
                break  # Stop video if webview is running
        else:
            break

    cap.release()
    cv2.destroyAllWindows()
    video_playing = False

def recognize_speech():
    global video_playing, webview_running
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        try:
            var = r.recognize_google(audio)
            if var == "storytelling":
                if video_playing:
                    # Close the video window if playing
                    cv2.destroyAllWindows()
                    video_playing = False
                if not webview_running.is_set():
                    # Start webview if not already running
                    asyncio.run_coroutine_threadsafe(webview_async(), loop=loop)  # Run webview in the main thread
            else:
                command = f"ros2 run llm_chat2 client '{var}'"
                os.system(command)
                if not video_playing:
                    # Start video playback if not already playing
                    video_playing = True
                    play_video("Helmet Eyes blink and wink - 3 min.mp4")
            print("Recognized speech: " + var)
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Speech Recognition service; {0}".format(e))

def start_webview():
    print("Starting webview...")
    webview.create_window('Hello world', 'http://localhost:8501')
    webview.start()

async def webview_async():
    global webview_running
    cv2.destroyAllWindows()
    webview_running.set()  # Set the webview running flag
    window = webview.create_window('Hello world', 'http://localhost:8501')
    webview.start(destroy, window)
    time.sleep(2)
    on_closing()
    #await loop.run_in_executor(None, start_webview)  # Execute start_webview() on the main thread
    print("Waiting for webview window to be closed manually...")
    webview_running.clear()  # Clear the webview running flag

def on_closing():
    print("Webview window closed")
    global video_playing
    if not video_playing:
        # Start video playback if not already playing
        video_playing = True
        play_video("Helmet Eyes blink and wink - 3 min.mp4")

async def main():
    global video_playing
    video_path = "Helmet Eyes blink and wink - 3 min.mp4"

    with concurrent.futures.ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        video_task = loop.run_in_executor(executor, play_video, video_path)
        speech_task = loop.run_in_executor(executor, recognize_speech)
        await asyncio.gather(video_task, speech_task)

if __name__ == '__main__':
    print("Starting main loop...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
