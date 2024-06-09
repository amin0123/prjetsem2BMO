import speech_recognition as sr
import os
import cv2
import webview
import asyncio
import concurrent.futures

def play_video(video_path):
    cap = cv2.VideoCapture(video_path)

    while(cap.isOpened()):
        ret, frame = cap.read()

        if ret:
            cv2.imshow('Video', frame)
            cv2.setWindowProperty('Video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

def recognize_speech():
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        try:
            var = r.recognize_google(audio)
            if var == "storytelling":
                asyncio.run(webview_async())
            else:
                command = f"ros2 run llm_chat2 client '{var}'"
                os.system(command)
            print("Recognized speech: " + var)
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Speech Recognition service; {0}".format(e))

async def webview_async():
    webview.create_window('Hello world', 'http://localhost:8501')
    webview.start()

async def main():
    video_path = "Helmet Eyes blink and wink - 3 min.mp4"

    with concurrent.futures.ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        video_task = loop.run_in_executor(executor, play_video, video_path)
        speech_task = loop.run_in_executor(executor, recognize_speech)
        await asyncio.gather(video_task, speech_task)

if __name__ == '__main__':
    # Start the event loop in a separate thread to avoid blocking the main thread
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
