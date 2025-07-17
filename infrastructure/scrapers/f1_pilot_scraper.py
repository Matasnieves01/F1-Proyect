import requests
from bs4 import BeautifulSoup

def scrape_driver_details(driver_url):
    try:
        # Extraer nombre del slug de la URL
        name_from_url = driver_url.rstrip('/').split('/')[-1]  # ej: "oscar-piastri"
        nombre = ' '.join([part.capitalize() for part in name_from_url.split('-')])

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(driver_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Nacionalidad
        nacionalidad_tag = soup.select_one('.f1-race-driver-nationality') or soup.select_one('.driver-nationality')
        pais = nacionalidad_tag.get_text(strip=True) if nacionalidad_tag else "Desconocido"

        # Número del piloto
        numero_tag = soup.select_one('.f1-race-driver-number') or soup.select_one('.driver-number')
        numero = numero_tag.get_text(strip=True) if numero_tag else "N/A"

        # Escudería
        escuderia_tag = soup.select_one('.f1-race-driver-team') or soup.select_one('.driver-team')
        escuderia = escuderia_tag.get_text(strip=True) if escuderia_tag else "Desconocida"

        # Extraer datos de la cuadrícula (Season Positions y Season Points)
        season_positions = "N/A"
        season_points = "0"
        
        # Buscar todos los ítems de la cuadrícula de datos
        items = soup.find_all('div', class_='DataGrid-module_item_cs92d')
        
        for item in items:
            title = item.find('dt', class_='DataGrid-module_title_hXM-n')
            value = item.find('dd', class_='DataGrid-module_description_e-Mnw')
            
            if title and value:
                title_text = title.get_text(strip=True)
                value_text = value.get_text(strip=True)
                
                if "Season Positions" in title_text:
                    season_positions = value_text
                elif "Season Points" in title_text:
                    season_points = value_text

        # Campeonatos ganados
        campeonatos = 0
        campeonatos_tag = soup.find(text=lambda t: t and ("championship" in t.lower() or "world titles" in t.lower()))
        if campeonatos_tag:
            parent = campeonatos_tag.find_parent()
            if parent:
                numero_tag = parent.find_next('span')
                if numero_tag and numero_tag.get_text(strip=True).isdigit():
                    campeonatos = int(numero_tag.get_text(strip=True))

        return {
            'nombre': nombre,
            'pais': pais,
            'numero': numero,
            'escuderia': escuderia,
            'puntos': season_points,  # Usamos los puntos de la cuadrícula
            'posicion': season_positions,  # Nueva clave para la posición
            'titulos': campeonatos
        }

    except Exception as e:
        print(f"Error al extraer detalles de {driver_url}: {e}")
        return {}
    
driver_url = "https://www.formula1.com/en/drivers/oscar-piastri.html"
detalles = scrape_driver_details(driver_url)
print(detalles)