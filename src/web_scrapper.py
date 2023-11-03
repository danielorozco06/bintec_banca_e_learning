import requests
import json
from bs4 import BeautifulSoup


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


def main() -> None:
    json_content = load_json("src/productos.json")

    for producto in json_content:
        for url in json_content[producto]:
            print(url)
            partes = url.split("/")
            nombre_producto = partes[-1]
            info = get_relevant_info(url)

            if info:
                save_to_file(f"websites/{producto}/{nombre_producto}.txt", info)
            else:
                print("No se pudo recuperar información relevante de la página.")


if __name__ == "__main__":
    main()
