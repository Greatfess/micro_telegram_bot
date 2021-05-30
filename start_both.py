import contextlib
import time
from threading import Thread
import os

import uvicorn
from uvicorn.config import Config

from telegram_client import start_teleclient
from trans_server import app


class Server(uvicorn.Server):
    def install_signal_handlers(self):
        pass

    @contextlib.contextmanager
    def run_in_thread(self):
        thread = Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()


def start():
    PORT = os.getenv('$PORT')
    print(PORT)
    print('another port', os.getenv('PORT'))
    config = Config(app, host="0.0.0.0", port=PORT, log_level="info")
    server = Server(config=config)

    with server.run_in_thread():
        start_teleclient()


if __name__ == '__main__':
    start()
