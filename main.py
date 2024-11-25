import os
from dotenv import load_dotenv
from vk_api import VkClient
from yandex_disk_api import YandexDisk
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Загрузка токенов из .env
    load_dotenv()
    vk_token = os.getenv("VK_TOKEN")
    yandex_token = os.getenv("YANDEX_TOKEN")
    
    if not vk_token or not yandex_token:
        raise Exception("Не найдены токены в .env файле")

    vk_client = VkClient(vk_token)
    yandex_disk_client = YandexDisk(yandex_token)

    # Запрос ID пользователя
    user_id = input("Введите ID пользователя VK: ")
    photo_count = int(input("Введите количество фотографий для загрузки (по умолчанию 5): ") or 5)

    logging.info("Получаем фотографии профиля...")
    photos = vk_client.get_photos(user_id, photo_count)

    logging.info("Сохраняем информацию в JSON...")
    vk_client.save_photos_to_json(photos, "photos.json")

    folder_name = "VK_Photos"
    logging.info(f"Создаём папку '{folder_name}' на Яндекс.Диске...")
    yandex_disk_client.create_folder(folder_name)

    logging.info("Загружаем фотографии на Яндекс.Диск...")
    yandex_disk_client.upload_photos(folder_name, photos)

    logging.info("Все фотографии успешно загружены.")

if __name__ == "__main__":
    main()