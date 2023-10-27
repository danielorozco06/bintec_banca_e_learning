"""
Main file for the project
"""
import os
import gradio as gr
import openai, subprocess
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_TOKEN")
SYSTEM_MESSAGE_CONTENT = "Eres experto financiero, ayudame a aclarar mis dudas."
TRANSCRIPTION_MODEL = "whisper-1"
CHAT_MODEL = "gpt-3.5-turbo"
SPEAK_COMMAND = ["espeak-ng", "-ves-49"]


def create_chat_transcript(messages):
    return "\n\n".join(
        [
            f"{message['role']}: {message['content']}"
            for message in messages
            if message["role"] != "system"
        ]
    )


def transcribe_audio(audio):
    with open(audio, "rb") as audio_file:
        return openai.Audio.transcribe(TRANSCRIPTION_MODEL, audio_file)


def chat_completion(messages):
    return openai.ChatCompletion.create(model=CHAT_MODEL, messages=messages)


def speak_message(message):
    subprocess.call(SPEAK_COMMAND + [message])


def transcribe(audio):
    messages = [{"role": "system", "content": SYSTEM_MESSAGE_CONTENT}]

    transcript = transcribe_audio(audio)
    messages.append({"role": "user", "content": transcript["text"]})

    response = chat_completion(messages)
    system_message = response["choices"][0]["message"]
    messages.append(system_message)

    speak_message(system_message["content"])

    return create_chat_transcript(messages)


def main() -> None:
    """
    Main function
    """

    ui = gr.Interface(
        fn=transcribe,
        inputs=gr.components.Audio(source="microphone", type="filepath"),
        outputs="text",
    )
    ui.launch()


if __name__ == "__main__":
    main()
