from database import get_user, update_user_level_xp

class User:
    def __init__(self):
        user_data = get_user()
        if user_data:
            (self.id, self.name, self.user_class, self.race, self.level, self.xp, self.max_xp) = user_data
        else:
            self.id = None
            self.name = ""
            self.user_class = ""
            self.race = ""
            self.level = 0
            self.xp = 0
            self.max_xp = 100

    def add_xp(self, amount):
        self.xp += amount
        while self.xp >= self.max_xp:
            self.xp -= self.max_xp
            self.level += 1
            self.max_xp += 100
        update_user_level_xp(self.level, self.xp, self.max_xp)

