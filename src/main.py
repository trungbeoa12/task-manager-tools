from models.task import Task
from models.task_list import TaskList
from utils.file_manager import FileManager
from ui.ui_manager import UIManager
import tkinter as tk

if __name__ == "__main__":
    # Đường dẫn tới file JSON
    file_path = "../data/tasks.json"

    # Tải công việc từ file JSON
    loaded_tasks_data = FileManager.load_tasks(file_path)
    my_tasks = TaskList("Công việc cá nhân")

    for task_data in loaded_tasks_data:
        task = Task(
            task_data["id"], 
            task_data["name"], 
            task_data["description"], 
            task_data["status"], 
            task_data["due_date"], 
            task_data["priority"]
        )
        my_tasks.add_task(task)

    # Tạo giao diện Tkinter
    root = tk.Tk()
    app = UIManager(root, my_tasks)
    root.mainloop()

    # Lưu công việc sau khi đóng giao diện
    FileManager.save_tasks(file_path, [vars(task) for task in my_tasks.tasks])

