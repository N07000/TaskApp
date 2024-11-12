# main.py

from database import create_tables
from gui import setup_gui

# Tabellen erstellen
create_tables()

# GUI starten
setup_gui()
