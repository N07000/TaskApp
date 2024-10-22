# task.py

from datetime import datetime

class Task:
    def __init__(self, taskname, taskdesc, difficulty='medium', status='pending', priority='normal', finaldate=None):
        self.taskname = taskname
        self.taskdesc = taskdesc
        self.difficulty = difficulty
        self.status = status  # pending, completed, etc.
        self.priority = priority  # low, normal, high
        self.finaldate = finaldate  # Deadline

    def mark_as_completed(self):
        self.status = 'completed'

    def update_task(self, taskname=None, taskdesc=None, difficulty=None, status=None, priority=None, finaldate=None):
        if taskname:
            self.taskname = taskname
        if taskdesc:
            self.taskdesc = taskdesc
        if difficulty:
            self.difficulty = difficulty
        if status:
            self.status = status
        if priority:
            self.priority = priority
        if finaldate:
            self.finaldate = finaldate

    def __str__(self):
        return f"Task: {self.taskname}, Description: {self.taskdesc}, Due: {self.finaldate}, Priority: {self.priority}, Status: {self.status}, Difficulty: {self.difficulty}"
