import logging

class say_hello:
    def __init__(self) -> None:
        logging.critical("say_hello class initialized")
    
    def say(self):
        logging.critical("say_hello.say called")
        return "Hello, world!"