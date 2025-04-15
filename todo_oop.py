from enum import Enum
import os

class Status(Enum):
    """
    0 : NOT_STARTED
    1 : IN_PROGRESS
    2 : DONE
    """
    NOT_STARTED: int = 0
    IN_PROGRESS: int = 1
    DONE: int = 2

class Priority(Enum):
    """
    0 : LOW
    1 : MEDIUM
    2 : HIGH
    """
    LOW: int = 0
    MEDIUM: int = 1
    HIGH: int = 2

class OpeningMessage(Enum):
    """
    0 : EXIT
    1 : CREATE
    2 : UPDATE
    3 : SHOW
    """
    EXIT: int = 0
    CREATE: int = 1
    UPDATE: int = 2
    SHOW: int = 3


class Task:

    id_counter: int = 0

    description: str
    priority: Priority

    def __init__(
        self,
        description: str,
        priority: Priority,
        status: Status = Status.NOT_STARTED
    ):
        self.id: int = self.get_id()
        self.set_description(description=description)
        self.set_priority(priority=priority)

        self.status = status
        
    def set_description(self, description: str):
        if not isinstance(description, str):
            raise ValueError(f"'desciption' must be a string, but {type(description)} is found.")

        self.description = description

    def set_priority(self, priority: Priority):
        if not isinstance(priority, Priority):
            raise ValueError(f"'priority' must be a string, but {type(priority)} is found.")

        self.priority = priority

    def __repr__(self) -> str: 
        return f"Task(id={self.id}, description={self.description}, priority={self.priority}, status={self.status})"
    
    def get_id(self):
        Task.id_counter += 1
        return Task.id_counter



class Todo:

    def __init__(self):
        self.tasks: list[Task] = []

    def add_task(self, task: Task):
        self.tasks.append(task)
    
    def all_tasks(self):
        return self.tasks

    def get_task_by_id(self, id: int):
        for task in self.tasks:
            if id == task.id:
                return task
    
    def get_task_by_description(self, description: str):
        for task in self.tasks:
            if description == task.description:
                return task

    # def update_task(self, task: Task):
    #     pass
    
    # def show_tasks(self, task: Task):
    #     pass


class Interface:

    def __init__(self):
        ... 

    def run(self):
        ...

    def start(self):
        print(f"{self.__class__.__name__} is started")


class CMDInterface(Interface):

    def __init__(self, todo: Todo):
        super().__init__()
        self.todo = todo
        self.opening_message = "\n".join([
            "Please choose an option: ",
            "1 : create a task",
            "2 : modify & update a task",
            "3 : list all tasks",
            "0 : exit\n"
        ])

        self.updating_message = "\n".join([
            "Please the task you want to update:",
            "1 : by id"
            "2 : by description"
        ])
    
    def clear_screen(self):
        os.system("cls")

    def run(self):
        while True:
            try:
                msg_code = OpeningMessage(int(input(self.opening_message)))
            except:
                self.clear_screen()
                print("INVALID CHOICE, PLEASE SELECT A VALID NUMBER\n")
                continue
            if OpeningMessage.EXIT == msg_code:
                break
            elif OpeningMessage.CREATE == msg_code:
                description = input("Add a task description :\t")
                while True:
                    try:
                        priority = Priority(int(input("Add a task priority (0:Low, 1:Medium, 2:High) :\t")))
                        break
                    except:
                        print("INVALID CHOICE, PLEASE SELECT A VALID NUMBER\n")
                task = Task(description=description, priority=priority)
                self.todo.add_task(task)
                self.clear_screen()
                print(f"Task {description} is created\n\n")
            elif OpeningMessage.UPDATE == msg_code:
                pass
                # for task in Todo.tasks:
                #     print(task)
                # self.todo.get_task_by_id()
                # self.clear_screen()
            elif OpeningMessage.SHOW == msg_code:
                self.clear_screen()
                


class QTInterface(Interface):

    def __init__(self):
        super().__init__()

    def run(self):
        ...


class WebInterface(Interface):

    def __init__(self):
        super().__init__()

    def run(self):
        pass


if __name__ == "__main__":

    todo = Todo()
    cmd = CMDInterface(todo)
    cmd.start()
    cmd.run()

    # qt = QTInterface()
    # qt.start()


    # task = Task(
    #     description="hello",
    #     priority= Priority.LOW,

    # )
