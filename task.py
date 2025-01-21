from database import create_quest, get_quests, complete_quest

class Quest:
    def __init__(self, id, name, description, difficulty, end_date, completed):
        self.id = id
        self.name = name
        self.description = description
        self.difficulty = difficulty
        self.end_date = end_date
        self.completed = completed

    @staticmethod
    def create_new(name, description, difficulty, end_date):
        create_quest(name, description, difficulty, end_date)

    @staticmethod
    def get_all():
        quests_data = get_quests()
        quests = []
        for q in quests_data:
            quest = Quest(*q)
            quests.append(quest)
        return quests

    @staticmethod
    def complete(quest_id):
        complete_quest(quest_id)


