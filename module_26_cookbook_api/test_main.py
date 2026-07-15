"""
Тесты для Cookbook API.
Использует pytest фикстуры для гарантированного создания таблиц перед тестами.
"""

import asyncio
import pytest
from fastapi.testclient import TestClient

from main import app
from database import engine
import models


# Эта фикстура запускается ОДИН раз перед всеми тестами в файле
# и гарантированно создаёт таблицы в базе данных
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    async def create_tables():
        async with engine.begin() as conn:
            await conn.run_sync(models.Base.metadata.create_all)
    
    # Запускаем асинхронную функцию в синхронном контексте pytest
    asyncio.run(create_tables())
    yield


# Создаём клиент один раз на весь модуль тестов, 
# чтобы не закрывать engine и session между отдельными тестами
client = TestClient(app)


def test_create_recipe():
    """Тест создания рецепта с ингредиентами."""
    response = client.post(
        "/recipes",
        json={
            "title": "Борщ",
            "cook_time": 120,
            "description": "Классический рецепт",
            "ingredients": [
                {"name": "Свёкла", "amount": "300 г"}
            ]
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Борщ"
    assert data["views"] == 0
    assert len(data["ingredients"]) == 1


def test_get_recipes_sorted():
    """Тест сортировки: при равных просмотрах сначала идёт рецепт с меньшим временем."""
    client.post("/recipes", json={"title": "Долгий рецепт", "cook_time": 100})
    client.post("/recipes", json={"title": "Быстрый рецепт", "cook_time": 10})
    
    response = client.get("/recipes")
    assert response.status_code == 200
    recipes = response.json()
    
    # Проверяем, что последние два добавленных рецепта отсортированы правильно
    # (они будут в конце списка, если там были другие рецепты, но между собой они отсортированы)
    # Для чистоты теста найдём их в списке:
    titles = [r["title"] for r in recipes]
    assert titles.index("Быстрый рецепт") < titles.index("Долгий рецепт")


def test_views_increment():
    """Тест увеличения счётчика просмотров."""
    create_resp = client.post("/recipes", json={"title": "Тест на просмотры", "cook_time": 30})
    recipe_id = create_resp.json()["id"]
    
    response = None
    # Открываем рецепт 3 раза и сохраняем последний ответ
    for _ in range(3):
        response = client.get(f"/recipes/{recipe_id}")
    
    # Проверяем счётчик в последнем ответе (он должен быть равен 3)
    assert response.status_code == 200
    assert response.json()["views"] == 3


def test_get_recipe_not_found():
    """Тест обработки ошибки 404."""
    response = client.get("/recipes/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Рецепт с id=99999 не найден"


def test_create_recipe_without_ingredients():
    """Тест создания рецепта без ингредиентов (допустимый случай)."""
    response = client.post(
        "/recipes",
        json={
            "title": "Простой рецепт",
            "cook_time": 15,
            "description": "Рецепт без ингредиентов"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Простой рецепт"
    assert data["ingredients"] == []