from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_recipe_keyboard(recipe_url: str) -> InlineKeyboardMarkup:
    """📖 Inline-кнопка для просмотра полного рецепта"""
    keyboard = InlineKeyboardMarkup()
    
    if recipe_url:
        keyboard.add(
            InlineKeyboardButton(
                "📖 Полный рецепт",
                url=recipe_url
            )
        )
    
    return keyboard


def get_recipes_list_keyboard(recipes: list) -> InlineKeyboardMarkup:
    """📋 Inline-кнопки для списка рецептов"""
    keyboard = InlineKeyboardMarkup()
    
    for recipe in recipes[:5]:  # Максимум 5 кнопок
        url = recipe.get('url', '')
        label = recipe.get('label', 'Без названия')[:30]
        
        if url:
            keyboard.add(
                InlineKeyboardButton(
                    f"📖 {label}",
                    url=url
                )
            )
    
    return keyboard


def get_history_keyboard() -> InlineKeyboardMarkup:
    """🗑️ Inline-кнопка для очистки истории"""
    keyboard = InlineKeyboardMarkup()
    
    keyboard.add(
        InlineKeyboardButton(
            "🗑️ Очистить историю",
            callback_data="clear_history"
        )
    )
    
    return keyboard