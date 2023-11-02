import os
import openai
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


def read_file(file_path: str) -> str:
    with open(file_path, "r") as f:
        return f.read()


def write_file(file_path: str, content: str) -> None:
    with open(file_path, "w") as f:
        f.write(content)


def main() -> None:
    content = read_file("websites/cuenta-ahorros.txt")

    messages = [
        {
            "role": "system",
            "content": "Eres un experto financiero",
        },
        {
            "role": "user",
            "content": f"Obtener TODA la información del producto financiero principal descrito "
            f"en el siguiente contenido: {content}.\nEstructurar la información en bullet points",
        },
    ]

    response = chat_completion(messages)
    write_file(
        "productos/cuenta-ahorro.txt", response["choices"][0]["message"]["content"]
    )


if __name__ == "__main__":
    main()
