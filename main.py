from taskito.cmd import CMDInterface
from taskito.task import TaskDB
from taskito.enums import OSType 

def main():

    task_db = TaskDB()

    cmd = CMDInterface(
        task_db= task_db, os=OSType.LINUX
    )

    cmd.run()


if __name__ == "__main__":
    main()