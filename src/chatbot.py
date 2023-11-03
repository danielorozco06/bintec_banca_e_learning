"""
This module contains the implementation of a chatbot that interacts with users to answer financial questions.
"""

import os
import glob
import gradio as gr
import openai
import time
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()


def chat_completion(messages: str):
    """
    Sends a list of messages to the OpenAI API and returns the response.
    """
    openai.api_type = "azure"
    openai.api_base = "https://pocdevops-dev-oai-01.openai.azure.com"
    openai.api_version = "2023-05-15"
    openai.api_key = os.getenv("AZURE_OPENAI_TOKEN")

    return openai.ChatCompletion.create(
        engine="gpt-35-turbo",
        messages=messages,
        temperature=0,
        max_tokens=1000,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
    )


def speak_message(message: str) -> None:
    """
    Generates an audio file from the given message and plays it using the mpg123 player.
    """
    gTTS(text=message, lang="es", slow=False).save("audios/input.mp3")
    os.system("mpg123 audios/input.mp3 &")


def transcribe_audio(audio: str) -> str:
    """
    Transcribes the audio file at the given path using the OpenAI API and returns the resulting text.
    """
    with open(audio, "rb") as audio_file:
        openai.api_key = os.getenv("OPENAI_TOKEN")
        transcription = openai.Audio.transcribe("whisper-1", audio_file)
        return transcription["text"]


def request_ai(transcript: str, perfil: str, producto: str) -> str:
    """
    Sends a message to the OpenAI API to generate a response to the user's query.
    """
    messages = [
        {
            "role": "system",
            "content": "Eres un experto financiero, ayúdame a aclarar mis dudas.",
        },
        {
            "role": "user",
            "content": f"Responder brevemente la siguiente pregunta: {transcript}. "
            f"Tener en cuenta la siguiente información de la persona: {perfil}. "
            f"Apoyarme en el siguiente contenido: {producto}",
        },
    ]
    response = chat_completion(messages)
    system_message = response["choices"][0]["message"]["content"]
    return system_message


def read_file(filename: str) -> str:
    """
    Reads the contents of a file and returns it as a string.
    """
    with open(filename, "r") as f:
        return f.read()


def concatenate_files(dir_path: str) -> str:
    files = glob.glob(os.path.join(dir_path, "*"))
    content = ""
    for file in files:
        content += read_file(file)
    return content


def select_product(query: str) -> str:
    messages = [
        {
            "role": "system",
            "content": "Eres un experto financiero.",
        },
        {
            "role": "user",
            "content": f"Clasificar el siguiente texto en alguna de las siguientes opciones [cuentas, creditos, tarjetas]: {query}. Como ejemploe retornar en el siguient formato: cuentas",
        },
    ]
    response = chat_completion(messages)
    system_message = response["choices"][0]["message"]["content"]
    return system_message


def response(query: str, chat_history: str):
    """
    Sends the user's query to the OpenAI API and generates a response.
    The response is then spoken aloud and added to the chat history.
    """
    perfil = read_file("perfiles/daniel.txt")
    ruta_producto = select_product(query)

    contenido_productos = concatenate_files(f"productos/{ruta_producto}")
    response = request_ai(query, perfil, contenido_productos)
    speak_message(response)
    chat_history.append((query, response))
    time.sleep(2)
    return "", chat_history


def main() -> None:
    """
    Launches the Gradio demo for the virtual financial advisor chatbot.
    """
    with gr.Blocks() as demo:
        gr.Markdown("## Asesor financiero virtual")
        chatbot = gr.Chatbot()
        query = gr.Textbox(label="Escriba su consulta")
        audio = gr.Audio(
            source="microphone", type="filepath", label="Díganos su consulta"
        )
        send = gr.Button("Enviar")
        clear = gr.ClearButton(value="Limpiar")

        audio.stop_recording(transcribe_audio, audio, query)

        send.click(response, [query, chatbot], [query, chatbot])
        chatbot.change(lambda: None, None, audio)
        chatbot.change(lambda: None, None, query)

        clear.click(lambda: None, None, audio)
        clear.click(lambda: None, None, query)

    demo.launch()


if __name__ == "__main__":
    main()
