import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Números de pilotos a excluir
excluded_numbers = {'17', '50', '34', '37', '38', '45', '7', '72'}

url = "http://www.espn.com.pa/deporte-motor/pilotos/_/series/f1/formula-1"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'es-PA,es;q=0.9'
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Buscar filas de datos (excluyendo el encabezado)
    driver_rows = soup.find_all('tr', class_=lambda x: x and ('oddrow' in x or 'evenrow' in x))
    
    for row in driver_rows:
        try:
            # Extraer todas las celdas de la fila
            cells = row.find_all('td')
            
            # Verificar que haya suficientes celdas
            if len(cells) >= 2:  # Al menos nombre y número
                driver_number = cells[1].get_text(strip=True)  # Segunda columna es el número
                
                # Si el número está en la lista de excluidos, saltar este piloto
                if driver_number in excluded_numbers:
                    continue
                
                # Extraer nombre y URL
                link_tag = cells[0].find('a', href=True)
                if link_tag:
                    full_name = link_tag.get_text(strip=True)
                    driver_url = urljoin('http://www.espn.com.pa', link_tag['href'])
                    
                    # Extraer equipo (cuarta columna)
                    team = cells[3].get_text(strip=True) if len(cells) >= 4 else "Desconocido"
                    
                    print(f"Número: {driver_number}")
                    print(f"Nombre: {full_name}")
                    print(f"Equipo: {team}")
                    print(f"URL: {driver_url}")
                    print("-" * 50)
                
        except Exception as e:
            print(f"Error procesando fila: {e}")
            continue

except requests.exceptions.RequestException as e:
    print(f"Error al acceder a la página: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")