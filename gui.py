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
    ui.query('body').classes('bg-gradient-to-t from-blue-400 to-blue-100')
    with ui.card().classes('w-96 mx-auto mt-10'):
        ui.markdown('## Nutzer erstellen')
        with ui.stepper().props('vertical').classes('w-full') as stepper:
            with ui.step('Nutzername'):
                name = ui.input('Nutzername eingeben', validation={'Pflichtfeld': lambda value: len(value) != 0}).classes('mt-5')
                with ui.stepper_navigation():
                    ui.button('weiter', on_click=stepper.next)
            with ui.step('Rasse'):
                race = ui.input('Rasse eingeben', validation={'Pflichtfeld': lambda value: len(value) != 0})
                with ui.stepper_navigation():
                    ui.button('weiter', on_click=stepper.next)
                    ui.button('zurück', on_click=stepper.previous).props('flat')
            with ui.step('Klasse'):
                user_class = ui.input('Klasse eingeben', validation={'Pflichtfeld': lambda value: len(value) != 0})
                with ui.stepper_navigation():
                    def create():
                        create_user(name.value, user_class.value, race.value)
                        ui.notify('Nutzer erfolgreich erstellt!', color='green')
                        ui.run_javascript('window.location.reload()')
                    ui.button('Nutzer erstellen', on_click=create)
                    ui.button('zurück', on_click=stepper.previous).props('flat')
def show_main_interface():
    user = User()
    ui.colors(primary='#555') #--- STANDARDFARBE FÜR KNÖPFE ---

    with ui.card():
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
            dark = ui.dark_mode()
            ui.label('   Design:   ')
            ui.button('Darkmode', on_click=dark.enable)
            ui.button('Lightmode', on_click=dark.disable)

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
        ui.label('Enddatum auswählen')
        end_date = ui.date(on_change=lambda e: result.set_text(e.value), mask='DD.MM.YYYY')
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
    ui.run_javascript('window.location.reload()')
    ui.notify(f'Quest "{quest.name}" abgeschlossen! {xp_reward[quest.difficulty]} XP erhalten.', color='green', type='positive')
    