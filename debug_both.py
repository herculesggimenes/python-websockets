from dotenv import load_dotenv
from threading import Thread
from client.main import Client
from server.main import Server
from server.services.logger import Logger

if __name__ == "__main__":
    load_dotenv()
    logger = Logger()
    server = Server(logger)
    server_thread = Thread(target=server.start, args=())
    server_thread.start()
    for index in range(5):
        client = Client()
        client_thread = Thread(target=client.start(),args=())
        client_thread.start()