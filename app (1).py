#!/bin/env python3
import os
import tempfile
import streamlit as st
from streamlit_chat import message
from rag import ChatPDF
from gtts import gTTS
from playsound import playsound
import openpyxl
from openpyxl import Workbook
from datetime import datetime
import pyttsx3
import threading
import speech_recognition as sr

st.set_page_config(page_title="ChatPDF")


def open_pdf(pdf_path):
    os.system(f'start {pdf_path}')


def save_to_excel(input_text, output_text):
    try:
        wb = openpyxl.load_workbook("chat_logs.xlsx")
        sheet = wb.active
    except FileNotFoundError:
        wb = Workbook()
        sheet = wb.active
        sheet.append(["Input", "Output", "Timestamp"])

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append([input_text, output_text, timestamp])

    wb.save("Conversation.xlsx")


def display_messages():
    st.subheader("Chat")
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))
    st.session_state["thinking_spinner"] = st.empty()

    # Save input and output to Excel file
    if len(st.session_state["messages"]) >= 2:
        input_text = st.session_state["messages"][-2][0]
        output_text = st.session_state["messages"][-1][0]

        # Generate unique filename for each output message
        filename = f"output_{len(st.session_state['messages']) // 2}.mp3"

        save_to_excel(input_text, output_text)

        # Remove the previous MP3 file, if it exists
        if os.path.exists(filename):
            os.remove(filename)

        tts = gTTS(output_text, lang="en")
        tts.save(filename)
        playsound(filename)


def process_input():
    if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        user_text = st.session_state["user_input"].strip()
        with st.session_state["thinking_spinner"], st.spinner(f"Thinking"):
            agent_text = st.session_state["assistant"].ask(user_text)

        st.session_state["messages"].append((user_text, True))
        st.session_state["messages"].append((agent_text, False))
    else:
        # If the user hasn't entered text, listen for speech input and convert it to text
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("Listening...")
            recognizer.adjust_for_ambient_noise(source)  # Adjust microphone for ambient noise
            audio = recognizer.listen(source)

        try:
            user_text = recognizer.recognize_google(audio)  # Convert speech to text using Google Speech Recognition
            st.session_state["user_input"] = user_text  # Set the recognized text as the user input
            process_input()  # Process the recognized text
        except sr.UnknownValueError:
            st.write("Sorry, I couldn't understand what you said.")
        except sr.RequestError:
            st.write("Sorry, there was an error with the speech recognition service.")


def read_and_save_file():
    st.session_state["assistant"].clear()
    st.session_state["messages"] = []
    st.session_state["user_input"] = ""

    for file in st.session_state["file_uploader"]:
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(file.getbuffer())
            file_path = tf.name

        with st.session_state["ingestion_spinner"], st.spinner(f"Ingesting {file.name}"):
            st.session_state["assistant"].ingest(file_path)
        os.remove(file_path)


def page():
    if len(st.session_state) == 0:
        st.session_state["messages"] = []
        st.session_state["assistant"] = ChatPDF()

    st.header("Autism ChatBot")

    file_path = "AutismData.pdf"
    pdf_file_path = "Lettre.pdf"

    if st.button("Generate Report"):
        open_pdf(pdf_file_path)
    if st.button("Open Microphone"):
        process_input()

    st.session_state["ingestion_spinner"] = st.empty()

    display_messages()  # Call display_messages without passing any arguments

    st.text_input("Message", key="user_input", on_change=process_input)

    if file_path:
        st.session_state["assistant"].ingest(file_path)


if __name__ == "__main__":
    page()
