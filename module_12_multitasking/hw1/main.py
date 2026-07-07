import sqlite3
import time
import multiprocessing
import requests
from multiprocessing import Pool, pool


def fetch_character(character_id: int) -> dict:
    """Загружает данные одного персонажа из API"""
    url = f"https://swapi.tech/api/people/{character_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        result = data.get("result", {}).get("properties", {})
        return {
            "id": character_id,
            "name": result.get("name"),
            "gender": result.get("gender"),
            "birth_year": result.get("birth_year")
        }
    except requests.exceptions.HTTPError:
        print(f"   ⚠️ Персонаж {character_id} не найден (404)")
        return None


def init_db(db_path: str = "star_wars.db") -> None:
    """Создаёт таблицу в БД"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            birth_year TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_to_db(characters: list, db_path: str = "star_wars.db") -> None:
    """Сохраняет список персонажей в БД"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executemany(
        "INSERT OR REPLACE INTO characters (id, name, gender, birth_year) VALUES (?, ?, ?, ?)",
        [(c["id"], c["name"], c["gender"], c["birth_year"]) for c in characters if c is not None]
    )
    conn.commit()
    conn.close()


def fetch_with_pool(num_processes: int = 4) -> float:
    """Загружает персонажей с использованием пула процессов"""
    init_db()
    start_time = time.time()
    
    character_ids = list(range(1, 21))
    
    with Pool(processes=num_processes) as pool:
        characters = pool.map(fetch_character, character_ids)
    
    save_to_db(characters)
    
    elapsed = time.time() - start_time
    return elapsed


def fetch_with_thread_pool(num_threads: int = 10) -> float:
    """Загружает персонажей с использованием пула потоков"""
    init_db()
    start_time = time.time()
    
    character_ids = list(range(1, 21))
    
    with pool.ThreadPool(processes=num_threads) as thread_pool:
        characters = thread_pool.map(fetch_character, character_ids)
    
    save_to_db(characters)
    
    elapsed = time.time() - start_time
    return elapsed


def main() -> None:
    cpu = multiprocessing.cpu_count()  
    
    print("=" * 60)
    print("Загрузка 20 персонажей из Star Wars API")
    print(f"Обнаружено ядер CPU: {cpu}")  
    print("=" * 60)
    
    print(f"\n1. Тестирование multiprocessing.Pool ({cpu} процессов)...") 
    time_pool = fetch_with_pool(num_processes=cpu) 
    print(f"   Время: {time_pool:.2f} сек")
    
    print(f"\n2. Тестирование ThreadPool ({cpu * 2} потоков)...") 
    time_thread = fetch_with_thread_pool(num_threads=cpu * 2)  
    print(f"   Время: {time_thread:.2f} сек")
    
    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТЫ:")
    print(f"   Pool (процессы): {time_pool:.2f} сек")
    print(f"   ThreadPool (потоки): {time_thread:.2f} сек")
    
    if time_thread < time_pool:
        print(f"\n   ✅ Потоки быстрее в {time_pool / time_thread:.2f} раз")
    else:
        print(f"\n   ✅ Процессы быстрее в {time_thread / time_pool:.2f} раз")
    
    print("=" * 60)


if __name__ == "__main__":
    main()