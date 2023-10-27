import os
import gradio as gr
import openai, subprocess
import time
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_TOKEN")
if not api_key:
    raise ValueError("Missing OPENAI_TOKEN environment variable.")
openai.api_key = api_key

TRANSCRIPTION_MODEL = "whisper-1"
CHAT_MODEL = "gpt-3.5-turbo"
SPEAK_COMMAND = ["espeak-ng", "-ves-49"]


def chat_completion(messages):
    return openai.ChatCompletion.create(model=CHAT_MODEL, messages=messages)


def speak_message(message):
    subprocess.call(SPEAK_COMMAND + [message])


def transcribe_audio(audio) -> str:
    with open(audio, "rb") as audio_file:
        transcription = openai.Audio.transcribe(TRANSCRIPTION_MODEL, audio_file)
        return transcription["text"]


def request_ai(transcript: str, perfil: str, producto: str) -> str:
    messages = [
        {
            "role": "system",
            "content": "Eres un experto financiero, ayúdame a aclarar mis dudas.",
        },
        {
            "role": "user",
            "content": f"Responder brevemente la siguiente pregunta: ${transcript}. Tener en cuenta la siguiente informacion de la persona:${perfil}. Apoyarme en el siguiente contenido: ${producto}",
        },
    ]
    response = chat_completion(messages)
    system_message = response["choices"][0]["message"]["content"]
    speak_message(system_message)
    return system_message


def readFile(filename):
    with open(filename, "r") as f:
        return f.read()


def respond(query: str, chat_history: str):
    perfil = readFile("perfiles/daniel.txt")
    producto = readFile("productos/cuentas.txt")
    response = request_ai(query, perfil, producto)
    chat_history.append((query, response))
    time.sleep(2)
    return "", chat_history


with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    query = gr.Textbox()
    audio = gr.Audio(source="microphone", type="filepath")
    send = gr.Button("Submit")
    clear = gr.ClearButton()

    audio.stop_recording(transcribe_audio, audio, query)

    send.click(respond, [query, chatbot], [query, chatbot])
    chatbot.change(lambda: None, None, audio)
    chatbot.change(lambda: None, None, query)

    clear.click(lambda: None, None, audio)
    clear.click(lambda: None, None, query)

demo.launch()
