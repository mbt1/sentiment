import azure.functions as func
import logging


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.critical("got here")
    return func.HttpResponse("Hello, world!")
