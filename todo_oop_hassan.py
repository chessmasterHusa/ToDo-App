from enum import Enum, auto
import os

class Status(Enum):
    NOT_STARTED = auto()
    IN_PROGRESS = auto()
    DONE = auto()

class Priority(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()

class OpeningMessage(Enum):
    CREATE = auto()
    UPDATE = auto()
    DELETE = auto()
    SHOW = auto()
    EXIT = 0

class UpdatingMessage(Enum):
    BY_ID = auto()
    BY_DESCRIPTION = auto()
    EXIT = 0

class Task:
    id_counter = 0

    def __init__(self, description: str, priority: Priority, status: Status = Status.NOT_STARTED):
        self.id = self.get_id()
        self.set_description(description)
        self.set_priority(priority)
        self.status = status

    def set_description(self, description: str):
        if not isinstance(description, str):
            raise ValueError(f"'description' must be a string, but {type(description)} is found.")
        self.description = description

    def set_priority(self, priority: Priority):
        if not isinstance(priority, Priority):
            raise ValueError(f"'priority' must be a Priority instance, but {type(priority)} is found.")
        self.priority = priority

    def __repr__(self):
        return f"Task(id={self.id}, description='{self.description}', priority={self.priority.name}, status={self.status.name})"

    @classmethod
    def get_id(cls):
        cls.id_counter += 1
        return cls.id_counter

class Todo:

    def __init__(self):
        self.tasks = []

    def add_task(self, task: Task):
        self.tasks.append(task)
    
    def get_all_tasks(self):
        return [(i + 1, task) for i, task in enumerate(self.tasks)]

    def get_task_by_id(self, id: int):
        for task in self.tasks:
            if id == task.id:
                return task

    def get_task_by_description(self, description: str):
        for task in self.tasks:
            if description == task.description:
                return task

    def show_tasks(self):
        if not self.tasks:
            print("No tasks available.")
        else:
            for num, task in self.get_all_tasks():
                print(f"Task number {num} :", task)

    def update_task(self, task: Task, task_description: str = "", task_priority=None, task_status=None):
        if task_description.strip():
            task.description = task_description
        if task_priority:
            task.priority = task_priority
        if task_status:
            task.status = task_status
        print("Task updated successfully!\n")

class Interface:
    def __init__(self):
        pass

    def run(self):
        pass

    def start(self):
        print(f"{self.__class__.__name__} is started")

class CMDInterface(Interface):

    def __init__(self, todo: Todo):
        super().__init__()
        self.todo = todo
        self.clear_screen()
        self.opening_message = "\n".join([
            "Please choose an option:",
            "1 : create a task",
            "2 : modify & update a task",
            "3 : delete a task",
            "4 : list all tasks",
            "0 : exit\n"
        ])
    
    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def run(self):
        while True:
            try:
                msg_code = OpeningMessage(int(input(self.opening_message)))
            except:
                self.clear_screen()
                print("INVALID CHOICE, PLEASE SELECT A VALID NUMBER\n")
                continue

            if msg_code == OpeningMessage.EXIT:
                self.clear_screen()
                while True:
                    want_to_exit = input("Are you really want to quit ? (Y/N)\n")
                    if want_to_exit.upper() == "Y":
                        self.clear_screen()
                        print("Thank you for using my app to create tour daily tasks\n")
                        quit()
                    elif want_to_exit.upper() == "N":
                        self.clear_screen()
                        break
                    else:
                        print("Please select a valid choice\t(Y : Yes\tN : No)\n")

            elif OpeningMessage.CREATE == msg_code:
                self.clear_screen()
                while True:
                    description = input("Add a task description:\t").strip()
                    if not description:
                        print("Description cannot be empty.\n")
                        continue
                    if any(task.description.lower() == description.lower() for task in self.todo.tasks):
                        print("A task with this description already exists. Please enter a different one.\n")
                        continue
                    break

                while True:
                    try:
                        priority = Priority(int(input("Add a task priority (1:Low, 2:Medium, 3:High):\t")))
                        break
                    except ValueError:
                        print("INVALID CHOICE, PLEASE SELECT A VALID NUMBER\n")
                task = Task(description=description, priority=priority)
                self.todo.add_task(task)
                self.clear_screen()
                print(f"Task '{description}' is created successfully.\n\n")

            elif msg_code == OpeningMessage.UPDATE:
                self.todo.show_tasks()
                while True:
                    try:
                        method = UpdatingMessage(int(input("Update by (1: ID, 2: Description, 0: Cancel): ")))
                    except:
                        print("Invalid update method.")
                        continue
                    break
                if method == UpdatingMessage.EXIT:
                    break
                if method == UpdatingMessage.BY_ID:
                    while True:
                        try:
                            task_id = int(input("Enter task ID: "))
                        except:
                            self.clear_screen()
                            print("INVALID TASK\n")
                            continue
                        break
                    task_to_update = self.todo.get_task_by_id(task_id)
                elif method == UpdatingMessage.BY_DESCRIPTION:
                    while True:
                        try:
                            desc = input("Enter task description: ")
                        except:
                            self.clear_screen()
                            print("INVALID TASK\n")
                            continue
                        break
                    task_to_update = self.todo.get_task_by_description(desc)
                if task_to_update:
                    task_description = input("New description (press Enter to skip): ")
                    while True:
                        try:
                            priority_input = input("New priority (1:Low, 2:Medium, 3:High, press Enter to skip): ")
                        except:
                            self.clear_screen()
                            print("INVALID TASK\n")
                            continue
                        break
                    while True:
                        try:
                            status_input = input("New status (1:Not started, 2:In progress, 3:Done, press Enter to skip): ")
                        except:
                            self.clear_screen()
                            print("INVALID TASK\n")
                            continue
                        break

                    task_priority = Priority(int(priority_input)) if priority_input.strip() else None
                    task_status = Status(int(status_input)) if status_input.strip() else None

                    self.todo.update_task(task_to_update, task_description, task_priority, task_status)
                else:
                    self.clear_screen()
                    print("Task not found.")

            elif msg_code == OpeningMessage.SHOW:
                self.clear_screen()
                self.todo.show_tasks()

            elif msg_code == OpeningMessage.DELETE:
                self.todo.show_tasks()
                try:
                    task_number = int(input("Enter the number of the task you want to delete (0 to cancel): "))
                    if task_number == 0:
                        continue
                    task_to_delete = dict(self.todo.get_all_tasks()).get(task_number)
                    if task_to_delete:
                        self.todo.tasks.remove(task_to_delete)
                        print("Task deleted successfully.\n")
                    else:
                        print("Invalid task number.\n")
                except ValueError:
                    print("Please enter a valid number.\n")


class QTInterface(Interface):
    def __init__(self):
        super().__init__()

    def run(self):
        pass

class WebInterface(Interface):
    def __init__(self):
        super().__init__()

    def run(self):
        pass

if __name__ == "__main__":
    todo = Todo()
    cmd = CMDInterface(todo)
    # cmd.start()
    cmd.run()
