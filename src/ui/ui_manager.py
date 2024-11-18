import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, Label, Button
from models.task import Task
from models.task_list import TaskList
from datetime import datetime
from utils.file_manager import FileManager
from PIL import Image, ImageTk

FILE_PATH = "../data/tasks.json"

class UIManager:
    def __init__(self, root, task_list):
        self.root = root
        self.task_list = task_list
        self.filtered_tasks = task_list.tasks
        self.root.title("Quản lý công việc")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Đặt hình nền
        self.background_image_path = "/home/trungdt2/Desktop/WorkMana/task_manager/xongbay.jpg"
        self.create_background()
        self.create_widgets()

    def create_background(self):
        """Tạo ảnh nền với kích thước tự động điều chỉnh theo cửa sổ."""
        # Tạo Canvas trước khi tải ảnh nền
        self.canvas = tk.Canvas(self.root, width=700, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Tải và lưu ảnh gốc để có thể thay đổi kích thước động
        self.bg_image_original = Image.open(self.background_image_path)

        # Gọi update_background để hiển thị ảnh nền với kích thước hiện tại
        self.update_background()

        # Gắn sự kiện thay đổi kích thước cửa sổ để cập nhật hình nền
        self.root.bind("<Configure>", self.update_background)

    def update_background(self, event=None):
        """Cập nhật ảnh nền khi kích thước cửa sổ thay đổi."""
        # Lấy kích thước hiện tại của cửa sổ
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        # Thay đổi kích thước ảnh nền theo kích thước cửa sổ
        bg_image_resized = self.bg_image_original.resize((window_width, window_height), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image_resized)

        # Đặt ảnh nền mới lên Canvas
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

    def create_widgets(self):
        """Tạo các widget trên nền Canvas."""
        # Khung chứa tiêu đề
        title_frame = tk.Frame(self.canvas, bg="#343a40", pady=10)
        title_frame.pack(fill="x", pady=(10, 20))

        self.task_label = tk.Label(title_frame, text="Danh sách công việc", font=("Arial", 18, "bold"), bg="#343a40", fg="white")
        self.task_label.pack()

        # Khung chứa bộ lọc và danh sách công việc
        filter_frame = tk.Frame(self.canvas, bg="#f8f9fa", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=20)

        self.status_filter = tk.StringVar(value="All")
        self.status_menu = tk.OptionMenu(filter_frame, self.status_filter, "All", "Pending", "In Progress", "Completed", command=self.filter_tasks)
        self.status_menu.config(font=("Arial", 12))
        self.status_menu.pack(side="left", padx=5)

        self.task_listbox = tk.Listbox(filter_frame, font=("Arial", 12), width=70, height=10, bg="#e9ecef")
        self.task_listbox.pack(pady=10)

        # Khung chứa các trường nhập liệu
        input_frame = tk.Frame(self.canvas, bg="#f8f9fa", padx=10, pady=10)
        input_frame.pack(fill="x", padx=20, pady=(10, 20))

        self.task_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.task_entry.pack(fill="x", pady=5)
        self.task_entry.insert(0, "Nhập tên công việc mới...")

        self.due_date_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.due_date_entry.pack(fill="x", pady=5)
        self.due_date_entry.insert(0, "Nhập ngày hoàn thành (YYYY-MM-DD)")

        self.priority_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.priority_entry.pack(fill="x", pady=5)
        self.priority_entry.insert(0, "Nhập mức độ ưu tiên (Low, Medium, High)")

        # Khung chứa các nút chức năng
        button_frame = tk.Frame(self.canvas, bg="#f8f9fa", pady=10)
        button_frame.pack(fill="x", padx=20)

        self.add_task_button = tk.Button(button_frame, text="Thêm công việc", command=self.add_task, font=("Arial", 12), bg="#007bff", fg="white")
        self.add_task_button.pack(side="left", fill="x", expand=True, padx=5)

        self.change_status_button = tk.Button(button_frame, text="Thay đổi trạng thái", command=self.change_status, font=("Arial", 12), bg="#6c757d", fg="white")
        self.change_status_button.pack(side="left", fill="x", expand=True, padx=5)

        self.delete_task_button = tk.Button(button_frame, text="Xóa công việc", command=self.delete_task, font=("Arial", 12), bg="#dc3545", fg="white")
        self.delete_task_button.pack(side="left", fill="x", expand=True, padx=5)

        # Khung chứa các nút sắp xếp
        sort_frame = tk.Frame(self.canvas, bg="#f8f9fa", pady=10)
        sort_frame.pack(fill="x", padx=20, pady=(10, 20))

        self.sort_by_due_date_button = tk.Button(sort_frame, text="Sắp xếp theo ngày hoàn thành", command=self.sort_by_due_date, font=("Arial", 12), bg="#28a745", fg="white")
        self.sort_by_due_date_button.pack(side="left", fill="x", expand=True, padx=5)

        self.sort_by_priority_button = tk.Button(sort_frame, text="Sắp xếp theo mức độ ưu tiên", command=self.sort_by_priority, font=("Arial", 12), bg="#ffc107", fg="black")
        self.sort_by_priority_button.pack(side="left", fill="x", expand=True, padx=5)

        self.refresh_task_list()

    def refresh_task_list(self):
        """Cập nhật danh sách công việc hiển thị sau khi lọc."""
        self.task_listbox.delete(0, tk.END)
        for task in self.filtered_tasks:
            task_text = f"{task.id}: {task.name} - {task.status} - Due: {task.due_date} - Priority: {task.priority}"
            
            # Thêm màu sắc cho các trạng thái
            if task.status == "Pending":
                self.task_listbox.insert(tk.END, task_text)
                self.task_listbox.itemconfig(tk.END, {'bg': 'light yellow'})
            elif task.status == "In Progress":
                self.task_listbox.insert(tk.END, task_text)
                self.task_listbox.itemconfig(tk.END, {'bg': 'light blue'})
            elif task.status == "Completed":
                self.task_listbox.insert(tk.END, task_text)
                self.task_listbox.itemconfig(tk.END, {'bg': 'light green'})

    def add_task(self):
        """Thêm công việc mới với các thông tin từ các trường nhập liệu."""
        task_name = self.task_entry.get()
        due_date = self.due_date_entry.get()
        priority = self.priority_entry.get()

        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Lỗi", "Định dạng ngày không hợp lệ. Vui lòng nhập dạng YYYY-MM-DD.")
                return

        if priority not in ["Low", "Medium", "High"]:
            messagebox.showerror("Lỗi", "Mức độ ưu tiên không hợp lệ. Vui lòng nhập 'Low', 'Medium' hoặc 'High'.")
            return

        if task_name:
            new_task = Task(len(self.task_list.tasks) + 1, task_name, due_date=due_date, priority=priority)
            self.task_list.add_task(new_task)
            self.save_tasks()
            self.refresh_task_list()
            messagebox.showinfo("Thông báo", "Công việc mới đã được thêm!")
            self.clear_entries()

    def delete_task(self):
        """Xóa công việc được chọn."""
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task_id = int(self.task_listbox.get(selected_index).split(":")[0])
            task = self.task_list.get_task_by_id(task_id)
            if task:
                confirm = messagebox.askyesno("Xóa công việc", f"Bạn có chắc muốn xóa công việc '{task.name}' không?")
                if confirm:
                    self.task_list.tasks.remove(task)
                    self.save_tasks()
                    self.refresh_task_list()
                    messagebox.showinfo("Thông báo", "Công việc đã được xóa!")

    def change_status(self):
        """Thay đổi trạng thái của công việc đã chọn."""
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task_id = int(self.task_listbox.get(selected_index).split(":")[0])
            task = self.task_list.get_task_by_id(task_id)
            if task:
                if task.status == "Pending":
                    task.status = "In Progress"
                elif task.status == "In Progress":
                    task.status = "Completed"
                else:
                    task.status = "Pending"
                self.save_tasks()
                self.refresh_task_list()

    def sort_by_due_date(self):
        """Sắp xếp công việc theo ngày hoàn thành."""
        self.task_list.tasks.sort(key=lambda x: x.due_date or "")
        self.filtered_tasks = self.task_list.tasks  # Cập nhật danh sách đã lọc
        self.refresh_task_list()

    def sort_by_priority(self):
        """Sắp xếp công việc theo mức độ ưu tiên."""
        priority_order = {"Low": 1, "Medium": 2, "High": 3}
        self.task_list.tasks.sort(key=lambda x: priority_order.get(x.priority, 2))
        self.filtered_tasks = self.task_list.tasks  # Cập nhật danh sách đã lọc
        self.refresh_task_list()

    def filter_tasks(self, status):
        """Lọc danh sách công việc theo trạng thái."""
        if status == "All":
            self.filtered_tasks = self.task_list.tasks
        else:
            self.filtered_tasks = [task for task in self.task_list.tasks if task.status == status]
        self.refresh_task_list()

    def save_tasks(self):
        """Lưu công việc vào file JSON."""
        FileManager.save_tasks(FILE_PATH, [vars(task) for task in self.task_list.tasks])

    def clear_entries(self):
        """Xóa dữ liệu trong các trường nhập liệu."""
        self.task_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)

