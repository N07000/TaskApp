from database import create_quest, get_quests, complete_quest, update_quest, delete_quest

class Quest:
    def __init__(self, id, name, description, difficulty, end_date, current_status, completed):
        self.id = id
        self.name = name
        self.description = description
        self.difficulty = difficulty
        self.end_date = end_date
        self.current_status = current_status
        self.completed = completed

    @staticmethod
    def create_new(name, description, difficulty, end_date, current_status):
        create_quest(name, description, difficulty, end_date, current_status)

    @staticmethod
    def get_all():
        quests_data = get_quests()
        quests = []
        for q in quests_data:
            quest = Quest(*q)
            quests.append(quest)
        return quests
    
    @staticmethod
    def update_existing(quest_id, name, description, difficulty, end_date, current_status):
        update_quest(quest_id, name, description, difficulty, end_date, current_status)

    @staticmethod
    def delete(quest_id):
        delete_quest(quest_id)

    @staticmethod
    def complete(quest_id):
        complete_quest(quest_id)


