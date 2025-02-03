from nicegui import ui
from gui import start_app
from database import initialize_database

def main():
    initialize_database()

    @ui.page('/')
    def index():
        start_app()

    ui.run(title='TaskApp', favicon='📝')

if __name__ in {'__main__', '__mp_main__'}:
    main()