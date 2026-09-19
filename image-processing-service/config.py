"""
В этом файле будут секретные данные

Для создания почтового сервиса воспользуйтесь следующими инструкциями

- Yandex: https://yandex.ru/support/mail/mail-clients/others.html
- Google: https://support.google.com/mail/answer/7126229?visit_id=638290915972666565-928115075
"""

import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

SMTP_USER = os.getenv("SMTP_USER", "your_email@yandex.ru")
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.yandex.ru")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your_app_password")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))