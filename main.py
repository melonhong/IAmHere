from models import initialize_database
from views import main_view

def main():
    # DB 초기화
    initialize_database()

    # GUI 실행
    main_view.run_gui()

if __name__ == "__main__":
    main()
