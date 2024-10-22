# main.py

from database import create_tables
from nicegui import ui

# Tabellen erstellen
create_tables()

# GUI starten
setup_gui()
