
import json
import logging
import time
logging.basicConfig(level = logging.INFO)
import functools
from websockets.sync.server import serve


class ChatServer:
    def __init__(self):

        self.clients = {}
        self.websockets = {}
        self.clients_start_time = {}
        self.max_clients = 4
        self.max_connection_time = 600
        logging.info("Chat Server Initialized")

    def get_wait_time(self):
        """
        Calculate and return the estimated wait time for clients.

        Returns:
            float: The estimated wait time in minutes.
        """
        wait_time = None

        for k, v in self.clients_start_time.items():
            current_client_time_remaining = self.max_connection_time - (time.time() - v)

            if wait_time is None or current_client_time_remaining < wait_time:
                wait_time = current_client_time_remaining

        return wait_time / 60
    
    def recv_message(self,websocket):
        logging.info("New client connected")
        options = websocket.recv()
        options = json.loads(options)
        print(options["message"])
        
        if len(self.clients) >= self.max_clients:
            logging.warning("Client Queue Full. Asking client to wait ...")
            wait_time = self.get_wait_time()
            response = {
                "uid": options["uid"],
                "status": "WAIT",
                "message": wait_time,
            }
            websocket.send(json.dumps(response))
            websocket.close()
            del websocket
            return
        
        client = ZhipuClient()
        self.clients[websocket] = client
        self.clients_start_time[websocket] = time.time()

        while True:
            try:
                message = websocket.recv()
                print(message)

                elapsed_time = time.time() - self.clients_start_time[websocket]
                if elapsed_time >= self.max_connection_time:
                    self.clients[websocket].disconnect()
                    logging.warning(f"Client with uid '{self.clients[websocket].client_uid}' disconnected due to overtime.")
                    self.clients[websocket].cleanup()
                    self.clients.pop(websocket)
                    self.clients_start_time.pop(websocket)
                    websocket.close()
                    del websocket
                    break

            except Exception as e:
                logging.error(e)
                self.clients.pop(websocket)
                self.clients_start_time.pop(websocket)
                del websocket
                break

    def run(self, host, port):
        with serve(
            self.recv_message,
            host="0.0.0.0",
            port=9091
        ) as server:
            server.serve_forever()

class ZhipuClient:
    pass