"""
Модуль ORM-моделей для кулинарной книги.

Описывает две сущности:
- Recipe: рецепт (название, время готовки, описание, счётчик просмотров)
- Ingredient: ингредиент (название, количество, привязка к рецепту)

Связь: один рецепт — много ингредиентов (One-to-Many).
"""

from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Recipe(Base):
    """
    Модель рецепта.
    
    Атрибуты:
        id: уникальный идентификатор рецепта (первичный ключ)
        title: название блюда (индексируется для быстрого поиска)
        cook_time: время приготовления в минутах
        description: текстовое описание рецепта (опционально)
        views: счётчик просмотров (увеличивается при открытии деталей)
        ingredients: список связанных ингредиентов
    """
    __tablename__ = 'Recipe'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    cook_time = Column(Integer)
    description = Column(Text, nullable=True)
    views = Column(Integer, default=0)
    
    # Связь с ингредиентами: один рецепт — много ингредиентов
    # cascade="all, delete-orphan" — при удалении рецепта удаляются и его ингредиенты
    ingredients = relationship(
        "Ingredient", 
        back_populates="recipe", 
        cascade="all, delete-orphan",
        lazy="selectin" 
    )


class Ingredient(Base):
    """
    Модель ингредиента.
    
    Атрибуты:
        id: уникальный идентификатор ингредиента (первичный ключ)
        name: название ингредиента
        amount: количество (например, '200 г', '2 шт') — опционально
        recipe_id: внешний ключ, привязка к рецепту
        recipe: обратная связь с моделью Recipe
    """
    __tablename__ = 'Ingredient'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    amount = Column(String, nullable=True)
    recipe_id = Column(Integer, ForeignKey("Recipe.id"), nullable=False)
    
    # Обратная связь: ингредиент принадлежит одному рецепту
    recipe = relationship("Recipe", back_populates="ingredients")