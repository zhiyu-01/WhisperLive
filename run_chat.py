from chat import ChatServer

if __name__ == "__main__":
    server = ChatServer()
    server.run("0.0.0.0",
               port=9091)