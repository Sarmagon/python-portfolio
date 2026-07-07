"""
Быстрый тест всех endpoint сервиса обработки изображений.
Запуск: python test_api.py
"""
import os
import requests
import sys
from dotenv import load_dotenv

load_dotenv()
BASE_URL = "http://127.0.0.1:5000"
TEST_EMAIL = os.getenv("SMTP_USER", "test@example.com")


def test_blur():
    """POST /blur"""
    with open("test1.jpg", "rb") as f1, open("test2.jpg", "rb") as f2:
        files = [
            ("images", ("test1.jpg", f1, "image/jpeg")),
            ("images", ("test2.jpg", f2, "image/jpeg")),
        ]
        resp = requests.post(f"{BASE_URL}/blur", files=files, data={"email": TEST_EMAIL})
    assert resp.status_code == 202, f"/blur: {resp.status_code}"
    data = resp.json()
    assert "group_id" in data
    print(f"✅ POST /blur — OK (group_id={data['group_id'][:8]}...)")
    return data["group_id"]


def test_status(group_id):
    """GET /status/<id>"""
    import time
    for _ in range(30):
        resp = requests.get(f"{BASE_URL}/status/{group_id}")
        if resp.status_code == 200 and resp.json().get("status") == "completed":
            break
        time.sleep(1)
    else:
        raise AssertionError("/status: задачи не завершились за 30 сек")
    print(f"✅ GET /status/{group_id[:8]}... — completed")


def test_subscribe():
    """POST /subscribe"""
    resp = requests.post(f"{BASE_URL}/subscribe", data={"email": TEST_EMAIL})
    assert resp.status_code in (200, 201), f"/subscribe: {resp.status_code}"
    print(f"✅ POST /subscribe — OK ({resp.json()['message']})")


def test_unsubscribe():
    """POST /unsubscribe"""
    resp = requests.post(f"{BASE_URL}/unsubscribe", data={"email": TEST_EMAIL})
    assert resp.status_code == 200, f"/unsubscribe: {resp.status_code}"
    print(f"✅ POST /unsubscribe — OK ({resp.json()['message']})")


if __name__ == "__main__":
    try:
        gid = test_blur()
        test_status(gid)
        test_subscribe()
        test_unsubscribe()
        print("\n🎉 Все тесты пройдены!")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        sys.exit(1)