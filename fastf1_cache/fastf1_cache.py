import os
import fastf1
from pathlib import Path

# Ruta relativa al directorio de tu proyecto Django
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fastf1_cache')

# Crear la carpeta si no existe
os.makedirs(CACHE_DIR, exist_ok=True)

# Habilitar caché
fastf1.Cache.enable_cache(CACHE_DIR)

# Configuración automática multiplataforma
if os.name == 'nt':  # Windows
    cache_path = Path.home() / 'AppData' / 'Local' / 'fastf1' / 'cache'
else:  # Linux/macOS/otros
    cache_path = Path.home() / '.cache' / 'fastf1'

cache_path.mkdir(parents=True, exist_ok=True)
fastf1.Cache.enable_cache(cache_path)

print(f"✅ Caché de FastF1 configurado en: {cache_path}")