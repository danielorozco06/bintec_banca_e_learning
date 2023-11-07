import requests
from bs4 import BeautifulSoup
import unicodedata
# url = 'https://www.bancolombia.com/personas/solicitud-de-productos/tarjeta-mastercard-e-card'
# response = requests.get(url)

# if response.status_code == 200:
#     # La solicitud fue exitosa
#     page_content = response.content
# else:
#     # Maneja el error de alguna manera
#     print('Error al cargar la página:', response.status_code)



# soup = BeautifulSoup(page_content, 'html.parser')

# links = soup.find_all('a')

# for link in links:
#     print(link.get('href'))

def save_data(r1):
    with open(f"./OUTPUT.txt", "w") as file:
        file.write(r1)
    return "Data saved successfully."



def eliminar_diacriticos(texto):
    texto_normalizado = unicodedata.normalize('NFD', texto)
    texto_sin_diacriticos = ''.join([caracter for caracter in texto_normalizado if not unicodedata.combining(caracter)])
    return texto_sin_diacriticos

def modificar_cadena(texto):
    # Reemplaza dos tabulaciones por una sola.
    texto = texto.replace('            ', '')
    texto = texto.replace('    ', '')
    # Agrega un salto de línea después de cada punto.
    #texto = texto.replace('.', '.\n')

    return texto


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
            relevant_paragraphs = soup.find_all("html")

            # Extracción de texto
            extracted_text = "\n".join(title.get_text(strip=True) for title in titles)
            extracted_text += "\n".join(
                p.get_text(strip=True) for p in relevant_paragraphs
            )
            texto_limpio = eliminar_diacriticos(extracted_text)
            texto_modificado = modificar_cadena(texto_limpio)
            save_data(texto_modificado)
            return texto_modificado
        except requests.RequestException as e:
            print(f"Error al recuperar la página web: {e}")


get_relevant_info('https://www.bancolombia.com/personas/tarjetas-de-credito/mastercard/black')