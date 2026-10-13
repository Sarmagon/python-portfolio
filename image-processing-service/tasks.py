import os
import zipfile
from celery_app import celery_app
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
def process_order(blurred_files: list, order_id: str, email: str):
    """Chord callback: invoked only after every blur task succeeds."""
    if not blurred_files or not all(os.path.isfile(p) for p in blurred_files):
        raise ValueError("Incomplete image results; no archive or email created")
    output_dir = os.path.dirname(blurred_files[0])
    if any(os.path.dirname(p) != output_dir for p in blurred_files):
        raise ValueError("Image results belong to different orders")
    zip_path = os.path.join(output_dir, 'blurred_images.zip')
    with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
        for blurred_file in blurred_files:
            zipf.write(blurred_file, os.path.basename(blurred_file))
    # SMTP errors propagate to the task result; a ZIP alone is not completion.
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