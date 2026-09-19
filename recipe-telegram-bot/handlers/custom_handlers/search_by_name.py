from telebot.types import Message
from loader import bot
from keyboards.reply.main_menu import get_main_menu_keyboard
from keyboards.inline.recipe_keyboard import get_recipe_keyboard
from api.recipe_api import search_by_name
from database.models import SearchHistory, User
from utils.user_states import delete_state


def process_dish_name(message: Message):
    """🔎 Обрабатываем название блюда"""
    
    text = message.text
    if not text:
        return
    
    # ⛔ Отмена
    if text.lower() in ["отмена", "❌ отмена", "cancel"]:
        delete_state(message.from_user.id)
        bot.send_message(
            chat_id=message.chat.id,
            text="✅ Отменено. Выберите команду в меню:",
            reply_markup=get_main_menu_keyboard()
        )
        return
    
    # ⚠️ Команды
    if text.startswith('/'):
        delete_state(message.from_user.id)
        return
    
    # 💾 Сохраняем в историю
    try:
        user, created = User.get_or_create(
            user_id=message.from_user.id,
            defaults={
                "username": message.from_user.username,
                "first_name": message.from_user.first_name or "",
                "last_name": message.from_user.last_name or "",
            }
        )
        recipe = search_by_name(text)
        SearchHistory.create(
            user=user,
            query=text,
            result_summary=recipe.get('label', 'Не найдено') if recipe else 'Не найдено'
        )
    except Exception as e:
        print(f"⚠️ Ошибка сохранения в историю: {e}")
    
    # 🔍 Ищем рецепт
    recipe = search_by_name(text)
    
    if recipe:
        recipe_text = f"""
🍳 **{recipe.get('label', 'Рецепт')}**

📝 **Ингредиенты:**
"""
        ingredients = recipe.get('ingredientLines', [])
        if isinstance(ingredients, list):
            for ing in ingredients:
                recipe_text += f"• {ing}\n"
        
        instructions = recipe.get('instructions', 'Нет инструкции')
        if instructions:
            recipe_text += f"\n📖 **Инструкция:**\n{instructions}"
        
        url = recipe.get('url', '')

        bot.send_message(
            chat_id=message.chat.id,
            text=recipe_text,
            parse_mode="Markdown",
            reply_markup=get_recipe_keyboard(url) if url else get_main_menu_keyboard()
        )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text=f"❌ Рецепт **{text}** не найден.\n\n"
                 f"🍳 **10+ гарантированно рабочих блюд:**\n\n"
                 f"🇷🇺 **На русском:**\n"
                 f"• Пицца, Спагетти, Лазанья\n"
                 f"• Курица, Говядина, Стейк\n"
                 f"• Рыба, Лосось, Креветки\n"
                 f"• Суп, Бургер, Салат\n"
                 f"• Омлет, Блины, Карри\n"
                 f"• Пирог, Торт, Печенье\n"
                 f"• Рис, Картофель, Томат\n"
                 f"• Яблоко, Банан, Клубника\n"
                 f"• Сыр, Молоко, Йогурт\n"
                 f"• Шоколад, Кофе, Мёд\n\n"
                 f"🇬 **На английском (лучшие результаты):**\n"
                 f"• Pizza, Spaghetti, Lasagna\n"
                 f"• Chicken, Beef, Steak\n"
                 f"• Fish, Salmon, Shrimp\n"
                 f"• Soup, Burger, Salad\n"
                 f"• Omelette, Pancake, Curry\n"
                 f"• Pie, Cake, Cookie\n"
                 f"• Rice, Potato, Tomato\n"
                 f"• Apple, Banana, Strawberry\n"
                 f"• Cheese, Milk, Yogurt\n"
                 f"• Chocolate, Coffee, Honey\n\n"
                 f"💡 **Совет:** Вводите на английском для 100% результата!\n"
                 f"📋 Всего в API: 1000+ рецептов",
            parse_mode="Markdown",
            reply_markup=get_main_menu_keyboard()
        )

        delete_state(message.from_user.id)