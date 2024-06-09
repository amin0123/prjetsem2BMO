from example_interfaces.srv import AddTwoInts
from langchain_community.llms import Ollama
import rclpy
from my_interfaces.msg import Text
from my_interfaces.srv import LlmInputOutput
from rclpy.node import Node
from langchain_community.llms import HuggingFaceHub
from gtts import gTTS
from langchain.memory import ChatMessageHistory
from langchain.prompts import PromptTemplate
#huggingfacehub_api_token = '<HUGGING_FACE_TOKEN>'
#from TTS.api import TTS
from playsound import playsound
#from pathlib import Path

#current_working_directory = Path.cwd()
#tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)
#llm = HuggingFaceHub(repo_id='tiiuae/falcon-7b-instruct', huggingfacehub_api_token=huggingfacehub_api_token)





class LLmService(Node):

    def __init__(self):
        super().__init__('llm_service')
        self.srv = self.create_service(LlmInputOutput, 'llm_chat', self.llm_chat_callback)
        #self.model = Ollama(model="llama3")
        #self.history = ChatMessageHistory()
        #self.history.add_ai_message("hi ! ask me anything")
        #self.prompt_template = PromptTemplate.from_template(
        #    """             
        #<s> [INST] You are a knowledgeable and friendly guide[/INST] </s>
            
        #    [INST] You: {user_input} </s>
        #    Assistant: 
        #    """
        #)        
        #self.chain = (self.prompt_template | self.model)
    
    def llm_chat_callback(self, request, response):
        llm = Ollama(model="llama3")
        user_input = request.input
        response.output = llm.invoke(user_input)
        #Settings.llm = Ollama(model="llama3", request_timeout=100.0, additional_kwargs={"num_predict": 10})
        #self.history.add_user_message(user_input)
        #response.output = self.chain.invoke({
        #    "user_input": self.history.messages,
        #})
        #self.history.add_ai_message(response)

        #tts = gTTS(response.output, lang="en")
        #tts.save('output.mp3')
        #tts.tts_to_file(text=response.output,
        #        file_path="output.wav",
        #        speaker_wav=str(current_working_directory)+"/speaker.wav",
        #        language="en")
        #response.output = query
        #playsound('output.mp3')
        #response.output
        self.get_logger().info('Incoming request\n: %s' % (request.input))

        return response


def main():
    rclpy.init()

    llm_service = LLmService()

    rclpy.spin(llm_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()