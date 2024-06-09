import cv2
import os

from mutagen.mp3 import MP3
import time





def check_status_file():
    status_file_path = os.path.join(script_dir, "status.txt")
    if os.path.exists(status_file_path):
        with open(status_file_path, "r") as file:
            status = file.read().strip()
            return status == "True"
    return False


def get_mp3_length(file_path):
    try:
        audio = MP3(file_path)
        return audio.info.length
    except Exception as e:
        print("Error:", e)
        return None

script_dir = os.path.dirname(os.path.abspath(__file__))

# Video file name
video_file = "BMO.mp4"

# Path to the video file
video_path = os.path.join(script_dir, video_file)
img_path = os.path.join(script_dir, "image2.jpg")

cap = cv2.VideoCapture(video_path)

end_image = cv2.imread(img_path)  # Load the end image outside the loop``
PlayVid=False

while True:
    PlayVid=check_status_file()
    print(PlayVid)
    while cap.isOpened() and PlayVid==True:
        #l = get_mp3_length('output.mp3')
        #print("Vid")
        ret, frame = cap.read()
        if not ret:
            # Video is over, break the inner loop
            break
        frame = cv2.resize(frame, (800, 480))
        cv2.imshow("video", frame)
        key = cv2.waitKey(10)
        if key & 0xFF == ord('q'):
            PlayVid=False
            break
      # Display the end image
    # Wait for either 5 seconds or for Enter key press
    #print("IMG")
    cv2.imshow("video", end_image)
    key = cv2.waitKeyEx(100)
    #print("Over")
    if key & 0xFF == ord('p'):
        PlayVid=True
    # Reset video capture to play the video from the beginning
    #If i click button here do this : 
    #cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

#cv2.destroyAllWindows()
#cap.release()