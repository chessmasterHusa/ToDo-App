import sys 


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