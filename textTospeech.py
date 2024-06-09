import speech_recognition as sr
import os
import webview
# obtain audio from the microphone
r = sr.Recognizer()
var1 = "ros2 run llm_chat2 client"

#command2 = "python3 src/llm2_chat2/llm2_chat/test.py"
#os.system(command2)
#print("".join([var1, r.recognize_google(audio)]))
while True:
    
    with sr.Microphone() as source:
        print("Say something!")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

# recognize speech using Sphinx
    try:
        var= r.recognize_google(audio)
    #os.system("".join([var1, str(r.recognize_google(audio))]))
    #os.system("ros2 run llm_chat2 client 'hello'")
        if var == "tell me a story":
            webview.create_window('Hello world', 'https://pywebview.flowrl.com/hello')
            webview.start()
        
        
        command = f"ros2 run llm_chat2 client '{var}'"
        os.system(command)
    #!ros2 run llm_chat2 client 'hello'
    #print("Sphinx thinks you said " + r.recognize_sphinx(audio))
        print("Sphinx thinks you said " + r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))