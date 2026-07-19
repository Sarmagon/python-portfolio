"""
Главный модуль FastAPI приложения для кулинарной книги.

Реализует REST API с тремя эндпоинтами:
- POST /recipes — создание нового рецепта
- GET /recipes — получение списка всех рецептов (отсортированных по популярности)
- GET /recipes/{recipe_id} — получение детальной информации о рецепте

Использует асинхронную SQLAlchemy для работы с базой данных.
Применяет Dependency Injection для сессий и lifespan для управления жизненным циклом.
"""

from contextlib import asynccontextmanager
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

import models
import schemas
from database import Base, engine, get_session


# Современный способ управления запуском и остановкой приложения (lifespan)
# Заменяет устаревший @app.on_event("startup") и @app.on_event("shutdown")
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Контекстный менеджер жизненного цикла приложения.

    Выполняется при запуске: создаёт таблицы в базе данных.
    Выполняется при остановке: освобождает ресурсы движка.
    """
    # Код здесь выполняется ПРИ ЗАПУСКЕ (startup)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Код здесь выполняется ПРИ ОСТАНОВКЕ (shutdown)
    await engine.dispose()


# Инициализация FastAPI приложения с полной документацией
app = FastAPI(
    title="Cookbook API",
    description="""
    API для управления кулинарной книгой.
    
    ## Возможности:
    - Создание рецептов с ингредиентами
    - Получение списка всех рецептов (отсортировано по популярности)
    - Получение детальной информации о рецепте
    
    ## Сортировка списка рецептов:
    1. По убыванию количества просмотров (популярные сверху)
    2. При равенстве просмотров — по возрастанию времени готовки
    
    ## Просмотры:
    Счётчик просмотров увеличивается автоматически при каждом запросе 
    к детальной информации рецепта (GET /recipes/{recipe_id}).
    """,
    version="1.0.0",
    lifespan=lifespan,  # Подключаем lifespan для управления жизненным циклом
)


@app.post(
    "/recipes",
    response_model=schemas.RecipeOut,
    status_code=201,
    summary="Создать новый рецепт",
    description="""
    Создаёт новый рецепт с указанием названия, времени готовки, 
    описания и списка ингредиентов.
    
    - **title**: название блюда (1-100 символов)
    - **cook_time**: время приготовления в минутах (должно быть > 0)
    - **description**: текстовое описание рецепта (опционально)
    - **ingredients**: список ингредиентов с названием и количеством
    """,
)
async def create_recipe(
    recipe: schemas.RecipeIn, session: AsyncSession = Depends(get_session)
) -> models.Recipe:
    """
    Эндпоинт создания рецепта.

    Args:
        recipe: данные рецепта в формате RecipeIn (название, время, описание, ингредиенты)
        session: асинхронная сессия БД (внедряется через Dependency Injection)

    Returns:
        Созданный рецепт с присвоенным ID и начальным значением views=0
    """
    # Извлекаем данные из Pydantic модели (V1 синтаксис)
    data = recipe.dict()
    ingredients_data = data.pop("ingredients", [])

    # Создаём объект рецепта
    new_recipe = models.Recipe(**data)

    # Добавляем ингредиенты к рецепту
    for ing_data in ingredients_data:
        new_recipe.ingredients.append(models.Ingredient(**ing_data))

    # Сохраняем в базу данных
    session.add(new_recipe)
    await session.commit()
    await session.refresh(new_recipe)

    return new_recipe


@app.get(
    "/recipes",
    response_model=List[schemas.RecipeListItem],
    summary="Получить список всех рецептов",
    description="""
    Возвращает список всех рецептов в базе данных.
    
    ## Сортировка:
    1. **По убыванию просмотров** — самые популярные рецепты сверху
    2. **По возрастанию времени готовки** — если просмотры равны
    
    ## Возвращаемые поля:
    - id: уникальный идентификатор
    - title: название блюда
    - cook_time: время готовки в минутах
    - views: количество просмотров
    """,
)
async def get_recipes(
    session: AsyncSession = Depends(get_session),
) -> List[models.Recipe]:
    """
    Эндпоинт получения списка рецептов.

    Args:
        session: асинхронная сессия БД (внедряется через Dependency Injection)

    Returns:
        Список всех рецептов, отсортированных по популярности и времени готовки
    """
    # Запрос с сортировкой: сначала по views (убывание), потом по cook_time (возрастание)
    # selectinload предотвращает проблему N+1 запросов при загрузке ингредиентов
    res = await session.execute(
        select(models.Recipe)
        .options(selectinload(models.Recipe.ingredients))
        .order_by(models.Recipe.views.desc(), models.Recipe.cook_time.asc())
    )
    return res.scalars().all()


@app.get(
    "/recipes/{recipe_id}",
    response_model=schemas.RecipeOut,
    summary="Получить детальный рецепт",
    description="""
    Возвращает полную информацию о рецепте по его ID, включая список ингредиентов.
    
    **Важно:** При каждом запросе к этому эндпоинту счётчик просмотров 
    увеличивается на 1, что влияет на сортировку в списке рецептов.
    
    ## Возвращаемые поля:
    - id: уникальный идентификатор
    - title: название блюда
    - cook_time: время готовки в минутах
    - description: текстовое описание
    - views: количество просмотров (увеличено на 1)
    - ingredients: список ингредиентов с названием и количеством
    """,
)
async def get_recipe(
    recipe_id: int, session: AsyncSession = Depends(get_session)
) -> models.Recipe:
    """
    Эндпоинт получения детальной информации о рецепте.

    Args:
        recipe_id: уникальный идентификатор рецепта
        session: асинхронная сессия БД (внедряется через Dependency Injection)

    Returns:
        Полная информация о рецепте с ингредиентами

    Raises:
        HTTPException 404: если рецепт с указанным ID не найден
    """
    # Загружаем рецепт вместе с ингредиентами (eager loading для избежания N+1)
    res = await session.execute(
        select(models.Recipe)
        .options(selectinload(models.Recipe.ingredients))
        .where(models.Recipe.id == recipe_id)
    )
    recipe = res.scalars().first()

    # Если рецепт не найден — возвращаем 404
    if not recipe:
        raise HTTPException(
            status_code=404, detail=f"Рецепт с id={recipe_id} не найден"
        )

    # Увеличиваем счётчик просмотров
    recipe.views += 1

    # Сохраняем изменения
    await session.commit()
    await session.refresh(recipe)

    return recipe
