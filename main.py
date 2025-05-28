from models import initialize_database
from viewss import main_views  # gui/gui_main.py 에 run_gui() 함수가 있다고 가정

def main():
    # DB 초기화
    initialize_database()

    # GUI 실행
    main_views.run_gui()

if __name__ == "__main__":
    main()
