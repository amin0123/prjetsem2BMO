#!/bin/env python3
import os
import tempfile
import streamlit as st
from streamlit_chat import message
from rag import ChatPDF
from gtts import gTTS
from playsound import playsound
st.set_page_config(page_title="ChatPDF")


import openpyxl
from openpyxl import Workbook
from datetime import datetime
import pyttsx3
import threading


def open_pdf(pdf_path):
    os.system(f'start {pdf_path}')
    #webbrowser.open_new_tab(pdf_path)


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
    if len(st.session_state["messages"]) >= 2:  # Assuming messages are always in pairs (user input and bot response)
        input_text = st.session_state["messages"][-2][0]
        output_text = st.session_state["messages"][-1][0]
        save_to_excel(input_text, output_text)

    tts = gTTS(st.session_state["messages"][-1][0], lang="en")
    tts.save('output.mp3')
    playsound('output.mp3')


def process_input():
    if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        user_text = st.session_state["user_input"].strip()
        with st.session_state["thinking_spinner"], st.spinner(f"Thinking"):
            agent_text = st.session_state["assistant"].ask(user_text)

        st.session_state["messages"].append((user_text, True))
        st.session_state["messages"].append((agent_text, False))


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

    st.session_state["ingestion_spinner"] = st.empty()

    display_messages()  # Call display_messages without passing any arguments
    st.text_input("Message", key="user_input", on_change=process_input)

    if file_path:
        st.session_state["assistant"].ingest(file_path)





if __name__ == "__main__":
    page()
