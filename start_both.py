from trans_server import app
from telegram_client import start_teleclient
from threading import Thread
import uvicorn
import contextlib
import time
from uvicorn.config import Config


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


if __name__ == '__main__':
    config = Config(app, host="0.0.0.0", port=9000, log_level="info")
    server = Server(config=config)

    with server.run_in_thread():
        start_teleclient()
