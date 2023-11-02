import requests
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
            titles = soup.find_all(["h1", "h2", "h3", "h4"])

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


# URL de la página que deseamos raspar
url = "https://www.bancolombia.com/personas/cuentas/ahorros-y-corriente/cuenta-ahorros"

# Dividimos el string por el delimitador '/'
partes = url.split("/")
# Obtenemos el último elemento de la lista resultante
nombre_producto = partes[-1]

# Extraer la información relevante
info = get_relevant_info(url)

if info:
    print(info)

    # Guardar la información en un archivo
    save_to_file(f"websites/{nombre_producto}.txt", info)
else:
    print("No se pudo recuperar información relevante de la página.")
