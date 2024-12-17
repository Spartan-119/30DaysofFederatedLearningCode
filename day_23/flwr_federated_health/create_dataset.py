import pandas as pd
import os
from sklearn.model_selection import train_test_split
from typing import List

# load the dataset
data = pd.read_csv('day_23/flwr_federated_health/data/heart_disease_uci.csv')

# shuffle and split the data into n parts
def split_data(data, n_clients: int) -> List:
    clients = []
    for i in range(n_clients):
        # avoid the test size being 0.0 on the last iteration
        if n_clients - i == 1:
            client_data = data
        else: 
            client_data, data = train_test_split(data, test_size = 1 - 1 / (n_clients - i), random_state = 100)
            
        client_file = f"day_23/flwr_federated_health/data/client_{i + 1}.csv"
        client_data.to_csv(client_file, index = False)
        clients.append(client_file)
    
    print(f"Dataset split into {n_clients} clients successfully.")
    return clients

# testing this file
split_data(data, 5)