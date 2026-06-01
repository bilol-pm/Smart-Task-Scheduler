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

if __name__ == "__main__":
    scheduler = PriorityQueue()

    while True:
        print("1. Add Task")
        print("2. View Current Tasks")
        print("3. Execute New Task")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            title = input("Enter Task Title: ")
            description = input("Enter Task Description: ")
            priority = int(input("Enter Task Priority: "))
            new_task = Task(title, description, priority)
            scheduler.add_task(new_task)
            print("Task added")
        elif choice == "2":
            if scheduler.is_empty():
                print("Queue is empty")
            else:
                for task in scheduler.queue:
                    print(task.display_task())
        elif choice == "3":
            if scheduler.is_empty():
                print("No task to execute")
            else:
                executed_task = scheduler.remove_task()
                print(f"Executing: {executed_task.title} (Priority: {executed_task.priority})")
        elif choice == "4":
            print("Goodbye")
            break
        else:
            print("Invalid choice")