from nicegui import ui
from database import load_user, save_user
from user import User

def setup_gui(user=None):
    """Setzt die Benutzeroberfläche basierend auf dem Benutzerstatus auf."""
    if user:
        # Wenn ein Benutzer vorhanden ist, Task-Manager anzeigen
        ui.label(f'Welcome {user.username}, Level {user.level}, Coins: {user.coins}').classes('text-2xl text-center')
        with ui.row().classes('justify-around'):
            ui.button('Add Task', on_click=lambda: ui.notify('Add Task clicked')).classes('bg-green-500 text-white px-4 py-2 rounded')
            ui.button('Show Tasks', on_click=lambda: ui.notify('Show Tasks clicked')).classes('bg-blue-500 text-white px-4 py-2 rounded')
    else:
        # Benutzererstellung anzeigen
        with ui.card().classes('w-full'):
            username_input = ui.input(label='Enter your Username')
            def create_user():
                username = username_input.value.strip()
                if username:
                    user = User(username=username)
                    save_user(user)
                    ui.notify(f'User {username} created!')
                    setup_gui(user)  # GUI neu laden mit dem neuen Benutzer
                else:
                    ui.notify('Please enter a valid username.', type='error')
            ui.button('Create User', on_click=create_user)

task_list_container = None  # Globaler Container für Aufgabenliste

def add_task():
    with ui.card().classes('w-full') as task_card:
        taskname = ui.input(label='Task Name')
        taskdesc = ui.textarea(label='Task Description')
        difficulty = ui.select(['easy', 'medium', 'hard'], label='Difficulty', value='medium')
        status = ui.select(['pending', 'completed'], label='Status', value='pending')
        priority = ui.select(['low', 'normal', 'high'], label='Priority', value='normal')
        finaldate = ui.date(label='Final Date')  # Datumsauswahl

        def save_task_data():
            if taskname.value.strip():  # Überprüfen, ob der Taskname gültig ist
                task = Task(
                    taskname=taskname.value,
                    taskdesc=taskdesc.value,
                    difficulty=difficulty.value,
                    status=status.value,
                    priority=priority.value,
                    finaldate=finaldate.value,
                )
                save_task(task)
                ui.notify(f'Task "{taskname.value}" added!')
                task_card.close()  # Schließt das Formular nach dem Speichern
                update_task_list()  # Aktualisiert die Aufgabenliste
            else:
                ui.notify('Please provide a valid task name.', type='error')

        ui.button('Save Task', on_click=save_task_data)

def update_task_list():
    """Aktualisiert die Aufgabenliste"""
    global task_list_container
    if task_list_container is not None:
        task_list_container.clear()  # Löscht den aktuellen Inhalt der Liste
        tasks = get_tasks()  # Ruft alle Aufgaben aus der Datenbank ab
        if not tasks:
            ui.label('No tasks available!', parent=task_list_container)
        else:
            for task in tasks:
                with task_list_container:  # Aufgaben in die Liste einfügen
                    ui.label(f'Task: {task[1]}, Description: {task[2]}, Due: {task[6]}, '
                             f'Priority: {task[5]}, Status: {task[4]}, Difficulty: {task[3]}')

def show_tasks():
    """Initialisiert den Aufgabencontainer"""
    global task_list_container
    with ui.card().classes('w-full'):
        task_list_container = ui.column()  # Spalte für Aufgabenliste
    update_task_list()  # Aktualisiert die Liste beim ersten Mal