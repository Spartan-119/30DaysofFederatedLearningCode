import flwr as fl

# defining the strategy for fedlearning
strategy = fl.server.strategy.FedAvg(
    fraction_fit = 0.5,             # fraction of clients to train in each round
    fraction_evaluate = 0.5,        # fraction of clients to evaluate
    min_fit_clients = 2,            # minimum number of clients to train
    min_evaluate_clients = 2,       # minimum number of clients to evaluate
    min_available_clients = 2,      # minimum number of clients for the server
)

# starting hte FL server
if __name__ == "__main__":
    fl.server.start_server(
        server_address = "localhost:8080",
        strategy = strategy,
        config = fl.server.ServerConfig(num_rounds = 3), #{"num_rounds": 3},
    )