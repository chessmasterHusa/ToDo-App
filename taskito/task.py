from taskito.enums import Priority, Status


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

    def create_task(
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



