import requests
import time


class VkClient:
    def __init__(self, token):
        self.token = token
        self.api_version = "5.131"
        self.base_url = "https://api.vk.com/method/"
        self.max_retries = 5  # Максимальное количество попыток

    def get_photos(self, user_id, count=5):
        url = self.base_url + "photos.get"
        params = {
            "owner_id": user_id,
            "album_id": "profile",
            "extended": 1,
            "photo_sizes": 1,
            "count": count,
            "v": self.api_version,
            "access_token": self.token,
        }

        for attempt in range(self.max_retries):
            response = requests.get(url, params=params).json()

            # Проверка на капчу
            if "error" in response and response["error"]["error_code"] == 14:
                captcha_sid = response["error"]["captcha_sid"]
                captcha_img = response["error"]["captcha_img"]
                print(f"Пожалуйста, введите капчу: {captcha_img}")
                captcha_key = input("Введите текст с изображения: ")
                params.update({"captcha_sid": captcha_sid, "captcha_key": captcha_key})
                continue

            # Проверка других ошибок
            if "error" in response:
                error_msg = response["error"]["error_msg"]
                if error_msg.lower() == "retry":
                    print(f"Попытка {attempt + 1}/{self.max_retries}: Сервер запросил повторить.")
                    time.sleep(2 ** attempt)  # Увеличиваем время ожидания с каждой попыткой
                    continue
                else:
                    raise Exception(f"Ошибка VK API: {error_msg}")

            # Успешный ответ
            if "response" in response:
                photos = []
                for item in response["response"]["items"]:
                    max_size = max(item["sizes"], key=lambda x: x["width"] * x["height"])
                    photos.append({
                        "likes": item["likes"]["count"],
                        "date": item["date"],
                        "url": max_size["url"]
                    })
                return photos

        # Если все попытки исчерпаны
        raise Exception("Не удалось получить фотографии после нескольких попыток.")