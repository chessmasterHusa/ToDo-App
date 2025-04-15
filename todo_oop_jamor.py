from enum import Enum
import sys
import os

from typing import Optional

class Status(Enum):
    NOT_STARTED: int = 0
    IN_PROGRESS: int = 1
    DONE: int = 2

class Priority(Enum):
    LOW: int = 0
    MEDIUM: int = 1
    HIGH: int = 2

class MenuOption(Enum):
    EXIT: int = 0
    CREATE: int = 1
    UPDATE: int = 2
    SHOW: int = 3

class OS(Enum):
    LINUX: int = 0
    WINDOWS: int = 1


class Task:

    id_counter: int = 0

    description: str
    priority: Priority

    task_db: 'TaskDB' = None 

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

        self.max_len_desc: int = 60
        
    def set_description(self, description: str):
        if not isinstance(description, str):
            raise ValueError(f"'desciption' must be a string, but {type(description)} is found.")

        self.description = description

    def set_priority(self, priority: Priority):
        if not isinstance(priority, Priority):
            raise ValueError(f"'priority' must be a string, but {type(priority)} is found.")

        self.priority = priority

    def __repr__(self) -> str: 

        desc = self.description[:min(self.max_len_desc, len(self.description)) + 1]

        return f"Task(id={self.id}, desc=`{desc}{'...' if len(self.description) > self.max_len_desc else ''}`, status={self.status.name}, priority={self.priority.name})"
    
    def get_id(self):
        Task.id_counter += 1
        return Task.id_counter
    
    def set_task_db(self, task_db: 'TaskDB'):
        self.task_db = task_db 
    
    def save(self) -> 'Self':
        if (self.task_db is None) and not isinstance(self.task_db, TaskDB):
            raise AttributeError('`task_db` must be not None, use `set_task_db`')
         
        self.task_db.add_task(self)

        return self 


class TaskDB:

    def __init__(self):
        self.tasks: list[Task] = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def create(
        self, 
        description: str,
        priority: Priority,
        status: Status = Status.NOT_STARTED
    ) -> Task:
        
        task = Task(description=description, priority=priority, status=status)
        task.set_task_db(task_db=self)

        return task 
    
    def list(self):
        return self.tasks
    
    def __repr__(self):
        
        tasks_list_repr = ",\n".join([
            "\t" + repr(task) for task in self.list()
        ])

        return f"{self.__class__.__name__}([\n{tasks_list_repr}\n])"



class Interface:

    def __init__(self):
        ... 

    def run(self):
        ...

    def exit(self):
        sys.exit()

    def start(self):
        print(f"{self.__class__.__name__} is started")


class Logger:
    """" This class is used to handle all prints in the screen defined by `Interface` """
    def __init__(self):
        ... 

    def log(self):
        ... 


class CMDLogger(Logger):
    """" This class is used to handle all prints of `CDMInterface` """

    def __init__(self, os: OS = OS.LINUX):
        super().__init__()

        self.os = os 

        self.bar_length: int = 30
 
        self.messages = {
            "menu_options": "\n".join([
                                    self.add_bar(length=self.bar_length),
                                    "Please choose an option: ",
                                    self.add_bar(length=self.bar_length),
                                    "   1. Create a task",
                                    "   2. Modify & update a task",
                                    "   3. List all tasks",
                                    "   0. Exit",
                                    self.add_bar(length=self.bar_length),
                                ]),
            "menu_options_cmd": "Select an option: ", 
            "invalid_option": "Invalid Option, please retry.",
            "task_desc": "Task Desciprion: ",
            "task_priority": "Choose the task priority (0. LOW, 1. Medium, 2. High): ",
            "task_created": "Task is created: ",
            "tasks_list": "Tasks"
        }   
    
    def add_bar(self, length):
        return "-"*length

    def log(self, *message, msg: str = None):
        
        msgkw = self.messages.get(msg, "")
        print("\n".join(list(message) + [msgkw]))

    def continue_(self):
        input("\nContinue...")

    def clear(self):
        if self.os is OS.LINUX:
            os.system("clear")
        elif self.os is OS.WINDOWS:
            os.system("cls")
        else:
            raise ValueError("'os' must be a 'OS' option.")

    def menu_option_cls(self):
        self.clear()
        self.log(msg="menu_options")



class CMDReader:

    def __init__(self, logger: CMDLogger):
        self.logger = logger 


    def read_option(self, msg: str, enum: Enum) -> Optional[Enum]:

        try:
            inpt = input(msg)
            option = enum(int(inpt))
            return option
        except:
            return None 

    def option_menu(
        self, 
    ) -> Optional[MenuOption]:
        return self.read_option(
            msg= self.logger.messages["menu_options_cmd"],
            enum= MenuOption
        )
    
    def get_descr(self):
        return input(self.logger.messages["task_desc"])

    def get_priority(self) -> Optional[Priority]:
        return self.read_option(
            msg= self.logger.messages["task_priority"],
            enum= Priority
        )

class CMDInterface(Interface):

    def __init__(self, task_db: TaskDB, os: OS = OS.LINUX):
        super().__init__()

        self.task_db = task_db

        self.logger = CMDLogger(os=os)
        self.reader = CMDReader(logger= self.logger)

        self.running: bool = True  
    
    def create_task(self):
        self.logger.clear()

        desc = self.reader.get_descr()
        priority = self.reader.get_priority()

        if priority is not None:

            task = self.task_db.create(description=desc, priority=priority).save()  

            self.logger.log(
                "\n", self.logger.messages["task_created"], self.logger.add_bar(length=100), repr(task)
            )

        else:
            self.logger.log(msg="invalid_option")

        self.logger.continue_()


    def update_task(self):
        self.logger.clear()

    def list_all_tasks(self):
        self.logger.clear()

        self.logger.log(
            self.logger.messages["tasks_list"], self.logger.add_bar(100),
            "\n".join([
                repr(task) for task in self.task_db.list()
            ])
        )
        
        self.logger.continue_()

    def run(self):
    
        self.start()
        
        self.logger.menu_option_cls()
        
        while self.running:
            
            option: Optional[MenuOption] = self.reader.option_menu() # read from terminal option as `input`
            
            if option is not None:

                if option is MenuOption.CREATE:
                    self.create_task()

                if option is MenuOption.UPDATE:
                    self.update_task()

                if option is MenuOption.SHOW:
                    self.list_all_tasks()
                
                if option is MenuOption.EXIT:
                    self.exit()

                self.logger.menu_option_cls()

            else:
                self.logger.menu_option_cls()
                self.logger.log(msg="invalid_option")

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

    task_db = TaskDB()
    cmd = CMDInterface(task_db=task_db, os=OS.WINDOWS)
    cmd.run()
