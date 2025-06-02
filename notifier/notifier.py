import requests
from config import NOTIFY_API_URL, TOKEN

def send_check(id, lecture_title: str):
    if not NOTIFY_API_URL:
        raise ValueError("환경변수 NOTIFY_API_URL이 설정되지 않았습니다.")
    params = {"user_id": id, "lecture_title": lecture_title, "token": TOKEN}  # 쿼리 파라미터로 보낼 데이터
    try:
        response = requests.get(NOTIFY_API_URL + "/second-check", params=params)
        response.raise_for_status()
        print(f"✅ 알림 전송 성공: {response.json()}")
    except requests.RequestException as e:
        print(f"❌ 알림 전송 실패: {e}\n응답 내용: {getattr(e.response, 'text', '응답 없음')}")

def send_result(id, result: bool):
    if not NOTIFY_API_URL:
        raise ValueError("환경변수 NOTIFY_API_URL이 설정되지 않았습니다.")
    params = {"user_id": id, "result": result, "token": TOKEN}  # 쿼리 파라미터로 보낼 데이터
    try:
        response = requests.get(NOTIFY_API_URL + "/second-result", params=params)
        response.raise_for_status()
        print(f"✅ 알림 전송 성공: {response.json()}")
    except requests.RequestException as e:
        print(f"❌ 알림 전송 실패: {e}\n응답 내용: {getattr(e.response, 'text', '응답 없음')}")

