import requests
import json
from tqdm import tqdm


class VkClient:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.vk.com/method/"
        self.version = "5.131"

    def get_photos(self, user_id, count=5):
        """Получение фотографий профиля пользователя."""
        params = {
            "owner_id": user_id,
            "album_id": "profile",
            "extended": 1,
            "photo_sizes": 1,
            "count": count,
            "v": self.version,
            "access_token": self.token,
        }
        response = requests.get(self.api_url + "photos.get", params=params).json()

        if "error" in response:
            error = response["error"]
            if error["error_code"] == 14:  # Капча
                captcha_img = error["captcha_img"]
                captcha_sid = error["captcha_sid"]
                print(f"Требуется капча: {captcha_img}")
                captcha_key = input("Введите текст с капчи: ")
                params["captcha_sid"] = captcha_sid
                params["captcha_key"] = captcha_key
                response = requests.get(self.api_url + "photos.get", params=params).json()

            if "error" in response:
                raise Exception(f"Ошибка VK API: {response['error']['error_msg']}")

        photos = []
        for item in response["response"]["items"]:
            max_size_photo = max(item["sizes"], key=lambda size: size["height"] * size["width"])
            file_name = f"{item['likes']['count']}.jpg"
            if any(photo["file_name"] == file_name for photo in photos):
                file_name = f"{item['likes']['count']}_{item['date']}.jpg"
            photos.append({"file_name": file_name, "size": max_size_photo["type"], "url": max_size_photo["url"]})

        return photos

    def save_photos_to_json(self, photos, file_name):
        """Сохранение информации о фотографиях в JSON."""
        with open(file_name, "w") as file:
            json.dump(photos, file, indent=4)