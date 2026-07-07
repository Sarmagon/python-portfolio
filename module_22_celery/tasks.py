import os
import zipfile
from celery_app import celery_app
from celery import group
from image import blur_image
from mail import send_email, send_plain_email
from subscribers import get_subscribers

@celery_app.task
def blur_task(image_path: str, order_id: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.basename(image_path)
    dst_filename = os.path.join(output_dir, f'blur_{filename}')
    blur_image(image_path, dst_filename)
    return dst_filename

@celery_app.task
def process_order(image_paths: list, order_id: str, email: str):
    """
    Создаёт ZIP-архив с размытыми изображениями и отправляет email.
    """
    output_dir = f'results/{order_id}'
    zip_path = f'{output_dir}/blurred_images.zip'
    
    # Ждём, пока все файлы будут созданы (простая проверка)
    import time
    max_wait = 30  # секунд
    waited = 0
    
    while waited < max_wait:
        blurred_files = [
            f'{output_dir}/blur_{os.path.basename(path)}'
            for path in image_paths
        ]
        
        # Проверяем, все ли файлы существуют
        if all(os.path.exists(f) for f in blurred_files):
            break
        
        time.sleep(1)
        waited += 1
    
    # Создаём ZIP-архив
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for blurred_file in blurred_files:
            if os.path.exists(blurred_file):
                zipf.write(blurred_file, os.path.basename(blurred_file))
    
    # Отправляем email
    send_email(order_id, email, zip_path)
    
    return zip_path

@celery_app.task
def send_weekly_newsletter():
    subscribers = get_subscribers()
    subject = "Новости нашего сервиса обработки изображений"
    body = ("Здравствуйте! Напоминаем, что вы подписаны на новости сервиса. "
            "Мы постоянно улучшаем наши алгоритмы обработки изображений. "
            "Спасибо, что остаётесь с нами!")
    for email in subscribers:
        try:
            send_plain_email(email, subject, body)
        except Exception as e:
            print(f'Ошибка отправки на {email}: {e}')
    return f'Рассылка отправлена {len(subscribers)} подписчикам'