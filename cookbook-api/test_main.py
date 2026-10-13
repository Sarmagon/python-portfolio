"""
Тесты для Cookbook API.
Каждый тест запускает приложение на новой временной базе через lifespan.
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import database
import main


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Application startup, rather than the fixture, must create the tables.
    test_engine = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'test.db'}")
    monkeypatch.setattr(main, "engine", test_engine)
    monkeypatch.setattr(
        database,
        "async_session",
        sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession),
    )
    with TestClient(main.app) as test_client:
        yield test_client


def test_fresh_database_startup(client):
    response = client.get("/recipes")
    assert response.status_code == 200
    assert response.json() == []


def test_engine_disposed_on_shutdown(client, monkeypatch):
    dispose = AsyncMock(wraps=main.engine.dispose)
    monkeypatch.setattr(
        main, "engine", SimpleNamespace(begin=main.engine.begin, dispose=dispose)
    )
    with TestClient(main.app):
        pass
    dispose.assert_awaited_once()


def test_create_recipe(client):
    """Тест создания рецепта с ингредиентами."""
    response = client.post(
        "/recipes",
        json={
            "title": "Борщ",
            "cook_time": 120,
            "description": "Классический рецепт",
            "ingredients": [{"name": "Свёкла", "amount": "300 г"}],
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Борщ"
    assert data["views"] == 0
    assert len(data["ingredients"]) == 1


def test_get_recipes_sorted(client):
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


def test_views_increment(client):
    """Тест увеличения счётчика просмотров."""
    create_resp = client.post(
        "/recipes", json={"title": "Тест на просмотры", "cook_time": 30}
    )
    recipe_id = create_resp.json()["id"]

    response = None
    # Открываем рецепт 3 раза и сохраняем последний ответ
    for _ in range(3):
        response = client.get(f"/recipes/{recipe_id}")

    # Проверяем счётчик в последнем ответе (он должен быть равен 3)
    assert response.status_code == 200
    assert response.json()["views"] == 3


def test_get_recipe_not_found(client):
    """Тест обработки ошибки 404."""
    response = client.get("/recipes/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Рецепт с id=99999 не найден"


def test_create_recipe_without_ingredients(client):
    """Тест создания рецепта без ингредиентов (допустимый случай)."""
    response = client.post(
        "/recipes",
        json={
            "title": "Простой рецепт",
            "cook_time": 15,
            "description": "Рецепт без ингредиентов",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Простой рецепт"
    assert data["ingredients"] == []
