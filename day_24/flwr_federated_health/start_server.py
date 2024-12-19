import flwr as fl
from flwr.server import start_server

if __name__ == "__main__":
    start_server(server_address="localhost:8080")
