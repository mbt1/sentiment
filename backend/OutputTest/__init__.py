import azure.functions as func
import logging
from .OtherOutput import say_hello


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.critical("got here")
    mysay = say_hello()
    return func.HttpResponse(mysay.say())
