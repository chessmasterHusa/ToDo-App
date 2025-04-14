from enum import Enum


class Status(Enum):
    NOT_STARTED: int = 0
    IN_PROGRESS: int = 1
    DONE: int = 2

class Priority(Enum):
    LOW: int = 0
    MEDIUM: int = 1
    HIGH: int = 2


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
        return f"Task(id={self.id})"
    
    def get_id(self):
        Task.id_counter += 1
        return Task.id_counter



class Todo:

    def __init__(self):
        self.tasks: list[Task] = []

    def add_task(self, task: Task):
        self.tasks.append(task)


class Interface:

    def __init__(self):
        ... 

    def run(self):
        ...

    def start(self):
        print(f"{self.__class__.__name__} is started")


class CMDInterface(Interface):

    def __init__(self):
        super().__init__()
        
        self.opening_message = "\n".join([
            "Please choose an option: ",
            "1. create a task",
            "2. list all tasks",
            "3. modify & update a task"
        ]) 

    def run(self):

        while True:
            print(self.opening_message) 
            input()


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

    cmd = CMDInterface()
    cmd.start()
    # cmd.run()

    qt = QTInterface()
    qt.start()


    # task = Task(
    #     description="hello",
    #     priority= Priority.LOW,

    # )
