from nicegui import ui
from user import User
from task import Quest
from database import user_exists, create_user, delete_user

def start_app():
    if not user_exists():
        show_user_creation()
    else:
        show_main_interface()

def show_user_creation():
    with ui.card().classes('w-96 mx-auto mt-10'):
        ui.markdown('## Nutzer erstellen')
        name = ui.input('Username eingeben').classes('mt-5')
        race = ui.input('Rasse eingeben')
        user_class = ui.input('Klasse eingeben')
        def create():
            create_user(name.value, user_class.value, race.value)
            ui.notify('Nutzer erfolgreich erstellt!', color='green')
            ui.run_javascript('window.location.reload()')
        ui.button('Nutzer erstellen', on_click=create).classes('mt-5')

def show_main_interface():
    user = User()
    with ui.row().classes('justify-between items-center mt-5 mx-5'):
        with ui.column():
            ui.markdown(f'### {user.name} ({user.user_class})')
            ui.markdown(f'**Rasse:** {user.race}')
        with ui.column().classes('text-right'):
            ui.markdown(f'**Level:** {user.level}')
            ui.markdown(f'**XP:** {user.xp}/{user.max_xp}')
    
    with ui.row().classes('justify-end mx-5'):
        ui.button('Quest erstellen', on_click=show_quest_creation)
        ui.button('Nutzer löschen', on_click=confirm_user_deletion, color='red')
    
    quests = Quest.get_all()
    for quest in quests:
        with ui.card().classes('mt-5 mx-5'):
            with ui.row().classes('justify-between'):
                ui.markdown(f'### {quest.name}')
                ui.button('Abschließen', on_click=lambda q=quest: complete_quest_action(q))
            ui.markdown(quest.description)
            ui.markdown(f'**Schwierigkeit:** {quest.difficulty.capitalize()}')
            ui.markdown(f'**Enddatum:** {quest.end_date}')

def show_quest_creation():
    with ui.dialog() as quest_dialog, ui.card().classes('w-96'):
        ui.markdown('## Neue Quest erstellen')
        name = ui.input('Name der Quest').classes('mt-5')
        description = ui.textarea('Beschreibung der Quest')
        end_date = ui.input('Enddatum (YYYY-MM-DD)')
        ui.label('Schwierigkeit auswählen')
        difficulty = ui.radio(['Leicht', 'Mittel', 'Schwer'], value='Leicht')
        def create():
            Quest.create_new(name.value, description.value, difficulty.value.lower(), end_date.value)
            ui.notify('Quest erfolgreich erstellt!', color='green')
            quest_dialog.close()
            ui.run_javascript('window.location.reload()')
        ui.button('Quest erstellen', on_click=create).classes('mt-5')
    quest_dialog.open()

def confirm_user_deletion():
    with ui.dialog() as delete_user_dialog, ui.card().classes('w-96'):
        ui.markdown('## Nutzer löschen')
        ui.label('Möchten Sie den Nutzer wirklich löschen?')
        with ui.row().classes('justify-end'):
            ui.button('Abbrechen', on_click=delete_user_dialog.close)
            def delete():
                delete_user()
                ui.notify('Nutzer und alle Quests wurden gelöscht!', color='red')
                delete_user_dialog.close()
                ui.run_javascript('window.location.reload()')
            ui.button('Löschen', on_click=delete, color='red')
    delete_user_dialog.open()

def complete_quest_action(quest):
    Quest.complete(quest.id)
    xp_reward = {'leicht': 50, 'mittel': 100, 'schwer': 150}
    user = User()
    user.add_xp(xp_reward[quest.difficulty])
    ui.notify(f'Quest "{quest.name}" abgeschlossen! {xp_reward[quest.difficulty]} XP erhalten.', color='green')
    ui.run_javascript('window.location.reload()')
