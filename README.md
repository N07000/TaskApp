# 📋🎮 TaskApp 

Die **TaskApp** ist eine Python-basierte Anwendung, die Aufgabenverwaltung mit RPG-Elementen (Role-Playing Game) kombiniert. Benutzer können Quests (Aufgaben) erstellen und durch deren Abschluss Erfahrungspunkte (XP) sammeln, um Level aufzusteigen. 🏆

## 🛠️ Verwendete Technologien 

- **Python** als Hauptprogrammiersprache
- **NiceGui** für die Benutzeroberfläche
- **SQLite** für die Datenpersistenz
- **Pillow (PIL)** für Bildverarbeitung

## ⚙️ Systemanforderungen 

- **Python 3.x**
- **NiceGui Framework**
- **SQLite3**
- **Pillow Library**

## 🏗️ Systemarchitektur 

- **main.py**: Hauptanwendung und Startpunkt
- **gui.py**: Benutzeroberfläche und UI-Logik
- **database.py**: Datenbankoperationen
- **user.py**: Benutzerklasse und -verwaltung
- **task.py**: Quest-/Aufgabenklasse und -verwaltung
- **profile_images/**: Verzeichnis für Benutzerprofilbilder

## ✨ Funktionalitäten

### Kernfunktionen

1. **Benutzerverwaltung**
   - Erstellung eines Charakters mit Name, Klasse und Rasse
   - Level-System mit XP-Progression
   - Profilbild-Verwaltung (ab Level 5)
   - Dark/Light Mode (ab Level 2)

2. **Quest-System**
   - Erstellen neuer Quests mit Namen, Beschreibung und Schwierigkeitsgrad
   - Statusverwaltung (Nicht begonnen, In Bearbeitung, Warten, Abgeschlossen)
   - XP-Belohnungen basierend auf Schwierigkeitsgrad:
     - Leicht: 50 XP
     - Mittel: 100 XP
     - Schwer: 150 XP

3. **Benutzeroberfläche**
   - Responsive Design
   - Status-Farbkodierung
   - Fortschrittsanzeige für Level
   - Separate Ansichten für aktive und abgeschlossene Quests
