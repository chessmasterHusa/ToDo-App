from enum import Enum, auto
import os

class Status(Enum):
    """
    1 : NOT_STARTED
    2 : IN_PROGRESS
    3 : DONE
    """
    NOT_STARTED: int = auto()
    IN_PROGRESS: int = auto()
    DONE: int = auto()

class Priority(Enum):
    """
    1 : LOW
    2 : MEDIUM
    3 : HIGH
    """
    LOW: int = auto()
    MEDIUM: int = auto()
    HIGH: int = auto()

class OpeningMessage(Enum):
    """
    1 : CREATE
    2 : UPDATE
    3 : DELETE
    4 : SHOW
    0 : EXIT
    """
    CREATE: int = auto()
    UPDATE: int = auto()
    DELETE: int = auto()
    SHOW: int = auto()
    EXIT: int = 0

class UpdatingMessage(Enum):
    """
    1 : by id
    2 : by description
    0 : cancel
    """
    BY_ID: int = auto()
    BY_DESCRIPTION: int = auto()
    EXIT: int = 0


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
            raise ValueError(f"'priority' must be a Priority instance, but {type(priority)} is found.")

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
        for task in self.get_all_tasks():
            print(f"Task number {task[0]} :", task[1])
    
    def update_task(self, task: Task, task_description: str, task_priority: Priority, task_status: Status):
        for the_task in self.get_all_tasks():
            if task_description:
                if task == the_task[1]:
                    task.description = task_description
            if task_priority:
                if task == the_task[1]:
                    task.priority = task_priority
            if task_status:
                if task == the_task[1]:
                    task.status = task_status
        print("Task updated successfuly!\n")

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
            "3 : delete a task",
            "4 : list all tasks",
            "0 : exit\n"
        ])

        self.updating_message = "\n".join([
            "Please choose the task you want to update/modify:",
            "\n".join(todo.get_all_tasks()),
            "0 : cancel\n"
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
                self.clear_screen()
                print("END")
                break
            elif OpeningMessage.CREATE == msg_code:
                while True:
                    description = input("Add a task description :\t")

                    break
                while True:
                    try:
                        priority = Priority(int(input("Add a task priority (1:Low, 2:Medium, 3:High) :\t")))
                        break
                    except:
                        print("INVALID CHOICE, PLEASE SELECT A VALID NUMBER\n")
                task = Task(description=description, priority=priority)
                self.todo.add_task(task)
                self.clear_screen()
                print(f"Task {description} is created\n\n")
            
            elif OpeningMessage.UPDATE == msg_code:
                todo.show_tasks()
                while True:
                    task_to_update = int(input("Choose the number of the task you want to update/modify\t(Tape 0 to exit)\n"))
                    if task_to_update in [the_task[0] for the_task in todo.get_all_tasks()]:
                        task_to_update = [the_task[1] for the_task in todo.get_all_tasks() if the_task[0] == task_to_update]
                        update_by_id_description = UpdatingMessage(int(input("Choose with which way you want to update the task\n1 : by id\n2 : by description\n")))
                        if UpdatingMessage.BY_ID == update_by_id_description:
                            task_to_update = self.todo.get_task_by_id(task_to_update)
                        elif UpdatingMessage.BY_DESCRIPTION == update_by_id_description:
                            task_to_update = self.todo.get_task_by_description(task_to_update)
                        else:
                            print("EROOR")
                        task_description = input("Enter the task description\t Tape on 'Space' and 'Enter' if you don't want to update the description of the task\t")
                        task_priority = input("Enter the task priority\t Tape on 'Space' and 'Enter' if you don't want to update the priority of the task\t")
                        task_status = input("Enter the task status\t Tape on 'Space' and 'Enter' if you don't want to update the status of the task\t")
                        todo.update_task(task_to_update, task_description=task_description, task_priority=task_priority, task_status=task_status)
                        todo.show_tasks()
                    elif task_to_update == 0:
                        break
                    else:
                        self.clear_screen()
                # self.clear_screen()
            elif OpeningMessage.DELETE == msg_code:
                pass
            elif OpeningMessage.SHOW == msg_code:
                self.clear_screen()
                todo.show_tasks()
                


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
