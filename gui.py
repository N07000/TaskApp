# gui.py

from nicegui import ui
from task import Task
from user import User
from database import save_task, get_tasks, save_user, load_user

def create_user():
    ui.card().classes('w-full')
    username = ui.input(label='Enter your Username')
    global Username
    ui.notify(f'User "{User.username}" created!')
    setup_task_manager()
    ui.button('Create User', on_click=save_user(username))

def add_task():
    # Task-Formular als Card erstellen
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
            ui.notify(f'Task "{taskname.value}" added!')
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
    # Task Manager mit User-Daten anzeigen
    ui.label(f'Welcome {User.username}, Level {User.level}, Coins: {User.coins}').classes('text-2xl text-center')

    with ui.row().classes('justify-around'):
        ui.button('Add Task', on_click=add_task).classes('bg-green-500 text-white px-4 py-2 rounded')
        ui.button('Show Tasks', on_click=show_tasks).classes('bg-blue-500 text-white px-4 py-2 rounded')

# Benutzeroberfläche aufbauen
def setup_gui():
    with ui.card().classes('w-full bg-gray-200 p-4'):
        ui.label('Welcome to ToDoRPG').classes('text-4xl text-center mb-4')
        setup_task_manager()  # Direkt den Task Manager für den User anzeigen
        ui.run()