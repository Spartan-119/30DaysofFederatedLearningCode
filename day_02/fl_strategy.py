"""
In this file, FedAvg strategy is implemented.
"""

from fl_setup import *

# create an instance of the model and get the parameters

params = get_parameters(Net())

def server_fn(context: Context) -> ServerAppComponents:
    # defining the FedAvg strategy
    strategy = FedAvg(
        fraction_fit = 0.3,
        fraction_evaluate = 0.3,
        min_fit_clients = 3,
        min_evaluate_clients = 3,
        min_available_clients = NUM_PARTITIONS,
        initial_parameters = ndarrays_to_parameters(params), # here i pass the initial model params
    )

    # now configure the server for 3 rounds of training
    config = ServerConfig(num_rounds = 3)
    return ServerAppComponents(strategy = strategy, config = config)

# similar to the ClientApp, we now create the ServerApp using the server_fn
server = ServerApp(server_fn = server_fn)