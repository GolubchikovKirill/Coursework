import os
import json
from dotenv import load_dotenv
from vk_api import VkClient
from yandex_disk_api import YandexDisk

def main():
    # Загружаем переменные окружения
    load_dotenv()
    vk_token = os.getenv("VK_TOKEN")
    yandex_token = os.getenv("YANDEX_DISK_TOKEN")

    vk_client = VkClient(vk_token)
    yandex_client = YandexDisk(yandex_token)

    # Получаем ID пользователя
    user_id = input("Введите ID пользователя VK: ")

    # Получаем фотографии профиля
    print("Получаем фотографии профиля...")
    photos = vk_client.get_photos(user_id)

    # Форматируем данные для сохранения
    formatted_photos = []
    for photo in photos:
        file_name = f"{photo['likes']}.jpg"
        # Проверяем на совпадения имени
        if any(p["file_name"] == file_name for p in formatted_photos):
            file_name = f"{photo['likes']}_{photo['date']}.jpg"
        formatted_photos.append({"file_name": file_name, "url": photo["url"]})

    # Сохраняем данные в JSON
    print("Сохраняем информацию в JSON...")
    with open("photos.json", "w") as file:
        json.dump(formatted_photos, file, indent=4)
    print("Данные успешно сохранены в photos.json")

    # Создаем папку на Яндекс.Диске
    folder_name = "VK_Photos"
    yandex_client.create_folder(folder_name)

    # Загружаем фотографии на Яндекс.Диск
    print("Загружаем фотографии на Яндекс.Диск...")
    yandex_client.upload_photos(folder_name, formatted_photos)
    print("Загрузка завершена!")

if __name__ == "__main__":
    main()