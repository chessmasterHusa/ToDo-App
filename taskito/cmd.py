from taskito._base import Logger, Interface
from taskito.enums import Enum, Status, Priority, MenuOption, OSType
from typing import Optional

from taskito.task import Task, TaskDB

import os 


class CMDLogger(Logger):
    """" This class is used to handle all prints of `CDMInterface` """

    def __init__(self, os_type: OSType = OSType.LINUX):
        super().__init__()

        self.os_type = os_type 

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
            "tasks_list": "Tasks",
            "get_task_id" : "Choose The Task ID: ",
            "invalid_task_id": "Invalid Task IDs, please choose a valid one."
        }   
    
    def add_bar(self, length):
        return "-"*length

    def log(self, *message, msg: str = None):
        
        msgkw = self.messages.get(msg, "")
        print("\n".join(list(message) + [msgkw]))

    def continue_(self):
        input("\nContinue...")

    def clear(self):
        if self.os_type is OSType.LINUX:
            os.system("clear")
        elif self.os_type is OSType.WINDOWS:
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

    def get_task_id(self):
        
        try:
            return int(input(self.logger.messages["get_task_id"]))
        except:
            return None 

class CMDInterface(Interface):

    def __init__(self, task_db: TaskDB, os: OSType = OSType.LINUX):
        super().__init__()

        self.task_db = task_db

        self.logger = CMDLogger(os_type=os)
        self.reader = CMDReader(logger= self.logger)

        self.running: bool = True  
    
    def create_task(self):
        self.logger.clear()

        desc = self.reader.get_descr()
        priority = self.reader.get_priority()

        if priority is not None:

            task = self.task_db.create_task(description=desc, priority=priority).save()  

            self.logger.log(
                "\n", self.logger.messages["task_created"], self.logger.add_bar(length=100), repr(task)
            )

        else:
            self.logger.log(msg="invalid_option")

        self.logger.continue_()


    def update_task(self):
        self.logger.clear()
        
        self.list_all_tasks(continue_=False)

        task_id: Optional[int] = self.reader.get_task_id()

        if (task_id is not None) and task_id in list(map(lambda task: task.id, self.task_db.list())):
            
            # Todo: 
            # self.task_db.update_task(
            #     task_id= task_id,
            #     task = 
            # )

            ... 

        else:
            self.logger.log(self.logger.messages["invalid_task_id"])   
            self.logger.continue_()                                               


    def list_all_tasks(self, continue_: bool = True):
        self.logger.clear()

        self.logger.log(
            self.logger.messages["tasks_list"], self.logger.add_bar(100),
            "\n".join([
                repr(task) for task in self.task_db.list()
            ])
        )
        
        if continue_:
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
