import json
from datetime import datetime


class Task:
    def __init__(self, id, caption, create, done):
        self.id = id
        self.caption = caption
        self.create = create
        self.done = done
        
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'caption': self.caption,
            'create': self.create.isoformat(),
            'done': self.done
        }

    @classmethod
    def from_dict(cls, data):
        create = datetime.fromisoformat(data['create'])  # Deserialize datetime from string
        return cls(data['id'], data['caption'], create, data['done'])
    
    
    def is_caption(self, caption):
        return len(caption) > 3

class TaskManager:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.tasks = self.load_data_from_json()
    
    def load_data_from_json(self):
        try:
            with open(self.json_file_path, 'r') as json_file:
                data = json.load(json_file)
                tasks = [Task.from_dict(item) for item in data]
            return tasks
        except FileNotFoundError:
            return []

    def save_data_to_json(self):
        data = [task.to_dict() for task in self.tasks]
        with open(self.json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)

    def add_task(self, caption):
        new_task = Task(
            id=len(self.tasks) + 1,
            caption=caption,
            create=datetime.now(),
            done=False
        )
        self.tasks.append(new_task)
        self.save_data_to_json()
        print("Task added successfully.")

    def list_tasks(self):
        for task in self.tasks:
            print(f"ID: {task.id}, Caption: {task.caption}, Created: {task.create}, Done: {task.done}")

    def query_all(self):
        return self.tasks

    def query_by_id(self, task_id):
        return [task for task in self.tasks if task.id == task_id]

    def query_by_caption(self, caption):
        return [task for task in self.tasks if caption.lower() in task.caption.lower()]

    def query_done_tasks(self):
        return [task for task in self.tasks if task.done]
    
    def query_undone_tasks(self):
        return [task for task in self.tasks if not task.done]
