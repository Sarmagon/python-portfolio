from telebot.types import Message
from loader import bot
from keyboards.reply.main_menu import get_main_menu_keyboard
from keyboards.inline.recipe_keyboard import get_recipes_list_keyboard
from api.recipe_api import search_by_ingredient
from database.models import SearchHistory, User
from utils.user_states import delete_state


def process_ingredient(message: Message):
    """🥕 Обрабатываем ингредиент"""
    
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
        recipes = search_by_ingredient(text)
        SearchHistory.create(
            user=user,
            query=text,
            result_summary=f"{len(recipes)} рецептов найдено" if recipes else "Не найдено"
        )
    except Exception as e:
        print(f"⚠️ Ошибка сохранения в историю: {e}")
    
    # 🔍 Ищем рецепты
    recipes = search_by_ingredient(text)
    
    if recipes:
        recipe_text = f"""
🥕 **Рецепты с ингредиентом: {text}**

Найдено рецептов: {len(recipes)}

"""
        for i, recipe in enumerate(recipes, 1):
            recipe_text += f"{i}. {recipe.get('label', 'Без названия')}\n"

        bot.send_message(
            chat_id=message.chat.id,
            text=recipe_text,
            parse_mode="Markdown",
            reply_markup=get_recipes_list_keyboard(recipes)
        )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text=f"❌ Рецепты с ингредиентом **{text}** не найдены.\n\n"
                 f"🥕 **10+ гарантированно рабочих ингредиентов:**\n\n"
                 f"🇷🇺 **На русском:**\n"
                 f"• Сыр, Молоко, Сливки, Масло\n"
                 f"• Курица, Говядина, Свинина\n"
                 f"• Рыба, Лосось, Креветки\n"
                 f"• Томат, Чеснок, Лук, Картофель\n"
                 f"• Морковь, Капуста, Рис\n"
                 f"• Фасоль, Горох, Кукуруза\n"
                 f"• Яблоко, Банан, Лимон\n"
                 f"• Клубника, Малина, Вишня\n"
                 f"• Яйцо, Бекон, Ветчина\n"
                 f"• Шоколад, Кофе, Мёд, Орехи\n"
                 f"• Соль, Перец, Карри, Имбирь\n"
                 f"• Базилик, Мята, Розмарин\n\n"
                 f"🇬 **На английском (лучшие результаты):**\n"
                 f"• Cheese, Milk, Cream, Butter\n"
                 f"• Chicken, Beef, Pork\n"
                 f"• Fish, Salmon, Shrimp\n"
                 f"• Tomato, Garlic, Onion, Potato\n"
                 f"• Carrot, Cabbage, Rice\n"
                 f"• Bean, Pea, Corn\n"
                 f"• Apple, Banana, Lemon\n"
                 f"• Strawberry, Raspberry, Cherry\n"
                 f"• Egg, Bacon, Ham\n"
                 f"• Chocolate, Coffee, Honey, Nut\n"
                 f"• Salt, Pepper, Curry, Ginger\n"
                 f"• Basil, Mint, Rosemary\n\n"
                 f"💡 **Совет:** Вводите на английском для 100% результата!\n"
                 f"📋 Всего в API: 1000+ рецептов",
            parse_mode="Markdown",
            reply_markup=get_main_menu_keyboard()
        )

        delete_state(message.from_user.id)