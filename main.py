# main.py

from database import create_tables
from gui import setup_gui
# Tabellen erstellen
create_tables()

# GUI starten
# main.py

from database import create_tables, load_user, save_user
from gui import setup_gui
from nicegui import ui
from user import User

# Tabellen erstellen
create_tables()

# Benutzer laden
current_user = load_user()

# GUI mit oder ohne Benutzer starten
setup_gui(current_user)

if __name__ == '__main__':
    main()