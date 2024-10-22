# gui.py

from nicegui import ui
from task import Task
from database import save_task, get_tasks

def add_task():
    taskname = ui.input(label='Task Name').value
    taskdesc = ui.input(label='Task Description').value
    difficulty = ui.select(['easy', 'medium', 'hard'], label='Difficulty').value
    status = ui.select(['pending', 'completed'], label='Status').value
    priority = ui.select(['low', 'normal', 'high'], label='Priority').value
    finaldate = ui.input(label='Final Date (YYYY-MM-DD)').value
    
    task = Task(taskname, taskdesc, difficulty, status, priority, finaldate)
    save_task(task)
    ui.notify(f'New task "{taskname}" added!')

def show_tasks():
    tasks = get_tasks()
    for task in tasks:
        ui.label(f'Task: {task[1]}, Description: {task[2]}, Due: {task[6]}, Priority: {task[5]}, Status: {task[4]}, Difficulty: {task[3]}')

# Benutzeroberfläche aufbauen
def setup_gui():
    ui.label('ToDoRPG Task Manager')
    ui.button('Add Task', on_click=add_task)
    ui.button('Show Tasks', on_click=show_tasks)
    ui.run()
