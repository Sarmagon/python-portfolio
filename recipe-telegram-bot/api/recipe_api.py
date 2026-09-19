"""
🌐 API для поиска рецептов (TheMealDB)
Прямой поиск в API + словарь для перевода с русского
"""

import requests
from typing import Optional, List, Dict, Any

# 🌍 TheMealDB API URL
THE_MEAL_DB_URL = "https://www.themealdb.com/api/json/v1/1"

# 🌍 Импортируем словари переводов из отдельного файла
from api.translations import DISH_NAMES_RU, INGREDIENT_TRANSLATIONS


def _parse_meal_from_api(meal: Dict) -> Dict[str, Any]:
    """
    Парсит данные о блюде из API TheMealDB.
    
    Args:
        meal: Словарь с данными о блюде от API
        
    Returns:
        Словарь с обработанными данными о рецепте
    """
    ingredients: List[str] = []
    for i in range(1, 21):
        ingredient = meal.get(f'strIngredient{i}', '').strip()
        measure = meal.get(f'strMeasure{i}', '').strip()
        if ingredient:
            ingredients.append(f"{ingredient} {measure}".strip())
    
    url = meal.get('strSource', '') or f"https://www.themealdb.com/meal/{meal.get('idMeal', '')}"
    
    return {
        "label": meal.get("strMeal", "Рецепт"),
        "ingredientLines": ingredients,
        "instructions": meal.get("strInstructions", "Нет инструкции"),
        "url": url,
    }


def search_by_name(dish_name: str) -> Optional[Dict[str, Optional[str]]]:
    """
    🔎 Поиск по названию через TheMealDB API.
    Сначала пробует оригинальный термин, потом перевод (для русского).
    
    Args:
        dish_name: Название блюда (русский или английский)
        
    Returns:
        Словарь с данными о рецепте или None если не найдено
    """
    dish_name = dish_name.strip()
    
    # 🎯 ШАГ 1: Пробуем ОРИГИНАЛЬНЫЙ термин (работает для English)
    try:
        response = requests.get(
            f"{THE_MEAL_DB_URL}/search.php",
            params={"s": dish_name},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        if data.get("meals"):
            meal = data["meals"][0]
            return _parse_meal_from_api(meal)
    except Exception as e:
        print(f"⚠️ Ошибка API (оригинал): {e}")
    
    # 🎯 ШАГ 2: Если не нашли — пробуем перевод (для Russian)
    dish_name_lower = dish_name.lower()
    if dish_name_lower in DISH_NAMES_RU:
        english_name = DISH_NAMES_RU[dish_name_lower]
        try:
            response = requests.get(
                f"{THE_MEAL_DB_URL}/search.php",
                params={"s": english_name},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("meals"):
                meal = data["meals"][0]
                return _parse_meal_from_api(meal)
        except Exception as e:
            print(f"⚠️ Ошибка API (перевод): {e}")
    
    return None


def search_by_ingredient(ingredient: str) -> List[Dict[str, str]]:
    """
    🥕 Поиск по ингредиенту через TheMealDB API.
    Сначала пробует оригинальный термин, потом перевод (для русского).
    
    Args:
        ingredient: Название ингредиента (русский или английский)
        
    Returns:
        Список словарей с данными о рецептах (максимум 10)
    """
    ingredient = ingredient.strip()
    
    # 🎯 ШАГ 1: Пробуем ОРИГИНАЛЬНЫЙ термин (работает для English)
    try:
        response = requests.get(
            f"{THE_MEAL_DB_URL}/filter.php",
            params={"i": ingredient},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        if data.get("meals"):
            return [
                {
                    "label": meal.get("strMeal", "Без названия"),
                    "url": f"https://www.themealdb.com/meal/{meal.get('idMeal', '')}",
                }
                for meal in data["meals"][:10]
            ]
    except Exception as e:
        print(f"⚠️ Ошибка API (оригинал): {e}")
    
    # 🎯 ШАГ 2: Если не нашли — пробуем перевод (для Russian)
    ingredient_lower = ingredient.lower()
    if ingredient_lower in INGREDIENT_TRANSLATIONS:
        english_ingredient = INGREDIENT_TRANSLATIONS[ingredient_lower]
        try:
            response = requests.get(
                f"{THE_MEAL_DB_URL}/filter.php",
                params={"i": english_ingredient},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("meals"):
                return [
                    {
                        "label": meal.get("strMeal", "Без названия"),
                        "url": f"https://www.themealdb.com/meal/{meal.get('idMeal', '')}",
                    }
                    for meal in data["meals"][:10]
                ]
        except Exception as e:
            print(f"⚠️ Ошибка API (перевод): {e}")
    
    return []