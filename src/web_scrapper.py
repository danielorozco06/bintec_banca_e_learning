import requests
import json
import os
import openai
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


def get_relevant_info(url: str):
    # Headers para simular una petición de navegador web
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    # Uso de una sesión para mantener la conexión abierta
    with requests.Session() as session:
        try:
            response = session.get(url, headers=headers)

            # Lanzará un error si la solicitud no fue exitosa
            response.raise_for_status()

            # Parsear el HTML con BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")

            # Encuentra elementos relevantes, como títulos y párrafos
            titles = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

            # Aquí podrías ser más específico
            relevant_paragraphs = soup.find_all("p")

            # Extracción de texto
            extracted_text = "\n".join(title.get_text(strip=True) for title in titles)
            extracted_text += "\n".join(
                p.get_text(strip=True) for p in relevant_paragraphs
            )

            return extracted_text

        except requests.RequestException as e:
            print(f"Error al recuperar la página web: {e}")


def save_to_file(file_name: str, data: str) -> None:
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(data)


def load_json(file_name: str) -> dict:
    with open(file_name, "r", encoding="utf-8") as file:
        return json.load(file)


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


def structure(file_name: str) -> None:
    content = read_file(file_name)

    messages = [
        {
            "role": "system",
            "content": "Eres un experto financiero",
        },
        {
            "role": "user",
            "content": f"Obtener TODA la información del producto financiero principal descrito "
            f"en el siguiente contenido: {file_name} {content}.\nEstructurar la información en bullet points",
        },
    ]

    response = chat_completion(messages)
    output_file = file_name.replace("websites", "productos")
    write_file(output_file, response["choices"][0]["message"]["content"])


def main() -> None:
    json_content = load_json("src/productos.json")

    for producto in json_content:
        for url in json_content[producto]:
            print(url)
            partes = url.split("/")
            nombre_producto = partes[-1]
            info = get_relevant_info(url)

            if info:
                file_name = f"websites/{producto}/{nombre_producto}.txt"
                save_to_file(file_name, info)
                structure(file_name)

            else:
                print("No se pudo recuperar información relevante de la página.")


if __name__ == "__main__":
    main()
