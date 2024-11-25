import requests

class YandexDisk:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://cloud-api.yandex.net/v1/disk/resources"

    def create_folder(self, folder_name):
        url = self.base_url
        headers = {"Authorization": f"OAuth {self.token}"}
        params = {"path": folder_name}
        response = requests.put(url, headers=headers, params=params)

        if response.status_code == 201:
            print(f"Папка '{folder_name}' успешно создана.")
        elif response.status_code == 409:
            print(f"Папка '{folder_name}' уже существует.")
        else:
            print(f"Ошибка при создании папки: {response.text}")
            response.raise_for_status()

    def upload_photos(self, folder_name, photos):
        base_url = f"{self.base_url}/upload"
        headers = {"Authorization": f"OAuth {self.token}"}

        for photo in photos:
            file_name = photo["file_name"]
            file_url = photo["url"]
            disk_path = f"{folder_name}/{file_name}"

            params = {"path": disk_path, "url": file_url}
            response = requests.post(base_url, headers=headers, params=params)

            if response.status_code == 202:
                print(f"Фотография {file_name} успешно загружена.")
            else:
                print(f"Ошибка при загрузке {file_name}: {response.text}")
