# gui.py

from nicegui import ui
from task import Task
from user import User
from database import save_task, get_tasks, save_user, load_user

current_user = None  # Variable, um den aktuellen Benutzer zu speichern

def create_user():
    global current_user
    with ui.card().classes('w-full') as user_card:
        username = ui.input(label='Enter your Username')

        def save_user_data():
            global current_user
            current_user = User(username.value)  # Neuen Benutzer erstellen
            save_user(current_user)  # Benutzer speichern
            ui.notify(f'User "{current_user.username}" created!')
            user_card.close()  # Schließt das Benutzererstellungsformular
            setup_task_manager()  # Startet die Task-Manager-Funktion
            
        ui.button('Create User', on_click=save_user_data)

def add_task():
    if not current_user:
        ui.notify('Please create a user first!')
        return
    
    with ui.card().classes('w-full') as task_card:
        taskname = ui.input(label='Task Name')
        taskdesc = ui.textarea(label='Task Description')
        difficulty = ui.select(['easy', 'medium', 'hard'], label='Difficulty', value='medium')
        status = ui.select(['pending', 'completed'], label='Status', value='pending')
        priority = ui.select(['low', 'normal', 'high'], label='Priority', value='normal')
        finaldate = ui.date(label='Final Date')  # Datumsauswahl

        def save_task_data():
            task = Task(taskname.value, taskdesc.value, difficulty.value, status.value, priority.value, finaldate.value)
            save_task(task)
            current_user.add_xp(task.get_xp_reward())  # XP für abgeschlossene Aufgaben vergeben
            save_user(current_user)  # Benutzer nach dem Hinzufügen von XP speichern
            ui.notify(f'Task "{taskname.value}" added! {task.get_xp_reward()} XP earned.')
            task_card.close()  # Schließt das Formular nach dem Speichern
            
        ui.button('Save Task', on_click=save_task_data)

def show_tasks():
    tasks = get_tasks()
    with ui.card().classes('w-full') as task_list_card:
        if not tasks:
            ui.label('No tasks available!')
        else:
            for task in tasks:
                ui.label(f'Task: {task[1]}, Description: {task[2]}, Due: {task[6]}, Priority: {task[5]}, Status: {task[4]}, Difficulty: {task[3]}')

def setup_task_manager():
    # Task Manager-Bereich nur nach Benutzereingabe anzeigen
    ui.label(f'Welcome {current_user.username}, Level {current_user.level}, XP: {current_user.xp}/{current_user.xp_until_next_level}, Coins: {current_user.coins}').classes('text-2xl text-center')

    with ui.row().classes('justify-around'):
        ui.button('Add Task', on_click=add_task).classes('bg-green-500 text-white px-4 py-2 rounded')
        ui.button('Show Tasks', on_click=show_tasks).classes('bg-blue-500 text-white px-4 py-2 rounded')

# Benutzeroberfläche aufbauen
def setup_gui():
    global current_user
    current_user = load_user()  # Benutzer aus der Datenbank laden, falls vorhanden
    
    if not current_user:
        with ui.card().classes('w-full bg-gray-200 p-4'):
            ui.label('Welcome to ToDoRPG').classes('text-4xl text-center mb-4')
            ui.label('Please create a user to get started').classes('text-center')
            create_user()  # Benutzererstellungsformular anzeigen
    else:
        setup_task_manager()  # Falls Benutzer existiert, direkt den Task-Manager anzeigen

    ui.run()
