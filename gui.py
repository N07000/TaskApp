import subprocess
from nicegui import ui

ui.button(
    'NICHT DRUECKEN!',
    on_click=lambda: subprocess.run("shutdown /h", shell=True, capture_output=True, text=True))

ui.run()
