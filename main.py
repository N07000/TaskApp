from database import create_tables, load_user
from gui import setup_gui
from nicegui import ui

# Tabellen erstellen
create_tables()

# Benutzer laden
current_user = load_user()

# GUI basierend auf dem Benutzer starten
setup_gui(current_user)

ui.run()