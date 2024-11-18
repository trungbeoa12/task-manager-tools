from datetime import datetime

class Task:
    def __init__(self, task_id, name, description="", status="Pending", due_date=None, priority="Medium"):
        self.id = task_id
        self.name = name
        self.description = description
        self.status = status
        self.due_date = due_date
        self.priority = priority
        self.notes = []
        self.attachments = []

    def update_status(self, new_status):
        self.status = new_status

    def add_note(self, note):
        self.notes.append(note)

    def attach_file(self, file_path):
        self.attachments.append(file_path)

    def __lt__(self, other):
        """So sánh công việc dựa trên due_date hoặc priority."""
        if self.due_date and other.due_date:
            return datetime.strptime(self.due_date, "%Y-%m-%d") < datetime.strptime(other.due_date, "%Y-%m-%d")
        # Sắp xếp theo priority nếu due_date không có
        priority_order = {"Low": 1, "Medium": 2, "High": 3}
        return priority_order[self.priority] < priority_order[other.priority]

