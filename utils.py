import json
from tqdm import tqdm

def save_to_json(data, file_name="photos.json"):
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Данные успешно сохранены в {file_name}")

def show_progress_bar(iterable, description="Processing"):
    return tqdm(iterable, desc=description, ncols=80)