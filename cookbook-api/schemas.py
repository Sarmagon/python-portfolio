from typing import List, Optional

from pydantic import BaseModel, Field

# ===== Схемы для ингредиента =====


class IngredientBase(BaseModel):
    """Базовая схема ингредиента с общими полями"""

    name: str = Field(
        ..., title="Название ингредиента", description="Например: 'Мука', 'Свёкла'"
    )
    amount: Optional[str] = Field(
        None, title="Количество", description="Например: '200 г', '2 шт'"
    )


class IngredientIn(IngredientBase):
    """Схема для создания ингредиента (входные данные)"""

    ...


class IngredientOut(IngredientBase):
    """Схема для отображения ингредиента (выходные данные с ID)"""

    id: int

    class Config:
        orm_mode = True  # Позволяет работать с ORM-объектами SQLAlchemy


# ===== Схемы для рецепта =====


class RecipeBase(BaseModel):
    """Базовая схема рецепта с общими полями"""

    title: str = Field(..., title="Название блюда", min_length=1, max_length=100)
    cook_time: int = Field(
        ..., title="Время готовки", description="Время приготовления в минутах", ge=1
    )
    description: Optional[str] = Field(
        None, title="Описание", description="Текстовое описание рецепта"
    )


class RecipeIn(RecipeBase):
    """Схема для создания рецепта (входные данные с ингредиентами)"""

    ingredients: List[IngredientIn] = Field(
        default_factory=list,
        title="Ингредиенты",
        description="Список необходимых ингредиентов",
    )


class RecipeOut(RecipeBase):
    """Схема для отображения полного рецепта (выходные данные с ID, просмотрами и ингредиентами)"""

    id: int
    views: int = Field(
        ...,
        title="Количество просмотров",
        description="Сколько раз открывали детальный рецепт",
    )
    ingredients: List[IngredientOut] = Field(default_factory=list)

    class Config:
        orm_mode = True


class RecipeListItem(BaseModel):
    """Схема для элемента списка рецептов (упрощенная, без ингредиентов)"""

    id: int
    title: str = Field(..., title="Название блюда")
    cook_time: int = Field(..., title="Время готовки (мин)")
    views: int = Field(..., title="Количество просмотров")

    class Config:
        orm_mode = True
