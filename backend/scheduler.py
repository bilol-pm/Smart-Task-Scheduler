class Task:
    def __init__(self, title, description, priority):
        self.title = title
        self.description = description
        self.priority = priority
    def display_task(self):
        return f"Title: {self.title}, Description: {self.description}, Priority: {self.priority}"


class PriorityQueue:
    def __init__(self):
        self.queue = []
    def is_empty(self):
        return len(self.queue) == 0

    def add_task(self, new_task):
        self.queue.append(new_task)
        self.queue.sort(key=lambda task: task.priority)
    def remove_task(self):
        if self.is_empty():
            return None
        return self.queue.pop(0)