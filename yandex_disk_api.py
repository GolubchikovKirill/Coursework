import requests
from tqdm import tqdm


class YandexDisk:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://cloud-api.yandex.net/v1/disk/resources"

    def create_folder(self, folder_name):
        """Создаёт папку на Яндекс.Диске."""
        headers = {"Authorization": f"OAuth {self.token}"}
        params = {"path": folder_name}
        response = requests.put(self.api_url, headers=headers, params=params)

        if response.status_code not in [201, 409]:  # 201 - создано, 409 - уже существует
            raise Exception(f"Ошибка при создании папки: {response.json()}")

    def upload_photos(self, folder_name, photos):
        """Загружает фотографии на Яндекс.Диск."""
        headers = {"Authorization": f"OAuth {self.token}"}
        for photo in tqdm(photos, desc="Загрузка фотографий"):
            upload_url = f"{self.api_url}/upload"
            params = {"path": f"{folder_name}/{photo['file_name']}", "url": photo["url"]}
            response = requests.post(upload_url, headers=headers, params=params)

            if response.status_code != 202:  # 202 - успешно отправлено
                raise Exception(f"Ошибка загрузки фотографии: {response.json()}")
