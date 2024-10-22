# task.py

from datetime import datetime

class Task:
    def __init__(self, taskname, taskdesc, difficulty='medium', status='pending', priority='normal', finaldate=None):
        self.taskname = taskname
        self.taskdesc = taskdesc
        self.difficulty = difficulty
        self.status = status  # pending, completed
        self.priority = priority  # low, normal, high
        self.finaldate = finaldate  # Deadline

    def mark_as_completed(self):
        self.status = 'completed'

    def get_xp_reward(self):
        # XP-Belohnung je nach Schwierigkeitsgrad
        if self.difficulty == 'easy':
            return 10
        elif self.difficulty == 'medium':
            return 20
        elif self.difficulty == 'hard':
            return 30

    def __str__(self):
        return f"Task: {self.taskname}, Due: {self.finaldate}, Status: {self.status}, Priority: {self.priority}, Difficulty: {self.difficulty}"
