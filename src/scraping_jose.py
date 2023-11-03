import requests
from bs4 import BeautifulSoup

url = 'https://www.bancolombia.com/personas/solicitud-de-productos/tarjeta-mastercard-e-card'
response = requests.get(url)

if response.status_code == 200:
    # La solicitud fue exitosa
    page_content = response.content
else:
    # Maneja el error de alguna manera
    print('Error al cargar la página:', response.status_code)



soup = BeautifulSoup(page_content, 'html.parser')

links = soup.find_all('a')

for link in links:
    print(link.get('href'))
