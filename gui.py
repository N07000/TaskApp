from nicegui import ui
from user import User
from task import Quest
from database import user_exists, create_user, delete_user, update_dark_mode, get_dark_mode

def start_app():
    if not user_exists():
        show_user_creation()
    else:
        show_main_interface()

def show_user_creation():
    ui.query('body').classes('bg-gradient-to-t from-blue-400 to-blue-100')
    with ui.card().classes('w-96 mx-auto mt-10'):
        ui.markdown('###Willkommen')
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
    #ui.button.default_props('rounded outline') #--- STANDARDEIGENSCHAFTEN FÜR KNÖPFE ---
    dark = ui.dark_mode()
    #dark.enable()
    if user.dark_mode:
        dark.enable()
    else:
        dark.disable()

    with ui.card(align_items='baseline').classes('w-full shadow-lg'):
        with ui.row().classes('justify-between items-center mt-5 mx-5'):
            with ui.column():
                ui.markdown(f'## **{user.name} ({user.user_class})**')
                ui.markdown(f'**Rasse:** {user.race}')
            with ui.column().classes('text-right'):
                ui.markdown(f'**Level:** {user.level}')
                ui.linear_progress(value=user.xp / user.max_xp, show_value=False, color="#00BFFF").classes('w-96')
                #ui.markdown(f'**XP:** {user.xp}/{user.max_xp}')
        
        with ui.row().classes('justify-end mx-5'):
            ui.button('Quest erstellen', on_click=show_quest_creation)
            ui.button('Nutzer löschen', on_click=confirm_user_deletion, color='red')
            def enable_dark():
                dark.enable()
                update_dark_mode(True)
                
            def disable_dark():
                dark.disable()
                update_dark_mode(False)
            if user.level >= 2:
                ui.markdown('   **Design:**   ')
                ui.button('Darkmode', on_click=enable_dark)
                ui.button('Lightmode', on_click=disable_dark)

        # Erstelle eine Zeile für die Quests
    quests = Quest.get_all()

    # Erstelle eine Zeile für die Quests
    with ui.row().classes('flex flex-wrap justify-start'):
        for quest in quests:
            with ui.card().classes('mt-5 mx-2 w-64 min-h-[300px] flex flex-col'):  # Feste Breite und minimale Höhe
                with ui.row().classes('justify-between'):
                    ui.markdown(f'### {quest.name}')
                ui.markdown(quest.description)  # Beschreibung ohne 'classes'
                ui.markdown(f'**Schwierigkeit:** {quest.difficulty.capitalize()}')
                ui.markdown(f'**Enddatum:** {quest.end_date}')
                ui.button('Abschließen', on_click=lambda q=quest: complete_quest_action(q), color='green').classes('flex justify-center')

def show_quest_creation():
    with ui.dialog() as quest_dialog, ui.card(align_items='stretch').classes('w-96'):
        ui.markdown('## Neue Quest erstellen')
        name = ui.input('Name der Quest').classes('mt-5')
        description = ui.input('Beschreibung der Quest')
        ui.markdown()
        ui.markdown(f'**Enddatum auswählen**')
        end_date = ui.date(mask='DD.MM.YYYY').classes('mt-2 w-full')
        ui.markdown()
        ui.markdown('**Schwierigkeit auswählen**')
        difficulty = ui.radio(['Leicht', 'Mittel', 'Schwer'], value='Leicht')
        def create():
            Quest.create_new(name.value, description.value, difficulty.value.lower(), end_date.value)
            ui.notify('Quest erfolgreich erstellt!', color='green')
            quest_dialog.close()
            ui.run_javascript('window.location.reload()')
        ui.button('Quest erstellen', on_click=create).classes('mt-5')
    quest_dialog.open()

def confirm_user_deletion():
    with ui.dialog() as delete_user_dialog, ui.card(align_items='stretch').classes('w-70'):
        ui.markdown('## Nutzer löschen?')
        ui.label('Möchten Sie den Nutzer wirklich löschen?')
        with ui.row().classes('justify-center'):
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
    