import json

class FileManager:
    @staticmethod
    def load_tasks(file_path):
        """Tải danh sách công việc từ file JSON."""
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def save_tasks(file_path, tasks):
        """Lưu danh sách công việc vào file JSON."""
        with open(file_path, 'w') as file:
            json.dump(tasks, file, indent=4)

