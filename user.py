# user.py

class User:
    def __init__(self, username, level=1, xp=0, coins=0):
        self.username = username
        self.level = level
        self.xp = xp
        self.coins = coins
        self.xp_until_next_level = 100

    def add_xp(self, xp):
        self.xp += xp
        print(f"{xp} XP received! Total XP: {self.xp}")
        self.check_level_up()

    def check_level_up(self):
        while self.xp >= self.xp_until_next_level:
            self.level += 1
            self.xp -= self.xp_until_next_level
            self.xp_until_next_level = int(self.xp_until_next_level * 1.5)  # Schwierigkeit des Level-Ups steigt
            self.coins += 100  # Belohnung für Level-Up
            print(f"Congratulations! You are now Level {self.level}. Coins: {self.coins}")

    def __str__(self):
        return f"User: {self.username}, Level: {self.level}, XP: {self.xp}/{self.xp_until_next_level}, Coins: {self.coins}"
