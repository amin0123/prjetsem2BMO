import sys

from langchain_community.llms import Ollama
import rclpy
from my_interfaces.msg import Text
from my_interfaces.srv import LlmInputOutput
from rclpy.node import Node
#from TTS.api import TTS
from gtts import gTTS
#huggingfacehub_api_token = '<HUGGING_FACE_TOKEN>'
#from TTS.api import TTS
from playsound import playsound
import cv2
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
status_file_path = "/home/amin/projetsem2_ws/src/llm_chat2/llm_chat2/status.txt"

global t
class LLmClientAsync(Node):

    def __init__(self):
        super().__init__('llm_client_async')
        self.cli = self.create_client(LlmInputOutput, 'llm_chat')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = LlmInputOutput.Request()
        with open(status_file_path, "w") as file:
            file.write("False")

    def send_request(self, input):
        self.req.input = input
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()
    





def main():
    rclpy.init()

    #img = cv2.imread("camera_Excited.png", cv2.IMREAD_ANYCOLOR)
    #cv2.imshow("camera_Excited", img)
    llm_client = LLmClientAsync()
    response = llm_client.send_request(sys.argv[1])
    llm_client.get_logger().info(
        'Response: for %s is : %s' %
        ((sys.argv[1]), response.output))
    tts = gTTS(response.output, lang="en")
    tts.save('output.mp3')
    with open(status_file_path, "w") as file:
        file.write("True")
    playsound('output.mp3')
    with open(status_file_path, "w") as file:
        file.write("False")
    print(status_file_path)
    #test.PlayVid = True
    t = True
    
    #command = f"ros2 run llm_chat2 client '{var}'"
    #os.system(command)
    llm_client.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()
    with open(status_file_path, "w") as file:
        file.write("False")